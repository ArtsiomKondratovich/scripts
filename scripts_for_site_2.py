import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
import lxml

session = HTMLSession()


def get_all_shops() -> list:
    base_url = 'https://som1.ru/shops/'
    list_of_all_shops = []
    response = session.get(url=base_url)
    response.html.render(wait=10, sleep=3)
    raw_data = response.html.find('.citys-box', first=True)
    ids_city = BeautifulSoup(raw_data.html, 'lxml').find_all('label')
    for city in ids_city:
        list_of_all_shops.append((city.get('id'), city.get_text()))
    return list_of_all_shops

def get_data_one_shop(one_shop_object: tuple):
    base_url = 'https://som1.ru/shops/'
    shop_id = one_shop_object[0]
    url=f'{base_url}{shop_id}'
    response = session.get(url=url)
    response.html.render(sleep=3)


print(get_data_one_shop(('3215', 'Богданович')))

# [('3215', 'Богданович'), ('3325', 'Заречный'), ('2015', 'Верхняя Салда')]