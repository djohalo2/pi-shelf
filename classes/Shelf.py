from uuid import getnode as get_mac
import requests

class Shelf:

    def __init__(self):
        self.set_mac_address()
        print(self.get_mac_address())
        self.authenticate()
        print(self.get_token())


    def connect(self):
        print("connect")

    def authenticate(self):
        r = requests.post("https://ipmedt5.roddeltrein.nl/api/authenticate",
                          data={'email': 's1095067@student.hsleiden.nl', 'password': 'secret'})
        if(r.status_code == 200):
            response = r.json()
            self._token = response['token']
            return self._token
        else:
            return false

    def get_token(self):
        return self._token

    def authenticate_check(self):
        print("check")

    def set_mac_address(self):
        mac_dec = get_mac()
        self._mac_address = "".join(c + ":" if i % 2 else c for i, c in enumerate(hex(mac_dec)[2:].zfill(12)))[:-1]

    def get_mac_address(self):
        return self._mac_address

def main():
    print("main")


if __name__ == "__main__":
    main()
