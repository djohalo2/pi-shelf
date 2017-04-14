import RPi.GPIO as GPIO


class GPIOFuckUp:

    # noinspection PyBroadException
    def __init__(self):

        # Elke GPIO pin
        self._pins = [ 7, 11, 12,
                      13, 15, 16,
                      18, 22, 29,
                      31, 32, 33,
                      35, 36, 37,
                      38, 40]

        # Loop door elke GPIO pin heen
        for pin in self._pins:

            # Probeer de GPIO pin of false te zetten.
            try:

                # Zet de pin op false.
                GPIO.output(pin, False)

            # Als het fout gaat
            except:

                # Sla over.
                pass


def main() -> None:
    """
    Code om de klasse te testen, deze code wordt niet uitgevoerd als de
    klasse in een ander bestand wordt geimporteerd!
    """
    GPIO.setmode(GPIO.BOARD)
    GPIOFuckUp()


# Zorg ervoor dat de main functie niet wordt uitgevoerd als de klasse
# wordt geimporteerd
if __name__ == '__main__':
    main()
