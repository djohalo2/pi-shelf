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

# Board mode.
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()

# Instantieer de .env.
load_dotenv(find_dotenv())

# Instantieer afstandsensor.
afstandsensor = Afstandsensor(os.environ.get("DISTANCE_SENSOR_PIN"))

# Instantieer knop.
knop = Button(os.environ.get("BUTTON_PIN"))

# Instantieer ledjes.
led_green = Led(os.environ.get("LED_GREEN_PIN"))
led_yellow = Led(os.environ.get("LED_YELLOW_PIN"))
led_red = Led(os.environ.get("LED_RED_PIN"))

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

try:

    # Wacht 200 milliseconden.
    sleep(0.2)

except KeyboardInterrupt:

    # GPIO cleanup
    GPIO.cleanup()

    # Alle GPIO pinnen worden op false gezet
    GPIOFuckUp()