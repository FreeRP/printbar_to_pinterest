import csv
import requests
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

    def get_board_id(self, boardname):
        response = None
        try:
            response = self.__pinterest.create_board(name=boardname)
        except requests.exceptions.HTTPError as err:
            return None
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

if __name__ == "__main__":
    user_info = load_json('config/login.json')
    pinterest = PinUploader(user_info)
    pinterest.login()
    pinterest.create_pins(load_json('config/board_data.json'))
    pinterest.logout()
