from .pin_uploader import PinUploader
from .printbar_parser import PrintbarParser
from .utils import load_json


def main():
  authorization_data = load_json('config/login.json')
  board_and_url = load_json('config/board_data.json')
  pin_uploader = PinUploader(authorization_data)
  printbar_parser = PrintbarParser()
  for pinterest_board_name, printbar_catalog_url in board_and_url.items():
    board_id = pin_uploader.get_board_id(pinterest_board_name)
    (name, price, image_path, printbar_url) = next(printbar_parser.get_product_data(
                                                   printbar_catalog_url))
    pin_uploader.create_pin(board_id, name, price, image_path, printbar_url)

if __name__ == "__main__":
  main()

