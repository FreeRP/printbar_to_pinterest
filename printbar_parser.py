import csv
import requests
from bs4 import BeautifulSoup
from time import sleep

from tool import load_json


class PrintbarParser:

    def __init__(self):
        self.__clothes_data = dict()
        self.__clothes_cntr = 0
        self.__proxies = {'http':"162.144.50.155:3838"}

    @staticmethod
    def get_html(url):
        user_agent = {'User-Agent':
        '''Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'''}
        response = requests.get(url, headers=user_agent)
        return response.text

    @staticmethod
    def __get_catalog_html(html):
        try:
            return BeautifulSoup(html, 'lxml').\
                   find('main', class_='main__page').\
                   find('div', class_='pb__container').\
                   find('div', class_='pb__catalog--list-section').\
                   find_all('div', class_='pb__catalog--list-section')[-1]
        except AttributeError as err:
            print(err)
            raise RuntimeError(err)

    @staticmethod
    def __get_catalog_urls(catalog_html):
        try:
            links = catalog_html.find_all('a')
        except AttributeError as err:
            print(err)
            raise RuntimeError(err)
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

    @staticmethod
    def __get_useful_data(html_soup):
        try:
            return html_soup.find('main', class_='main__page').\
                             find('div', class_='pb__container')
        except AttributeError as err:
            print(err)
            raise RuntimeError(err)

    @staticmethod
    def __get_description(html_soup):
        try:
            return html_soup.find('div', class_='pb__info--container-box pb__info--information')
        except AttributeError as err:
            print(err)
            raise RuntimeError(err)

    def __get_title(self, html_soup):
        return self.__get_img_attribute(html_soup, 'alt').\
                    replace('/','').replace('\\','').\
                    replace('?','').replace('*','')
    @staticmethod
    def __download_image(url, file_path):
        response = requests.get(url, stream=True)
        if response.ok:
            with open(file_path, 'wb') as f:
                f.write(response.content)

    @staticmethod
    def __get_price(html_soup):
        price_text = html_soup.find('span', class_='js-end-price').text.\
                     replace(' ','').replace('₽',' ₽').replace('ру',' ₽')
        return price_text[:price_text.find('или')]

    def __get_image_path(self, html_soup):
        url = self.__get_img_attribute(html_soup, 'data-full')
        img_name = f"{self.__clothes_data['title'].replace(' ','')}{self.__clothes_cntr}.jpg"
        file_path = f'''database/imgs/
            {self.__clothes_data['title'].replace(' ','')}{self.__clothes_cntr}.jpg'''
        self.__clothes_cntr += 1
        self.__download_image(url, file_path)
        return img_name

    def get_clothes_links(self, url):
        return self.__get_catalog_urls(
               self.__get_catalog_html(
               self.get_html(url)))

    def get_content_data(self, url)->dict:
        html_soup = self.__get_useful_data(BeautifulSoup(self.get_html(url), 'lxml'))
        self.__clothes_data['title'] = self.__get_title(html_soup)
        self.__clothes_data['price'] = self.__get_price(html_soup)
        self.__clothes_data['img_name'] = self.__get_image_path(html_soup)
        print(f'loaded: {self.__clothes_data["title"]}')
        return self.__clothes_data

def write_database(path, url):
    parser = PrintbarParser()
    with open(path, 'a', encoding='utf8') as db:
        writer = csv.DictWriter(db, fieldnames=['title', 'price', 'img_name'])
        content_links = parser.get_clothes_links(url)
        if len(content_links):
            for index in range(10):
                sleep(5)
                writer.writerow(parser.get_content_data(content_links[index]))
        else:
            print('ERROR: content_links is empty!')

def main():
    catalogs = [('database/russia.csv', 'https://printbar.ru/tovari/rossiya/'),
    	        ('database/animals.csv', 'https://printbar.ru/tovari/ghivotnye'),
    	        ('database/games.csv', 'https://printbar.ru/tovari/igry/')]
    for catalog in catalogs:
        write_database(*catalog)

if __name__ == '__main__':
    main()
