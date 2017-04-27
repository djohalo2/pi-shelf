import RPi.GPIO as GPIO

from time import sleep
from multiprocessing import Process



class Button:
    """
    Klasse om buttons uit te lezen die verbonden zijn met een raspberry
    """

    def __init__(self, input_pin: int, timeout_time: int = 30) -> None:
        """
        Code die wordt uitgevoerd bij het instantiëren van de klasse

        :param input_pin: De GPIO pin die wordt gebruikt op de raspberry
                          als int
        """
        # sla de button pin op.
        self._button_input_pin = input_pin
        self._timeout_time = timeout_time

        # Knop process
        self._button_process = None

        # Geef de pin setup op.
        GPIO.setup(self._button_input_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Geef aan de de fake pressed false is.
        self._fake_pressed = False

    def is_pressed(self) -> bool:
        """
        Kijk of de button is ingedrukt

        :return: True als de button is ingedrukt, False als deze niet
                 is ingedrukt, als boolean
        """
        # De raspberry geeft false terug als de button is ingedrukt en true
        # als deze niet is ingedrukt, dit is vrij verwarrend vandaar de we
        # return not gebruiken, hiermee draaien we deze logica om.
        return not GPIO.input(self._button_input_pin)

    def is_fake_pressed(self) -> bool:
        """
        Controleer of het faken van de knop True of False is.

        :return: True of False
        """
        return self.fake_pressed

    # noinspection PyBroadException
    def process_is_alive(self):
        """
        Controleert of er een thread bestaat.
        :return: True of False op basis op de thread bestaat, als boolean
        """
        try:
            return self._button_process.is_alive()
        except Exception as e:
            return False

    def start_process(self) -> None:
        """
        Start een timeout van 10 seconden in een thread.
        """
        self._button_process = Process(target=self.timeout)
        self._button_process.start()

    def timeout(self) -> None:
        """
        Start een timeout van 10 seconden.
        """
        sleep(self._timeout_time)

    @property
    def button_process(self) -> Process:
        """
        Getter voor button_process

        :return: button_process als Process
        """
        return self._button_process

    @button_process.setter
    def button_process(self, value: Process) -> None:
        """
        Setter voor button_process.

        :param value: Process
        """
        self._button_process = value

    @property
    def fake_pressed(self) -> bool:
        """
        Getter voor fake_pressed

        :return: fake_pressed als boolean
        """
        return self._fake_pressed

    @fake_pressed.setter
    def fake_pressed(self, value: bool) -> None:
        """
        Setter voor fake_pressed.
        :param value: True of False
        """
        self._fake_pressed = value


def main() -> None:
    """
    Code om de klasse te testen, deze code wordt niet uitgevoerd als de
    klasse in een ander bestand wordt geimporteerd!
    """
    # Zet de pin mode op de Raspberry Pi.
    GPIO.setmode(GPIO.BOARD)

    # Defineer een nieuwe button op pin 36.
    button = Button(36)

    # Geef terug of de knop is ingedrukt.
    print(button.is_pressed())


# Zorg ervoor dat de main functie niet wordt uitgevoerd als de klasse
# wordt geimporteerd
if __name__ == '__main__':
    main()
