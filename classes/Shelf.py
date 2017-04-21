from multiprocessing import Process
from time import sleep


class Shelf:
    """
    
    """
    def __init__(self, led_red, led_yellow, led_green) -> None:
        """
        
        :param led_red: 
        :param led_yellow: 
        :param led_green: 
        """
        self._led_red = led_red
        self._led_yellow = led_yellow
        self._led_green = led_green

        self._tekst_boven = ""
        self._tekst_onder = ""

        self._leds_process = None

    @property
    def tekst_boven(self) -> str:
        """
        Getter voor fake_pressed

        :return: fake_pressed als boolean
        """
        return self._tekst_boven

    @tekst_boven.setter
    def tekst_boven(self, value: str) -> None:
        """
        Setter voor fake_pressed.
        :param value: True of False
        """
        self._tekst_boven = value

    @property
    def tekst_onder(self) -> str:
        """
        Getter voor fake_pressed

        :return: fake_pressed als boolean
        """
        return self._tekst_onder

    @tekst_onder.setter
    def tekst_onder(self, value: str) -> None:
        """
        Setter voor fake_pressed.
        :param value: True of False
        """
        self._tekst_onder = value

    def process_is_alive(self):
        """
                Controleert of er een thread bestaat.
                :return: True of False op basis op de thread bestaat, als boolean
                """
        try:
            return self._leds_process.is_alive()
        except Exception as e:
            return False

    def bepaal_ledjes_in_process(self, response_api):
        """
        
        :param response_api: 
        :return: 
        """
        self._leds_process = Process(target=self.bepaal_ledjes,
                                     args=(response_api,))
        self._leds_process.start()

    def bepaal_ledjes(self, response_api) -> None:
        """
        
        :param response_api: 
        :return: 
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
                if size.get('eu_size') == response_api['data']['tag']['size']['eu_size']:

                    # Zet het groene ledje aan.
                    self._led_green.zet_aan()
                    sleep(3)
                    self._led_green.zet_uit()

                    # Zet op false.
                    andere_maat = False
                    break

                # Geef aan dat er andere maten zijn.
                andere_maat = True

            # Als er een andere maat is.
            if andere_maat:

                # Zet het gele ledje aan.
                self._led_yellow.zet_aan()
                sleep(3)
                self._led_yellow.zet_uit()

        # Als er geen maten zijn.
        else:

            # Ledje wordt rood.
            self._led_red.zet_aan()
            sleep(3)
            self._led_red.zet_uit()

    def set_tekst(self, shelf_information) -> None:
        """
        
        :param shelf_information: 
        :return: 
        """
        self.tekst_boven = shelf_information["data"]["demo"]["product"]["shoe"]["name"]
        self.tekst_onder = shelf_information["data"]["demo"]["product"]["shoe"]["price"]

    def get_maten(self, maten) -> str:
        """
        
        :param maten: 
        :return: 
        """
        display_maten = "Maten: "

        for size in maten["data"]["sizes"]:
            display_maten += size.get('eu_size')[:2] + " "

        return display_maten

    @property
    def leds_process(self) -> Process:
        """
        Getter voor fake_pressed

        :return: fake_pressed als boolean
        """
        return self._leds_process

    @leds_process.setter
    def leds_process(self, value) -> None:
        """
        Setter voor fake_pressed.
        :param value: True of False
        """
        self._leds_process = value


def main() -> None:
    """
    
    :return: 
    """


if __name__ == '__main__':
    main()