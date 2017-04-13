import RPi.GPIO as GPIO


class Button:
    """
    Klasse om buttons uit te lezen die verbonden zijn met een raspberry
    """

    def __init__(self, input_pin: int) -> None:
        """
        Code die wordt uitgevoerd bij het instantiëren van de klasse

        :param input_pin: De GPIO pin die wordt gebruikt op de raspberry
                          als int
        """
        self.__button_input_pin = input_pin
        GPIO.setup(self.__button_input_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.__fake_pressed = False

    def is_pressed(self) -> bool:
        """
        Kijk of de button is ingedrukt

        :return: True als de button is ingedrukt, False als deze niet
                 is ingedrukt, als boolean
        """
        # De raspberry geeft false terug als de button is ingedrukt en true
        # als deze niet is ingedrukt, dit is vrij verwarrend vandaar de we
        # return not gebruiken, hiermee draaien we deze logica om
        return not GPIO.input(self.__button_input_pin)

    def is_fake_pressed(self) -> bool:
        """
        Controleer of het faken van de knop True of False is.

        :return: True of False
        """
        return self.fake_pressed

    @property
    def fake_pressed(self) -> bool:
        """
        Getter voor fake_pressed

        :return: fake_pressed als boolean
        """
        return self.__fake_pressed

    @fake_pressed.setter
    def fake_pressed(self, value: bool) -> None:
        """
        Setter voor fake_pressed.
        :param value: True of False
        """
        self.__fake_pressed = value


def main() -> None:
    """
    Code om de klasse te testen, deze code wordt niet uitgevoerd als de
    klasse in een ander bestand wordt geimporteerd!
    """
    # Zet de pin mode op de Raspberry Pi.
    GPIO.setmode(GPIO.BOARD)

    button = Button(36)
    print(button.is_pressed())


# Zorg ervoor dat de main functie niet wordt uitgevoerd als de klasse
# wordt geimporteerd
if __name__ == '__main__':
    main()
