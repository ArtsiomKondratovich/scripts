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


def re_phone(string: str):
    string = string.split(':')[1:]
    result = []
    for i in string:
        result.append(re.sub(r'\D', '', i))
    return result


def get_data_for_one_shop(one_shop: tuple) -> dict:
    base_url = 'https://naturasiberica.ru'
    link = one_shop[0]
    result_dict = {}
    response = session.get(url=f'{base_url}{link}')
    response.html.render(sleep=3)
    raw_phones: str = response.html.find('.original-shops__phone', first=True).text
    working_time = response.html.find('.original-shops__schedule', first=True).text
    address = one_shop[1]
    result_dict["address"] = address
    result_dict["latlon"] = name_to_coords(address)
    result_dict["name"] = 'Natura Siberica'
    result_dict["phones"] = re_phone(raw_phones)
    result_dict["working_hours"] = [working_time]
    return result_dict


def main():
    list_of_all_shops = get_list_of_all_shops()
    result = []
    for one_shop in list_of_all_shops:
        result.append(get_data_for_one_shop(one_shop))
    return result


if __name__ == '__main__':
    session = HTMLSession()
    print(main())
