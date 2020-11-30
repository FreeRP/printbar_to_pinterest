import os
import shutil
from time import sleep
import atexit as _atexit
import requests

from pin_uploader import PinUploader
from printbar_parser import PrintbarParser
from tools.utils import load_json, get_logger


SAVED_IMAGES_DIR = 'imgs'

def parse_printbar_and_upload_to_pinterest(logger):
    account_data = load_json('config/account.json')
    board_and_url = load_json('config/board_data.json')
    settings = load_json('config/settings.json')

    printbar_parser = PrintbarParser(logger, settings['alias'], SAVED_IMAGES_DIR)
    pin_uploader = PinUploader(account_data, logger)

    for pinterest_board_name, printbar_catalog_url in board_and_url.items():
        board_id = pin_uploader.get_board_id(pinterest_board_name)
        products_data = printbar_parser.get_products_data(printbar_catalog_url)
        for name, price, image_path, printbar_url in products_data:
            try:
                pin_uploader.create_pin(board_id, name, price, image_path, printbar_url)
                print(f'pin created: {name}')
            except requests.exceptions.HTTPError as err:
                logger.exception(err)
                pin_uploader.logout()
                raise
            sleep(settings['pin_creating_period'])
        sleep(settings['board_creating_period'])

def remove_imgs_dir():
    shutil.rmtree(SAVED_IMAGES_DIR, ignore_errors=True)

def create_imgs_dir():
    if not os.path.isdir(SAVED_IMAGES_DIR):
        os.mkdir(SAVED_IMAGES_DIR)

if __name__ == "__main__":
    _atexit.register(remove_imgs_dir)
    create_imgs_dir()
    logger = get_logger('file.log', 'p2p')

    try:
        parse_printbar_and_upload_to_pinterest(logger)
    except Exception as err:
        logger.exception(f'unknow exception: {err}')