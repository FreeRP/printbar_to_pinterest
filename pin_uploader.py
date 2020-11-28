import requests
from py3pin.Pinterest import Pinterest


class PinUploader:

    def __init__(self, cfg, logger):
        self.__cfg = cfg
        self.__pinterest = None
        self.__logger = logger
        self.__boards = None
        self.__create_obj()

    def __create_obj(self):
        self.__pinterest = Pinterest(email=self.__cfg['email'],
                                     password=self.__cfg['password'],
                                     username=self.__cfg['username'],
                                     cred_root=self.__cfg['cred_root'],
                                     user_agent=self.__cfg['user_agent'])
        self.__pinterest.login()
        self.__logger.info(f"{self.__cfg['username']} login")
        self.__boards = self.__pinterest.boards()

    def logout(self):
        self.__pinterest.logout()
        self.__logger.info(f"{self.__cfg['username']} logout")

    def __find_board_id(self, boardname):
        for board in self.__boards:
            if boardname == board['name']:
                return board['id']

    def get_board_id(self, boardname):
        response = None
        board_id = self.__find_board_id(boardname)
        if board_id:
            return board_id
        response = self.__pinterest.create_board(name=boardname)
        if response is not None:
            board_id = response.json()['resource_response']['data']['id']
            self.__logger.info("board {boardname} created")
            self.__boards.append({'name': boardname, 'id': board_id})
            return board_id
        else:
            self.__logger.error("can't create board '{boardname}'")
            return None

    def create_pin(self, board_id, title, price, image_path, printbar_url):
        description = '''Принт выдерживает неограниченное количество стирок.
                         Выберите тип ткани и вид печати.
                         Продукция будет готова через 48 часов.'''
        hashtag = title.replace(' ', ' #')
        try:
            self.__pinterest.upload_pin(board_id=board_id,
                                image_file=image_path,
                                description= f"Цена: {price}. {description} {hashtag}",
                                link=printbar_url,
                                title=title)
        except requests.exceptions.HTTPError:
            self.__logger.info('')
            self.__logger.error(f"can't create pin")
            raise RuntimeError("Error: can't create pin")
        else:
            self.__logger.info("pin created:\n" + log_msg)
