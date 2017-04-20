from __future__ import print_function, division, absolute_import, unicode_literals
try:
    from RPLCD.i2c import CharLCD
    from RPLCD import Alignment, CursorMode, ShiftMode
    from RPLCD import cursor
    from RPLCD import BacklightMode
except ImportError:
    print("Hello!")
    pass

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

    # function after button press
    def notify(self):
        notification = ' Een medewerker\r\n  komt er aan!'
        self.led.write_string(notification)
        input('Retailer notified')

    # function to show product and price
    def show_info(self):
        shoe = 'Nike Air Max'
        price = '150'
        self.lcd.write_string(shoe)
        self.lcd.write_string('\r\n')
        self.lcd.write_string(unichr(1))
        self.lcd.write_string(price)
        input('Price shown')

    # function to show sizes
    def show_sizes(self):
        self.lcd.write_string(' Voorraad maten ')
        input('')


def main():
    screen = Screen()
    try:
        screen.show_sizes()
    except KeyboardInterrupt:
        screen.lcd.clear()


# Clearing the display
if __name__ == '__main__':
    main()

