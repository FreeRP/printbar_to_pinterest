from time import sleep
import requests

from pin_uploader import PinUploader
from printbar_parser import PrintbarParser
from utils import load_json, get_logger


def main():
    logger = get_logger('file.log', 'p2p')
    authorization_data = load_json('config/login.json')
    board_and_url = load_json('config/board_data.json')

    pin_uploader = PinUploader(authorization_data, logger)
    pin_uploader.login()

    printbar_parser = PrintbarParser(logger)
    for pinterest_board_name, printbar_url in board_and_url.items():
        board_id = pin_uploader.get_board_id(pinterest_board_name)
        products_data = printbar_parser.get_products_data(printbar_url['url'])
        for name, price, image_path, printbar_url in products_data:
            try:
                pin_uploader.create_pin(board_id, name, price, image_path, printbar_url)
            except requests.exceptions.HTTPError as err:
                logger.exception(err)
                pin_uploader.logout()
                raise RuntimeError('Error')
            except Exception as err:
                logger.exception(f'unknow exception: {err}')
                raise RuntimeError('Error')
            sleep(10)


if __name__ == "__main__":
    main()
