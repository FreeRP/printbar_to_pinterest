import requests
from bs4 import BeautifulSoup


class PrintbarParser:

    def __init__(self, logger, alias):
        self.__product_data = dict()
        self.__product_cntr = 0
        self.__alias = alias
        self.__logger = logger

    def get_html(self, url):
        user_agent = {'User-Agent':
        '''Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'''}
        response = requests.get(url, headers=user_agent)
        self.__logger.info(f'received html from {url}')
        return response.text

    def __get_catalog_html(self, html):
        try:
            return BeautifulSoup(html, 'lxml').\
                   find('main', class_='main__page').\
                   find('div', class_='pb__container').\
                   find('div', class_='pb__catalog--list-section').\
                   find_all('div', class_='pb__catalog--list-section')[-1]
        except AttributeError as err:
            self.__logger.exception(err)

    def __get_catalog_urls(self, catalog_html):
        try:
            links = catalog_html.find_all('a')
        except AttributeError as err:
            self.__logger.exception(err)
        self.__logger.info('received catalog urls')
        return [link.get('href') for link in links]

    @staticmethod
    def __get_img_attribute(html_soup, attribute):
        img_url = ''
        for tag in ('pb__product--mini-photo--list', 'tns6'):
            try:
                img_url = html_soup.find('div', tag).find('img').get(attribute)
            except AttributeError:
                continue
            else:
                break
        return img_url

    def __get_useful_data(self, html_soup):
        try:
            return html_soup.find('main', class_='main__page').\
                             find('div', class_='pb__container')
        except AttributeError as err:
            self.__logger.exception(err)

    def __get_description(self, html_soup):
        try:
            return html_soup.find('div', class_='pb__info--container-box pb__info--information')
        except AttributeError as err:
            self.__logger.exception(err)

    def __get_title(self, html_soup):
        return self.__get_img_attribute(html_soup, 'alt').\
                    replace('/','').replace('\\','').\
                    replace('?','').replace('*','')

    def __download_image(self, url, file_path):
        response = requests.get(url, stream=True)
        if response.ok:
            with open(file_path, 'wb') as file:
                file.write(response.content)
                self.__logger.info(f'{file_path} downloaded')

    @staticmethod
    def __get_price(html_soup):
        price_text = html_soup.find('span', class_='js-end-price').text.\
                     replace(' ','').replace('₽',' ₽').replace('ру',' ₽')
        return price_text[:price_text.find('или')]

    def __get_image_path(self, image_name, html_soup):
        url = self.__get_img_attribute(html_soup, 'data-full')
        file_path = f"imgs/{image_name.replace(' ','')}{self.__product_cntr}.jpg"
        self.__product_cntr += 1
        self.__download_image(url, file_path)
        return file_path

    def get_product_links(self, url):
        return self.__get_catalog_urls(
               self.__get_catalog_html(
               self.get_html(url)))

    def get_products_data(self, url):
        for product_url in self.get_product_links(url):
            html_soup = self.__get_useful_data(BeautifulSoup(self.get_html(product_url), 'lxml'))
            title = self.__get_title(html_soup)
            price = self.__get_price(html_soup)
            image_path = self.__get_image_path(title, html_soup)
            self.__logger.info(f'from {url} recived {product_url}, {price}, {image_path}')
            product_url = product_url.replace('printbar.ru', self.__alias)
            yield (title, price, image_path, product_url)
