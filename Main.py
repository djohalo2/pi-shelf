from dotenv import load_dotenv, find_dotenv
import os

from classes.Afstandsensor import Afstandsensor
from classes.Button import Button
from classes.Led import Led
from classes.Reader import Reader
from classes.Scherm import Scherm
from classes.Shelf import Shelf
from classes.State import State

# Instantieer de .env.
load_dotenv(find_dotenv())

# Instantieer alles.
afstandsensor = Afstandsensor(os.environ.get("DISTANCE_SENSOR_PIN"))
knop = Button(os.environ.get("BUTTON_PIN"))
led_green = Led(os.environ.get("LED_GREEN_PIN"))
led_yellow = Led(os.environ.get("LED_YELLOW_PIN"))
led_red = Led(os.environ.get("LED_RED_PIN"))
reader = Reader()
display = Scherm()
shelf = Shelf(os.environ.get("BASE_URL"), os.environ.get("PRIVATE_KEY"))
state = State()
