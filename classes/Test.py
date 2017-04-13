from dotenv import load_dotenv, find_dotenv
import os


class Test:

    def __init__(self) -> None:
        load_dotenv(find_dotenv())
        print(os.environ.get("BASE_URL"))


def main() -> None:
    test = Test()

if __name__ == '__main__':
    main()
