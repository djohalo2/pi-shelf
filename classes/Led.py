import RPi.GPIO as GPIO
from time import sleep


class Led:
    """
    Klasse om een led aan of uit te zetten die verbonden is met de
    Raspberry Pi.
    """

    def __init__(self, output_pin: int) -> None:
        """
        Code die wordt uitgevoerd bij het instantieren van de klasse.

        :param output_pin: De GPIO pin die gebruikt wordt op de Raspberry.
        """
        # Sla de output pin op.
        self._led_output_pin = output_pin

        # Stel de pin setup in.
        GPIO.setup(self._led_output_pin, GPIO.OUT)

    def zet_aan(self) -> None:
        """
        Zet de LED aan.
        """
        GPIO.output(self._led_output_pin, True)

    def zet_uit(self) -> None:
        """
        Zet de LED uit.
        """
        GPIO.output(self._led_output_pin, False)


def main() -> None:
    """
    Code om de klasse te testen, deze code wordt niet uitgevoerd als de
    klasse in een ander bestand wordt geimporteerd.
    """
    # Zet de pin mode op de Raspberry Pi.
    GPIO.setmode(GPIO.BOARD)

    # Maak alle ledjes aan.
    rood = Led(15)
    geel = Led(16)
    groen = Led(13)

    # Zet alle ledjes aan.
    rood.zet_aan()
    geel.zet_aan()
    groen.zet_aan()

    # Wacht 1 seconden.
    sleep(1)

    # Zet alle ledjes uit.
    rood.zet_uit()
    geel.zet_uit()
    groen.zet_uit()


# Zorg ervoor dat de main functie niet wordt uitgevoerd als de klasse
# wordt geimporteerd
if __name__ == '__main__':
    main()
