from time import sleep
import requests

from pin_uploader import PinUploader
from printbar_parser import PrintbarParser
from utils import load_json


def main():
    authorization_data = load_json('config/login.json')
    board_and_url = load_json('config/board_data.json')

    pin_uploader = PinUploader(authorization_data)
    pin_uploader.login()

    printbar_parser = PrintbarParser()
    for pinterest_board_name, printbar_catalog_url in board_and_url.items():
        board_id = pin_uploader.get_board_id(pinterest_board_name)
        products_data = printbar_parser.get_products_data(printbar_catalog_url['url'])
        for name, price, image_path, printbar_url in products_data:
            pin_uploader.create_pin(board_id, name, price, image_path, printbar_url)

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.HTTPError as err:
        print(err)