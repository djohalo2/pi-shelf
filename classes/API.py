from uuid import getnode as get_mac
import requests


class API:
    """
    
    """

    def __init__(self, base_url: str, private_key: str) -> None:
        """
        
        :param base_url: 
        :param private_key: 
        """
        self._base_url = base_url
        self._private_key = private_key

        self._token = ""
        self._mac_address = ""

        self.set_mac_address()
        self.connect()
        self.authenticate()

    def connect(self):
        """
        Connect call om de shelf te connecten aan de backend
        :return: True of False op basis van status code van de request
        """
        r = requests.post(
            self._base_url + "/shelves/" + self.get_mac_address() + "/connect",
            data={'private_key': self._private_key})
        if r.status_code == 200:
            return True
        else:
            return False

    def authenticate(self):
        """
        Authenticeer de shelf met inloggegevens om een token te ontvangen
        :return: Bij succesvol authenticatie geef token terug, anders False
        """

        r = requests.post(self._base_url + "/authenticate/shelf",
                          data={'mac_address': self.get_mac_address(),
                                'private_key': self._private_key})
        if r.status_code == 200:
            response = r.json()
            self._token = response['token']
        else:
            return False

    def get_token(self):
        return self._token

    def get_headers(self):
        return {'Authorization': 'Bearer ' + self.get_token()}

    def authenticate_check(self):
        """
        Controleer of token nog geldig is 
        :return: True of False op basis van status code van de request
        """

        r = requests.post(self._base_url + "/authenticate/shelf/check",
                          headers=self.get_headers())
        if r.status_code == 200:
            return True
        else:
            return False

    def schoen_opgepakt(self):
        """
        Post call als de schoen is opgepakt
        :return: True of False op basis van status code van de request
        """

        r = requests.post(
            self._base_url + "/shelves/" + self.get_mac_address() + "/actions/picked_up",
            headers=self.get_headers())

        if r.status_code == 200:
            return True
        else:
            return False

    def maat_gescanned(self, uuid_tag):
        """
        Post call als een maat wordt gescanned
        :return: Geeft beschikbare maten terug indien succesvol, anders False
        """

        r = requests.post(
            self._base_url + "/shelves/" + self.get_mac_address() + "/tags/" + uuid_tag + "/actions/maat_gescanned",
            headers=self.get_headers())

        if r.status_code == 200:
            return r.json()
        else:
            return False

    def demo_gescanned(self, uuid_tag):
        """
        Post call als een maat wordt gescanned
        :return: Geeft beschikbare maten terug indien succesvol, anders False
        """

        r = requests.post(
            self._base_url + "/shelves/" + self.get_mac_address() + "/demos/" + uuid_tag + "/scanned",
            headers=self.get_headers())

        if r.status_code == 200:
            return r.json()
        else:
            return False

    def knop_ingedrukt(self, uuid_tag):
        """
        Post call als de knop is ingedrukt
        :return: True of False op basis van status code van de request
        """

        r = requests.post(
            self._base_url + "/shelves/" + self.get_mac_address() + "/tags/" + uuid_tag +
            "/actions/knop_ingedrukt", headers=self.get_headers())

        print(r.json())

        if r.status_code == 200:
            return True
        else:
            return False

    def get_shelf_information(self):
        """
        Vraag shelf informatie op 
        :return: Geeft demo model informatie terug indien succesvol, anders False
        """

        r = requests.get(
            self._base_url + "/shelves/" + self.get_mac_address(),
            headers=self.get_headers())

        if r.status_code == 200:
            return r.json()
        else:
            return False

    def kan_koppelen(self):
        """
        Vraag shelf informatie op 
        :return: Geeft demo model informatie terug indien succesvol, anders False
        """

        r = requests.get(self._base_url + "/settings/kan_koppelen",
                         headers=self.get_headers())
        if r.status_code == 200:
            return r.json()["data"]["value"]
        else:
            return False

    def set_mac_address(self):
        """
        Zet het mac_address van de shelf op basis van het mac_address van de Pi
        """
        mac_dec = get_mac()
        self._mac_address = "".join(c + ":" if i % 2 else c for i, c in
                                    enumerate(hex(mac_dec)[2:].zfill(12)))[
                            :-1]

    def get_mac_address(self):
        """
        Getter voor mac_address
        :return: Geef het mac_address terug 
        """
        return self._mac_address


def main():
    api = API("http://localhost:8000/api/", 'changeme')

    print(api.authenticate_check())
    print(api.schoen_opgepakt())
    print(api.get_shelf_information())
    print(api.kan_koppelen())


if __name__ == "__main__":
    main()
