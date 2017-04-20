from dotenv import load_dotenv, find_dotenv
import os
import RPi.GPIO as GPIO

from time import sleep

from classes.Afstandsensor import Afstandsensor
from classes.API import API
from classes.Button import Button
from classes.Led import Led
from classes.Reader import Reader
from classes.Scherm import Scherm
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
display = Scherm()


# Instantieer API.
API = API(os.environ.get("BASE_URL"), os.environ.get("PRIVATE_KEY"))

# Instantieer shelf.
shelf = Shelf(led_red, led_yellow, led_green)

# Instantieer states.
state = State()

# Alle GPIO pinnen worden op false gezet
GPIOFuckUp()

tekst_boven = API.get_shelf_information()["data"]["demo"]["product"]["shoe"]["name"]
tekst_onder = API.get_shelf_information()["data"]["demo"]["product"]["shoe"]["price"]

# Probeer het volgende.
try:

    # Loop dit door zolang het true is.
    while True:

        # Controleer of de display idle is
        if display.is_idle():
            display.set_information(tekst_boven, tekst_onder)
        # Lees de reader uit.
        reader.read()

        # Controleer of het UUID niet hetzelfde is.
        if reader.uuid != reader.huidige_uuid:

            # Als het een maat tag is.
            if not API.kan_koppelen():

                # Geef aan dat de maat gescanned is.
                maten = API.maat_gescanned(reader.uuid)

                #Haal maten op en zet in variabele
                display_maten = "Maten: "
                for size in maten["data"]["sizes"]:
                    display_maten += size.get('eu_size')[:2] + " "

                #Haal display van de idle staat af
                display.set_is_idle(False)

                #Toon gevonden maten op de display
                display.set_information(tekst_boven, display_maten)
                
                # Kijken of het request goed verlopen is.
                if not type(maten) is bool:

                    # Handel de ledjes af.
                    shelf.bepaal_ledjes(maten)

            # Er gaat een nieuwe schoen gekoppelt worden
            if API.kan_koppelen():

                # Geef aan dat er een nieuwe demo gescanned is.
                demo = API.demo_gescanned(reader.uuid)

        # Sla de huidige UUID op.
        reader.huidige_uuid = reader.uuid

        # Controleer of de schoen is opgepakt.
        if afstandsensor.is_opgepakt() and not afstandsensor.is_fake_opgepakt():

            # Zet het fake oppakken op true.
            afstandsensor.fake_opgepakt = True

            # Doe een API call.
            API.schoen_opgepakt()

        # Reset het oppakken.
        if not afstandsensor.is_opgepakt() and afstandsensor.is_fake_opgepakt():

            # Zet het fake oppakken weer op false.
            afstandsensor.fake_opgepakt = False

        # Controleer of de knop ingedrukt wordt.
        if button.is_pressed() and not button.is_fake_pressed():

            # Controleer of de reader een uuid.
            if reader.heeft_uuid():

                # Doe API call.
                API.knop_ingedrukt(reader.uuid)

                # Zet het fake indrukken op true.
                button.fake_pressed = True

        # Controleer of de knop losgelaten is en fake ingedrukt is.
        if not button.is_pressed() and button.is_fake_pressed():

            print("Knop is nu niet ingedrukt maar voorheen wel.")

            print("Reader is uitgelezen: " + str(reader.read()))

            if reader.read():

                button.fake_pressed = False

        # Wacht 200 milliseconden.
        sleep(0.2)

# Anders doe dit.
except KeyboardInterrupt:

    # GPIO cleanup
    GPIO.cleanup()

    # Alle GPIO pinnen worden op false gezet
    GPIOFuckUp()
