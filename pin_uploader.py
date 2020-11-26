from time import sleep
import requests
from py3pin.Pinterest import Pinterest


class PinUploader:

    def __init__(self, cfg, logger):
        self.__cfg = cfg
        self.__pinterest = None
        self.__logger = logger

    def login(self):
        self.__pinterest = Pinterest(email=self.__cfg['email'],
                                     password=self.__cfg['password'],
                                     username=self.__cfg['username'],
                                     cred_root=self.__cfg['cred_root'])
        self.__logger.info('logged in successfully')

    def logout(self):
        self.__pinterest.logout()
        self.__logger.info('log out')

    def get_board_id(self, boardname):
        response = None
        try:
            response = self.__pinterest.create_board(name=boardname)
        except requests.exceptions.HTTPError as err:
            self.__logger.exception(err)
        self.__logger.exception('board created')
        return response.json()['resource_response']['data']['id']

    def create_pin(self, board_id, title, price, image_path, printbar_url):
        description = '''Принт выдерживает неограниченное количество стирок.
                         Выберите тип ткани и вид печати.
                         Продукция будет готова через 48 часов.'''
        hashtag = title.replace(' ', ' #')
        self.__pinterest.pin(board_id=board_id,
                            image_url=image_path,
                            description= f"Цена: {price}. {description} {hashtag}",
                            title=title,
                            link=printbar_url)
        self.__logger.info('pin created')
