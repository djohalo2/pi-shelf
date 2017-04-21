from multiprocessing import Process
from time import sleep

from classes import Led


class Shelf:
    """
    De klasse shelf.
    """

    def __init__(self, led_red: Led, led_yellow: Led, led_green: Led) -> None:
        """
        
        :param led_red: 
        :param led_yellow: 
        :param led_green: 
        """
        # Zet alle ledjes.
        self._led_red = led_red
        self._led_yellow = led_yellow
        self._led_green = led_green

        # Zet de teksten.
        self._tekst_boven = ""
        self._tekst_onder = ""

        # Zet jet process.
        self._leds_process = None

    @property
    def tekst_boven(self) -> str:
        """
        Getter voor tekst_boven

        :return: tekst_boven als string
        """
        return self._tekst_boven

    @tekst_boven.setter
    def tekst_boven(self, value: str) -> None:
        """
        Setter voor tekst_boven.
        
        :param value: String
        """
        self._tekst_boven = value

    @property
    def tekst_onder(self) -> str:
        """
        Getter voor tekst_onder

        :return: tekst_onder als string
        """
        return self._tekst_onder

    @tekst_onder.setter
    def tekst_onder(self, value: str) -> None:
        """
        Setter voor tekst_onder.
        
        :param value: String
        """
        self._tekst_onder = value

    @property
    def leds_process(self) -> Process:
        """
        Getter voor leds_process

        :return: leds_process als Process
        """
        return self._leds_process

    @leds_process.setter
    def leds_process(self, value: Process) -> None:
        """
        Setter voor leds_process.
        
        :param value: Process
        """
        self._leds_process = value

    def process_is_alive(self):
        """
        Controleert of er een thread bestaat.
        :return: True of False op basis op de thread bestaat, als boolean
        """
        # Probeer.
        try:
            # Te kijken of het leds process bestaat.
            return self._leds_process.is_alive()

        # Zo niet.
        except Exception as e:

            # Geef terug dat het process niet bestaat.
            return False

    def bepaal_ledjes_in_process(self, response_api) -> None:
        """
        Bepaal de ledjes op basis van de response in een process.
        
        :param response_api: Response van de api als object.
        """
        self._leds_process = Process(target=self.bepaal_ledjes,
                                     args=(response_api,))
        self._leds_process.start()

    def bepaal_ledjes(self, response_api) -> None:
        """
        Bepaal de ledjes op basis van de response.
        
        :param response_api: Response van de api als object.
        """
        self._led_red.zet_uit()
        self._led_yellow.zet_uit()
        self._led_green.zet_uit()

        # Print alles
        if response_api['data']['sizes']:

            # Standaard is er geen andere maat.
            andere_maat = False

            # Ga door alle maten heen.
            for size in response_api['data']['sizes']:

                # Vergelijk de maten.
                if size.get('eu_size') == response_api['data']['tag']['size'][
                        'eu_size']:

                    # Zet het groene ledje aan.
                    self._led_green.zet_aan()

                    # Wacht 3 seconden.
                    sleep(3)

                    # Zet het groene ledje uit.
                    self._led_green.zet_uit()

                    # Zet andere maat op false.
                    andere_maat = False

                    # Stop.
                    break

                # Geef aan dat er andere maten zijn.
                andere_maat = True

            # Als er een andere maat is.
            if andere_maat:

                # Zet het gele ledje aan.
                self._led_yellow.zet_aan()

                # Wacht 3 seconden.
                sleep(3)

                # Zet het gele ledje uit.
                self._led_yellow.zet_uit()

        # Als er geen maten zijn.
        else:

            # Zet het rode ledje aan.
            self._led_red.zet_aan()

            # Wacht 3 seconden.
            sleep(3)

            # Zet het rode ledje uit.
            self._led_red.zet_uit()

    def set_tekst(self, shelf_information) -> None:
        """
        Zet de beide teksten.
        
        :param shelf_information: shelf informatie van de API als string.
        """
        # Zet de bovenste regel.
        self.tekst_boven = shelf_information["data"]["demo"]["product"][
            'shoe']["name"]

        # Zet de onderste regel.
        self.tekst_onder = shelf_information["data"]["demo"]["product"][
            'shoe']["price"]

    def get_maten(self, maten) -> str:
        """
        Verkijg alle maten als string.
        
        :param maten: Maten als object op basis van de API.
        
        :return: Een string voor op de display.
        """
        # De display string.
        display_maten = "Maten: "

        # Ga door alle maten in.
        for size in maten["data"]["sizes"]:

            # Voeg de maat toe aan de string.
            display_maten += size.get('eu_size')[:2] + " "

        # Geef de maten terug.
        return display_maten


def main() -> None:
    """
    Test methode voor de klasse.
    """
    pass

if __name__ == '__main__':
    main()
