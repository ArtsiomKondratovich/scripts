from requests_html import HTMLSession
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
import lxml

session = HTMLSession()

URL = "https://oriencoop.cl/sucursales.htm"

response = session.get(url=URL)
response.html.render(sleep=5)


def name_to_coords(name: str) -> list:
    geolocator = Nominatim(user_agent="script_for_site_1")
    location = geolocator.geocode(name)
    return [location.latitude, location.longitude]


list_of_departments = []  # list =[(links, name), ...]

departments = response.html.find(".sub-menu")
soup_of_departments = BeautifulSoup(departments, 'lxml').find_all('a')
print(soup_of_departments)




# data = response.html.find(".s-dato")
# data = BeautifulSoup(data[0].html, 'lxml').find_all('p')
# name = BeautifulSoup(data[0].html, 'lxml').find('h3')

