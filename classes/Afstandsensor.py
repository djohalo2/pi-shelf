import RPi.GPIO as GPIO


class Afstandsensor:
    """
    Klasse om de afstandsensor uit te lezen die verbonden zijn
    met de Raspberry.
    """

    def __init__(self, input_pin: int) -> None:
        """
        Code die wordt uitgevoerd bij het instantieren van de klasse

        :param input_pin: De GPIO pin die wordt gebruikt op de
         raspberry als int.
        """
        # Instansieer de afstand sensor pin.
        self._afstandsensor_input_pin = input_pin
        GPIO.setup(self._afstandsensor_input_pin, GPIO.IN,
                   pull_up_down=GPIO.PUD_UP)

        # Zet fake opgepakt op false.
        self._fake_opgepakt = False

    def is_opgepakt(self) -> bool:
        """
        Kijk of de afstandsensor iets waar neemt.

        :return: True als de schoen is opgepakt, False als deze niet
         is opgepakt, als boolean.
        """
        return not GPIO.input(self._afstandsensor_input_pin)

    def is_fake_opgepakt(self) -> bool:
        """
        Controleer of het faken van het oppakken van de schoen
        true of false is.

        :return: True of False op basis van het faken.
        """
        return self._fake_opgepakt

    @property
    def fake_opgepakt(self) -> bool:
        """
        Getter voor de fake opgepakt.

        :return: fake opgepakt als boolean
        """
        return self._fake_opgepakt

    @fake_opgepakt.setter
    def fake_opgepakt(self, value: bool) -> None:
        """
        Setter voor de fake opgepakt.

        :param value: waarde als boolean
        """
        self._fake_opgepakt = value


def main() -> None:
    """
    Code om de klasse te testen, deze code wordt niet uitgevoerd als de
    klasse in een ander bestand wordt geimporteerd.
    """
    # Zet de pin mode op de Raspberry Pi.
    GPIO.setmode(GPIO.BOARD)

    # Instansieer een nieuwe afstandsensor.
    afstandsensor = Afstandsensor(11)

    # Test of de sensor werkt.
    print(afstandsensor.is_opgepakt())


# Zorg ervoor dat de main functie niet wordt uitgevoerd als de klasse
# wordt geimporteerd
if __name__ == '__main__':
    main()
