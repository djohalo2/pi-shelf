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

            andere_maat = False

            for size in response_api['data']['sizes']:

                print(type(size))

                print(size['eu_size'])
                # if size['eu_size'] == response_api['data']['size']['eu_size']:
                #
                #     self._led_green.zet_aat()
                #     break
                #
                # else:
                #     andere_maat = True

            if andere_maat:
                self._led_yellow.zet_aan()

        # Als er geen maten zijn.
        else:

            # Ledje wordt rood.
            self._led_red.zet_aan()


def main() -> None:
    """
    
    :return: 
    """


if __name__ == '__main__':
    main()