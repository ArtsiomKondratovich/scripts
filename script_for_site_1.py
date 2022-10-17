from requests_html import HTMLSession
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
import lxml


def name_to_coords(name: str) -> list:
    geolocator = Nominatim(user_agent="script_for_site_1")
    location = geolocator.geocode(name)
    return [location.latitude, location.longitude]


def get_all_departmets() -> list:
    URL = "https://oriencoop.cl/sucursales.htm"

    response = session.get(url=URL)
    response.html.render(sleep=1)
    list_of_departments = []  # list =[(links, name), ...]

    departments = response.html.find(".sub-menu")
    for i in departments:
        soup = BeautifulSoup(i.html, 'lxml').find('a')
        list_of_departments.append((soup.get('href'), soup.text))
    return list_of_departments


temp = [('/sucursales/79', 'Valparaíso'), ('/sucursales/127', 'Santiago'), ('/sucursales/165', 'San Fernando'),
        ('/sucursales/167', 'Cauquenes'), ('/sucursales/208', 'Los Ángeles'), ('/sucursales/231', 'Chillán'),
        ('/sucursales/267', 'Temuco'), ('/sucursales/312', 'Puerto Montt')]


def get_data_of_department(list_of_all_departmets: list) -> str:
    BASE_URL = 'https://oriencoop.cl'
    for i in temp:
        NAME = i[1]
        response = session.get(url=f'{BASE_URL}{i[0]}')
        response.html.render(sleep=5)
        raw_data = response.html.find('.s-dato', first=True)
        soup = BeautifulSoup(raw_data, 'lxml').find_all('p')
        print(soup)
    return '......'


if __name__ == '__main__':
    print('strat')
    session = HTMLSession()
    # print(get_all_departmets())
    get_data_of_department(temp)
