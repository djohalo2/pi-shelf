import os
import RPi.GPIO as GPIO

from dotenv import load_dotenv, find_dotenv
from time import sleep


from classes.Afstandsensor import Afstandsensor
from classes.API import API
from classes.Button import Button
from classes.Led import Led
from classes.Reader import Reader
from classes.Screen import Screen
from classes.Shelf import Shelf
from classes.State import State

from util.GPIOFuckUp import GPIOFuckUp

# Alle GPIO pinnen worden op false gezet
GPIOFuckUp()

# Board mode.
GPIO.setmode(GPIO.BOARD)

# Instantieer de .env.
load_dotenv(find_dotenv())

# Instantieer afstandsensor.
afstandsensor = Afstandsensor(int(os.environ.get("DISTANCE_SENSOR_PIN")))

# Instantieer knop.
button = Button(int(os.environ.get("BUTTON_PIN")))

# Instantieer ledjes.
led_green = Led(int(os.environ.get("LED_GREEN_PIN")))
led_yellow = Led(int(os.environ.get("LED_YELLOW_PIN")))
led_red = Led(int(os.environ.get("LED_RED_PIN")))

# Instantieer reader.
reader = Reader()

# Instantieer display.
display = Screen()


# Instantieer API.
API = API(os.environ.get("BASE_URL"), os.environ.get("PRIVATE_KEY"))

# Instantieer shelf.
shelf = Shelf(led_red, led_yellow, led_green)

# Instantieer states.
state = State()

# Alle GPIO pinnen worden op false gezet
GPIOFuckUp()

# Zet de tekst.
shelf.set_tekst(API.get_shelf_information())

# Probeer het volgende.
try:

    # Loop dit door zolang het true is.
    while True:

        # Controleer of de display idle is
        if not display.thread_is_alive() and not display.is_fake_idle():

            # Zet informatie op het scherm.
            display.set_information(shelf.tekst_boven, shelf.tekst_onder)

            # Toggle de fake idle.
            display.fake_idle = True

            # Reset de readers.
            reader.reset()

        # Lees de reader uit.
        reader.read()

        # Controleer of het UUID niet hetzelfde is.
        if reader.uuid != reader.huidige_uuid:

            # Als het een maat tag is.
            if not API.kan_koppelen():

                # Geef aan dat de maat gescanned is.
                maten = API.maat_gescanned(reader.uuid)

                # Controleer of de procress leeft.
                if display.thread_is_alive():

                    # Stop het proces.
                    display.information_process.terminate()

                # Toon de informatie op het scherm.
                display.information_in_process(shelf.tekst_boven,
                                               shelf.get_maten(maten))

                # Zet de idle terug naar false.
                display.fake_idle = False

                # Kijken of het request goed verlopen is.
                if not type(maten) is bool:

                    # Kijk even of er ledjes branden.
                    if shelf.process_is_alive():

                        # Opflikkeren.
                        shelf.leds_process.terminate()

                    # Handel de ledjes af.
                    shelf.bepaal_ledjes_in_process(maten)

            # Er gaat een nieuwe schoen gekoppelt worden
            if API.kan_koppelen():

                # Geef aan dat er een nieuwe demo gescanned is.
                demo = API.demo_gescanned(reader.uuid)

        # Sla de huidige UUID op.
        reader.huidige_uuid = reader.uuid

        # Controleer of de schoen is opgepakt.
        if afstandsensor.is_opgepakt() and \
                not afstandsensor.is_fake_opgepakt():

            # Zet het fake oppakken op true.
            afstandsensor.fake_opgepakt = True

            # Doe een API call.
            API.schoen_opgepakt()

        # Reset het oppakken.
        if not afstandsensor.is_opgepakt() and \
                afstandsensor.is_fake_opgepakt():

            # Zet het fake oppakken weer op false.
            afstandsensor.fake_opgepakt = False

        # Controleer of de knop ingedrukt wordt.
        if button.is_pressed() and not button.is_fake_pressed():

            # Controleer of de reader een uuid.
            if reader.heeft_uuid():

                # Doe API call.
                API.knop_ingedrukt(reader.laatste_uuid)

                # Start het process.
                button.start_process()

                # Zet het fake indrukken op true.
                button.fake_pressed = True

        # Controleer of de knop losgelaten is en fake ingedrukt is.
        if not button.is_pressed() and button.is_fake_pressed():

            # RFID leest iets uit.
            if not button.process_is_alive():

                # Fake pressed.
                button.fake_pressed = False

        # Wacht 200 milliseconden.
        sleep(0.2)

# Anders doe dit.
except KeyboardInterrupt:

    # GPIO cleanup
    GPIO.cleanup()

    # Alle GPIO pinnen worden op false gezet
    GPIOFuckUp()
