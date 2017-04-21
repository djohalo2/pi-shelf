import RPi.GPIO as GPIO
from pirc522 import RFID


class Reader:
    """
    Klasse om RFID stickers of tags uit te lezen op de Raspberry.
    """

    def __init__(self) -> None:
        """
        Code die wordt uitgevoerd bij het instantiëren van de klasse.
        """
        # Instantieer de RFID scanner.
        rfid = RFID()

        # Sla het op in een variabele.
        self._RFID = rfid

        # Sla de util op in een variabele.
        self._RFID_util = rfid.util()

        # uuid op de tag.
        self._uuid = ""

        # De huidige UUID.
        self._huidige_uuid = ""

        # Laatste UUID.
        self._laatste_uuid = ""

        # Fake gescanned
        self._fake_scanned = False

    def read(self) -> bool:
        """
        Lees de RFID scanner uit en sla de waarde op.
        """
        # Doe de request.
        (error, data) = self._RFID.request()

        # Verkrijg de UUID.
        (error, uuid) = self._RFID.anticoll()

        # Controleer of het goed gaat.
        if not error:

            # Sla de UUID op.
            self._uuid = '-'.join(str(uuid_part) for uuid_part in uuid)
            self._laatste_uuid = self._uuid

            # Geef terug dat het gelukt is.
            return True

        # Geef terug dat het niet gelukt is.
        return False

    def is_fake_scanned(self) -> bool:
        return self.fake_scanned

    def heeft_uuid(self) -> bool:
        """
        Geeft terug of de waarde van de uuid leeg is of niet.
        :return: Boolean op basis van bovenstaande vraag.
        """
        return not self._laatste_uuid == ""

    def reset(self) -> None:
        """
        
        :return: 
        """
        self.uuid = ""
        self.huidige_uuid = ""

    @property
    def fake_scanned(self) -> bool:
        """
        Getter voor fake_scanned

        :return: fake_pressed als boolean
        """
        return self._fake_scanned

    @property
    def huidige_uuid(self) -> str:
        """
        Getter voor fake_scanned

        :return: fake_pressed als boolean
        """
        return self._huidige_uuid

    @huidige_uuid.setter
    def huidige_uuid(self, value: str) -> None:
        """
        Setter voor fake_scanned.

        :param value: True of False
        """
        self._huidige_uuid = value

    @fake_scanned.setter
    def fake_scanned(self, value: bool) -> None:
        """
        Setter voor fake_scanned.

        :param value: True of False
        """
        self._fake_scanned = value

    @property
    def uuid(self) -> str:
        """
        Getter voor de uuid.

        :return: De uuid op de tag als string.
        """
        return self._uuid

    @uuid.setter
    def uuid(self, value: str) -> None:
        """
        Setter voor fake_scanned.

        :param value: True of False
        """
        self._uuid = value

    @property
    def laatste_uuid(self) -> str:
        """
        Getter voor de laatste uuid.

        :return: De uuid op de tag als string.
        """
        return self._laatste_uuid


def main() -> None:
    """
    Code om de klasse te testen, deze code wordt niet uitgevoerd als de
    klasse in een ander bestand wordt geimporteerd!
    """
    # Zet de pin mode op de Raspberry Pi.
    GPIO.setmode(GPIO.BOARD)

    # Maak een instantie aan van reader.
    reader = Reader()

    # Lees de reader uit.
    reader.read()

    # Print het uuid.
    print(reader.uuid)


# Zorg ervoor dat de main functie niet wordt uitgevoerd als de klasse
# wordt geimporteerd
if __name__ == '__main__':
    main()
