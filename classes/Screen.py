from __future__ import print_function, division, absolute_import, unicode_literals
import sys
from threading import ThreadError

sys.path.append('/usr/local/lib/python3.4/RPLCD/')
from RPLCD.i2c import CharLCD
from RPLCD import Alignment, CursorMode, ShiftMode
from RPLCD import cursor
from RPLCD import BacklightMode
from time import sleep
from multiprocessing import Process


class Screen:
    try:
        input = raw_input
    except NameError:
        pass

    try:
        unichr = unichr
    except NameError:
        unichr = chr

    # Defining LCD (i2c = port 1, i2c address is 3f), backlight turned on
    lcd = CharLCD(address=0x3f, port=1)
    lcd.backlight_enabled = True

    # Euro symbol defining and creating
    euro = (0b00110, 0b01001, 0b11110, 0b01000, 0b11110, 0b01001, 0b00110, 0b00000)
    lcd.create_char(1, euro)

    def __init__(self):
        """
        Uitvoeren code bij initialiseren klasse
        """
        self._fake_idle = False

        self._information_process = None

        self._demo_info = []

    # function after button press
    def notify(self):
        notification = ' Een medewerker\r\n  komt er aan!'
        self.lcd.write_string(notification)
        input('Retailer notified')

    def is_fake_idle(self):
        """
        Controleer of het faken van de display idle status True of False is.
        :return: True of False
        """
        return self._fake_idle

    # noinspection PyBroadException
    def thread_is_alive(self):
        """
        Controleert of er een thread bestaat.
        :return: True of False op basis op de thread bestaat, als boolean
        """
        try:
            return self._information_process.is_alive()
        except Exception as e:
            return False

    def information_in_process(self, tekst_boven, tekst_onder):
        """
        Voer de set_information functie uit in een aparte thread zodat er andere
        code tegelijkertijd gedraaid kan worden
        :param tekst_boven: De tekst voor de bovenste regel van de display 
                        als string
        :param tekst_onder: De tekst voor de bovenste regel van de display
                        als string
        """
        self._information_process = Process(target=self.set_information,
                                       args=(tekst_boven, tekst_onder, True))
        self._information_process.start()

    def set_information(self, tekst_boven, tekst_onder, need_timeout=False):
        """
        Zet de teksten die op de boven en onder regel van de display getoond moeten worden
        :param need_timeout: 
        :param tekst_boven: De tekst voor de bovenste regel van de display 
                        als string
        :param tekst_onder: De tekst voor de bovenste regel van de display
                        als string
        """
        self.lcd.clear()
        self.lcd.write_string(tekst_boven)
        self.lcd.write_string('\r\n')
        self.lcd.write_string(tekst_onder)

        if need_timeout:
            print("Going to sleep")
            sleep(3)
            print("Done sleeping")

    @property
    def fake_idle(self) -> bool:
        """
        Getter voor fake_pressed

        :return: fake_pressed als boolean
        """
        return self._fake_idle

    @fake_idle.setter
    def fake_idle(self, value: bool) -> None:
        """
        Setter voor fake_pressed.
        :param value: True of False
        """
        self._fake_idle = value

    @property
    def information_process(self) -> Process:
        """
        Getter voor fake_pressed

        :return: fake_pressed als boolean
        """
        return self._information_process

    @information_process.setter
    def information_process(self, value) -> None:
        """
        Setter voor fake_pressed.
        :param value: True of False
        """
        self._information_process = value


def main():
    screen = Screen()
    try:
        screen.show_sizes()
    except KeyboardInterrupt:
        screen.lcd.clear()


# Clearing the display
if __name__ == '__main__':
    main()

