import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
import lxml

from geopy import Nominatim
from googletrans import Translator

translator = Translator()


def get_list_of_all_shops() -> list:
    url = 'https://naturasiberica.ru/our-shops'
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml').find(class_='card-list').find_all('li')
    list_all_shops = []
    for i in soup:
        link = i.a.get('href')
        address = i.find(class_='card-list__description').get_text()
        address = re.sub(r'\s+', ' ', address).strip()
        list_all_shops.append((link, address))
    return list_all_shops


def name_to_coords(address: str) -> list:
    """
    Get coords of address
    :param address: "address"
    :return: [lat, lon]
    """
    geolocator = Nominatim(user_agent="script_for_site_1")
    address = translator.translate(address, src='ru', dest='en').text
    location = geolocator.geocode(address)
    if location is None:
        return name_to_coords(address.split(' ')[-1])
    return [location.latitude, location.longitude]


def get_data_for_one_shop(one_shop: tuple) -> dict:
    base_url = 'https://naturasiberica.ru'
    link = one_shop[0]
    result_dict = {}
    response = session.get(url=f'{base_url}{link}')
    r = response.html.render()
    # raw_phones: str = response.html.find('.original-shops__phone', first=True).text
    # raw_phones = raw_phones.split(':')[1]
    # phones = re.sub(r'[^0-9]', '', raw_phones)
    # print(phones)
    address = one_shop[1]
    print(address)
    result_dict["address"] = address
    result_dict["latlon"] = name_to_coords(address)
    result_dict["name"] = 'Natura Siberica'
    result_dict["phones"] = None
    result_dict["working_hours"] = None
    return result_dict


session = HTMLSession()

print(get_data_for_one_shop(('/our-shops/voronezh-tts-galereya-chizhova/',
                             ' Россия, Воронеж, ул. Кольцовская, д. 35, ТЦ "Галерея Чижова", 1 этаж ')))
