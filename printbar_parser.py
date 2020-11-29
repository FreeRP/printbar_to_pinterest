import requests
from bs4 import BeautifulSoup


class PrintbarParser:

    def __init__(self, logger, alias, imgs_dir):
        self.__product_data = dict()
        self.__product_counter = 0
        self.__alias = alias
        self.__logger = logger
        self.__imgs_dir = imgs_dir

    def get_html(self, url: str)->str:
        user_agent = {'User-Agent':
        '''Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'''}
        response = requests.get(url, headers=user_agent)
        self.__logger.info(f'received html from {url}')
        return response.text

    def __get_catalog_html(self, html: str)->str:
        try:
            return BeautifulSoup(html, 'lxml').\
                   find('main', class_='main__page').\
                   find('div', class_='pb__container').\
                   find('div', class_='pb__catalog--list-section').\
                   find_all('div', class_='pb__catalog--list-section')[-1]
        except AttributeError as err:
            self.__logger.exception(err)

    def __get_catalog_urls(self, html_bs4: BeautifulSoup)->list:
        try:
            links = html_bs4.find_all('a')
        except AttributeError as err:
            self.__logger.exception(err)
        self.__logger.info('received catalog urls')
        return [link.get('href') for link in links]

    @staticmethod
    def __get_img_attribute(html_bs4: BeautifulSoup, name:str)->str:
        attribute = ''
        for tag in ('pb__product--mini-photo--list', 'tns6'):
            try:
                attribute = html_bs4.find('div', tag).find('img').get(name)
            except AttributeError:
                continue
            else:
                break
        return attribute

    def __get_useful_data(self, html_bs4: BeautifulSoup)->str:
        try:
            return html_bs4.find('main', class_='main__page').\
                             find('div', class_='pb__container')
        except AttributeError as err:
            self.__logger.exception(err)

    def __get_description(self, html_bs4: BeautifulSoup)->str:
        try:
            return html_bs4.find('div', class_='pb__info--container-box pb__info--information')
        except AttributeError as err:
            self.__logger.exception(err)
            return ''

    def __get_title(self, html_bs4: BeautifulSoup)->str:
        title = self.__get_img_attribute(html_bs4, 'alt')
        for sym in ('/', '\\', '?', '*'):
            title = title.replace(sym, '')
        return title

    def __download_image(self, url: str, saved_img_path: str):
        response = requests.get(url, stream=True)
        if response.ok:
            with open(saved_img_path, 'wb') as file:
                file.write(response.content)
                self.__logger.info(f'{saved_img_path} downloaded')

    @staticmethod
    def __get_price(html_bs4: BeautifulSoup)->str:
        price = html_bs4.find('span', class_='js-end-price').text
        for key, val in {' ':'', '₽':' ₽', 'ру': ' ₽'}.items():
            price = price.replace(key, val)
        return price[:price.find('или')]

    def __get_image_path(self, image_name:str, html_bs4: BeautifulSoup)->str:
        url = self.__get_img_attribute(html_bs4, 'data-full')
        file_path = f"{self.__imgs_dir}/{image_name.replace(' ','')}{self.__product_counter}.jpg"
        self.__product_counter += 1
        self.__download_image(url, file_path)
        return file_path

    def get_product_links(self, url:str)->str:
        return self.__get_catalog_urls(
               self.__get_catalog_html(
               self.get_html(url)))

    def get_products_data(self, url:str):
        for product_url in self.get_product_links(url):
            html_bs4 = self.__get_useful_data(BeautifulSoup(self.get_html(product_url), 'lxml'))
            title = self.__get_title(html_bs4)
            price = self.__get_price(html_bs4)
            image_path = self.__get_image_path(title, html_bs4)
            self.__logger.info(f'from {url} recived {product_url}, {price}, {image_path}')
            product_url = product_url.replace('printbar.ru', self.__alias)
            yield (title, price, image_path, product_url)
