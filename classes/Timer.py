from time import sleep
from multiprocessing import Process


class Timer:
    """

    """
    def __init__(self):
        """

        """
        self._timer_process = None

    # noinspection PyBroadException
    def process_is_alive(self):
        """
        Controleert of er een thread bestaat.
        :return: True of False op basis op de thread bestaat, als boolean
        """
        try:
            return self._timer_process.is_alive()
        except Exception as e:
            return False

    def start_process(self, time: int) -> None:
        """
        Start een timeout van 10 seconden in een thread.
        """
        self._timer_process = Process(target=self.timeout, args=(time,))
        self._timer_process.start()

    def timeout(self, time: int) -> None:
        """
        Start een timeout van x seconden.
        :param time: tijd.
        """
        sleep(time)



def main() -> None:
    """
    Code om de klasse te testen, deze code wordt niet uitgevoerd als de
    klasse in een ander bestand wordt geimporteerd!
    """

    # Defineer een nieuwe timer.
    timer = Timer()

    # Start timeout van 10 seconden.
    timer.start_process(10)

    # Wacht 5 seconden.
    sleep(5)

    # Is alive?
    print("Slaapt: " + str(timer.process_is_alive()))

    # Wacht 5 seconden.
    sleep(7)

    # Is alive?
    print("Slaapt: " + str(timer.process_is_alive()))


# Zorg ervoor dat de main functie niet wordt uitgevoerd als de klasse
# wordt geimporteerd
if __name__ == '__main__':
    main()
