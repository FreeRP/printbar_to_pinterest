import csv
from time import sleep
from py3pin.Pinterest import Pinterest

from utils import load_json


class PinUploader:

    def __init__(self, cfg):
        self.__cfg = cfg
        self.__pinterest = None

    @staticmethod
    def __get_proxies():
        return {}

    def login(self):
        self.__pinterest = Pinterest(email=self.__cfg['email'],
                                     password=self.__cfg['password'],
                                     username=self.__cfg['username'],
                                     cred_root=self.__cfg['cred_root'])
        try:
            self.__pinterest.login()
        except:
            proxies = self.__get_proxies()
            self.__pinterest = Pinterest(email=self.__cfg['email'],
                                         password=self.__cfg['password'],
                                         username=self.__cfg['username'],
                                         cred_root=self.__cfg['cred_root'],
                                         proxies=proxies)

    def logout(self):
        self.__pinterest.logout()

    def __get_board_id(self, boardname):
        response = self.__pinterest.create_board(name=boardname)
        return response.json()['resource_response']['data']['id']

    def create_pin(self, board_id, name, price, image_path, printbar_url):
        description = '''Принт выдерживает неограниченное количество стирок.
                         Выберите тип ткани и вид печати.
                         Продукция будет готова через 48 часов.'''
        self.__pinterest.upload_pin(board_id=board_id,
                            image_file=row['image_path'],
                            description= f"Цена: {price}. {description} {hashtag}",
                            title=row['title'],
                            link=row['url'])

    def create_pins(self, board_data):
        for board_name, data in board_data.items():
            board_id = self.__get_board_id(board_name)
            self.__upload_pins_to_board(board_id, data['database'])
            sleep(50)

if __name__ == "__main__":
    user_info = load_json('config/login.json')
    pinterest = PinUploader(user_info)
    pinterest.login()
    pinterest.create_pins(load_json('config/board_data.json'))
    pinterest.logout()
