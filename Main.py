from dotenv import load_dotenv, find_dotenv
import os
import RPi.GPIO as GPIO

from time import sleep

from classes.Afstandsensor import Afstandsensor
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
knop = Button(int(os.environ.get("BUTTON_PIN")))

# Instantieer ledjes.
led_green = Led(int(os.environ.get("LED_GREEN_PIN")))
led_yellow = Led(int(os.environ.get("LED_YELLOW_PIN")))
led_red = Led(int(os.environ.get("LED_RED_PIN")))

# Instantieer reader.
reader = Reader()

# Instantieer display.
display = Scherm()

# Instantieer shelf.
shelf = Shelf(os.environ.get("BASE_URL"), os.environ.get("PRIVATE_KEY"))

# Instantieer states.
state = State()

# Alle GPIO pinnen worden op false gezet
GPIOFuckUp()

huidige_uuid = ""

# Probeer het volgende.
try:

    # Loop dit door zolang het true is.
    while True:

        # Lees de UUID uit.
        reader.read()

        if reader.uuid is not huidige_uuid:
            print(reader.uuid)

        if reader.heeft_uuid():
            huidige_uuid = reader.uuid

        # Controleer of de schoen is opgepakt.
        if afstandsensor.is_opgepakt() and not afstandsensor.is_fake_opgepakt():

            # Zet het fake oppakken op true.
            afstandsensor.fake_opgepakt = True

            # Doe een API call.
            shelf.schoen_opgepakt()

        # Reset het oppakken.
        if not afstandsensor.is_opgepakt() and afstandsensor.is_fake_opgepakt():

            # Zet het fake oppakken weer op false.
            afstandsensor.fake_opgepakt = False

        # Wacht 200 milliseconden.
        sleep(0.2)

        # Test
        print("Einde van de loop.")

# Anders doe dit.
except KeyboardInterrupt:

    # GPIO cleanup
    GPIO.cleanup()

    # Alle GPIO pinnen worden op false gezet
    GPIOFuckUp()
