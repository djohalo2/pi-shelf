import smbus
import time
from threading import Thread, ThreadError

class Scherm:
    """
    Klasse om Scherm aan te sturen
    """

    # Define some device parameters
    I2C_ADDR = 0x3f  # I2C device address
    LCD_WIDTH = 16  # Maximum characters per line

    # Define some device constants
    LCD_CHR = 1  # Mode - Sending data
    LCD_CMD = 0  # Mode - Sending command

    LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
    LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line
    LCD_LINE_3 = 0x94  # LCD RAM address for the 3rd line
    LCD_LINE_4 = 0xD4  # LCD RAM address for the 4th line

    LCD_BACKLIGHT = 0x08  # On
    # LCD_BACKLIGHT = 0x00  # Off

    ENABLE = 0b00000100  # Enable bit

    # Timing constants
    E_PULSE = 0.0005
    E_DELAY = 0.0005

    # Open I2C interface
    # bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
    bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

    def __init__(self):
        """
        Uitvoeren code bij initialiseren klasse
        """
        self.lcd_init()

        # uuid op de tag.
        self._is_idle = True

        self._demo_info = []

    def lcd_init(self):
        """
        Initialiseren van lcd scherm
        """
        # Initialise display
        self.lcd_byte(0x33, self.LCD_CMD)  # 110011 Initialise
        self.lcd_byte(0x32, self.LCD_CMD)  # 110010 Initialise
        self.lcd_byte(0x06, self.LCD_CMD)  # 000110 Cursor move direction
        self.lcd_byte(0x0C, self.LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
        self.lcd_byte(0x28, self.LCD_CMD)  # 101000 Data length, number of lines, font size
        self.lcd_byte(0x01, self.LCD_CMD)  # 000001 Clear display
        time.sleep(self.E_DELAY)


    def lcd_byte(self, bits, mode):
        """
        Versturen van bytes naar de datapinnen
        """

        bits_high = mode | (bits & 0xF0) | self.LCD_BACKLIGHT
        bits_low = mode | ((bits << 4) & 0xF0) | self.LCD_BACKLIGHT

        # High bits
        self.bus.write_byte(self.I2C_ADDR, bits_high)
        self.lcd_toggle_enable(bits_high)

        # Low bits
        self.bus.write_byte(self.I2C_ADDR, bits_low)
        self.lcd_toggle_enable(bits_low)


    def lcd_toggle_enable(self, bits):
        # Toggle enable
        time.sleep(self.E_DELAY)
        self.bus.write_byte(self.I2C_ADDR, (bits | self.ENABLE))
        time.sleep(self.E_PULSE)
        self.bus.write_byte(self.I2C_ADDR, (bits & ~self.ENABLE))
        time.sleep(self.E_DELAY)


    def lcd_string(self, message, line):
        # Send string to display

        message = message.ljust(self.LCD_WIDTH, " ")

        self.lcd_byte(line, self.LCD_CMD)

        for i in range(self.LCD_WIDTH):
            self.lcd_byte(ord(message[i]), self.LCD_CHR)

    def is_idle(self) -> bool:
        """
        Geeft terug of de waarde van de uuid leeg is of niet.
        :return: Boolean op basis van bovenstaande vraag.
        """
        return self._is_idle

    def set_is_idle(self, value):
        self._is_idle = value


    def thread_is_alive(self):
        """
        Controleert of er een thread bestaat.
        :return: True of False op basis op de thread bestaat, als boolean
        """
        try:
            return self.__information_thread.is_alive()
        except ThreadError as e:
            print("Exception (Scherm, thread_is_alive: {0})".format(e))
            return False
        except AttributeError as e:
            print("Exception (Scherm, thread_is_alive: {0})".format(e))
            return False

    def information_in_thread(self, tekst_boven, tekst_onder):
        """
        Voer de set_information functie uit in een aparte thread zodat er andere
        code tegelijkertijd gedraaid kan worden
        :param tekst_boven: De tekst voor de bovenste regel van de display 
                        als string
        :param tekst_onder: De tekst voor de bovenste regel van de display
                        als string
        """
        self.__information_thread = Thread(target=self.set_information,
                                           args=(tekst_boven, tekst_onder))
        self.__information_thread.start()

    def set_information(self, tekst_boven, tekst_onder):
        """
        Zet de teksten die op de boven en onder regel van de display getoond moeten worden
        :param tekst_boven: De tekst voor de bovenste regel van de display 
                        als string
        :param tekst_onder: De tekst voor de bovenste regel van de display
                        als string
        """

        self.lcd_string(tekst_boven, self.LCD_LINE_1)
        self.lcd_string(tekst_onder, self.LCD_LINE_2)



def main():

    scherm = Scherm()
    scherm.information_in_thread("Nike", "test")

    # Main program block



if __name__ == '__main__':
    main()
    # try:
    #     main()
    # except KeyboardInterrupt:
    #     pass
    # finally:
    #     lcd_byte(0x01, LCD_CMD)
