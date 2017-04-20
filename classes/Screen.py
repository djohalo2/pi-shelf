from __future__ import print_function, division, absolute_import, unicode_literals
import sys
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
        # uuid op de tag.
        self._is_idle = True

        self._is_fake_idle = False

        self._demo_info = []

    # function after button press
    def notify(self):
        notification = ' Een medewerker\r\n  komt er aan!'
        self.led.write_string(notification)
        input('Retailer notified')

    def is_idle(self) -> bool:
        """
        Geeft terug of de waarde van de uuid leeg is of niet.
        :return: Boolean op basis van bovenstaande vraag.
        """
        return self._is_idle

    def is_fake_idle(self):
        """
        Controleer of het faken van de display idle status True of False is.
        :return: True of False
        """
        return self._is_fake_idle

    def set_is_idle(self, value):
        self._is_idle = value

    # def thread_is_alive(self):
    #     """
    #     Controleert of er een thread bestaat.
    #     :return: True of False op basis op de thread bestaat, als boolean
    #     """
    #     try:
    #         return self.__information_thread.is_alive()
    #     except ThreadError as e:
    #         print("Exception (Scherm, thread_is_alive: {0})".format(e))
    #         return False
    #     except AttributeError as e:
    #         print("Exception (Scherm, thread_is_alive: {0})".format(e))
    #         return False

    def information_in_process(self, tekst_boven, tekst_onder):
        """
        Voer de set_information functie uit in een aparte thread zodat er andere
        code tegelijkertijd gedraaid kan worden
        :param tekst_boven: De tekst voor de bovenste regel van de display 
                        als string
        :param tekst_onder: De tekst voor de bovenste regel van de display
                        als string
        """
        self.__information_process = Process(target=self.set_information,
                                           args=(tekst_boven, tekst_onder, True))
        self.__information_process.start()

        return self.__information_process

    def set_information(self, tekst_boven, tekst_onder, needTimeout=False):
        """
        Zet de teksten die op de boven en onder regel van de display getoond moeten worden
        :param tekst_boven: De tekst voor de bovenste regel van de display 
                        als string
        :param tekst_onder: De tekst voor de bovenste regel van de display
                        als string
        """
        self.lcd.clear()
        self.lcd.write_string(tekst_boven)
        self.lcd.write_string('\r\n')
        self.lcd.write_string(tekst_onder)

        if needTimeout:
            print("Going to sleep")
            sleep(10)
            print("Done sleeping")


def main():
    screen = Screen()
    try:
        screen.show_sizes()
    except KeyboardInterrupt:
        screen.lcd.clear()


# Clearing the display
if __name__ == '__main__':
    main()

