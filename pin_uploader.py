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

    def create_pin(self, board_id, title, price, image_path, printbar_url):
        description = '''Принт выдерживает неограниченное количество стирок.
                         Выберите тип ткани и вид печати.
                         Продукция будет готова через 48 часов.'''
        hashtag = title.replace(' ', ' #')
        self.__pinterest.upload_pin(board_id=board_id,
                            image_file=image_path,
                            description= f"Цена: {price}. {description} {hashtag}",
                            title=title,
                            link=printbar_url)

