from requests_html import HTMLSession
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
import regex


def name_to_coords(name: str) -> list:
    """
    Get coords of address
    :param name: "address"
    :return: [lat, lon]
    """
    geolocator = Nominatim(user_agent="script_for_site_1")
    location = geolocator.geocode(name)
    if location is None:
        return name_to_coords(name.split(' ')[-1])
    return [location.latitude, location.longitude]


def get_all_departmets() -> list:
    """
    Get list of all departmets and short links
    :return: list[(links, names_of_depart),...}
    """
    url = "https://oriencoop.cl/sucursales.htm"
    list_of_departments = []  # list =[(links, name), ...]
    try:

        response = session.get(url=url)
        response.html.render(sleep=5)  # sleep need for render JS
        departments = response.html.find(".sub-menu")
        for i in departments:
            soup = BeautifulSoup(i.html, 'lxml').find_all('a')
            for j in soup:
                list_of_departments.append((j.get('href'), j.text))
        return list_of_departments
    except Exception:

        print('Error in def get_all_departments! Restart')
        return get_all_departmets()


def reg_for_date(raw_list: list) -> list:
    """
    Regular exp for search work time in str
    :param raw_list: list['str',...]
    :return: list[f'str',...]
    """
    reg = r'\d{1,2}\.\d{1,2}'
    new = []
    for i in raw_list:
        new.append(regex.findall(reg, i))
    working = [f"mon-thu {new[0][0]}-{new[0][1]} {new[1][0]}-{new[1][1]}",
               f"fri {new[0][0]}-{new[0][1]} {new[1][0]}-{new[1][-1]} "]
    return working


def get_data_of_department(one_object_at_list_derarp: list or tuple) -> dict:
    """
    Get data about one department
    :param one_object_at_list_derarp: tuple()
    :return: dict{
            "address": address,
            "latlon": latitude, lon,
            "name": name of depart,
            "phones": phones,
            "working_hours": work_hours
    }
    """
    base_url = 'https://oriencoop.cl'
    try:
        # for one_depart in one_object_at_list_derarp:
        # try:
        response = session.get(url=f'{base_url}{one_object_at_list_derarp[0]}')
        response.html.render(wait=1)

        raw_data = response.html.find('.s-dato', first=True)
        soup = BeautifulSoup(raw_data.html, 'lxml').find_all('p')  # list of tag 'p'

        address: str = soup[0].get_text().split(':')[1].strip('\n').lstrip('\n')

        loc: list = name_to_coords(address)

        name: str = BeautifulSoup(raw_data.html, 'lxml').find('h3').get_text()

        phones: list = [i.strip('\n').lstrip('\n') for i in soup[1].get_text().split(':')[1:]]

        work_hours_list = soup[3].find_all_next('span')
        work_hours_list = [i.get_text() for i in work_hours_list]
        work_hours = reg_for_date(work_hours_list)

        result_dict_for_one: dict = {
            "address": address,
            "latlon": loc,
            "name": name,
            "phones": phones,
            "working_hours": work_hours
        }
        print(result_dict_for_one)
        # del one_object_at_list_derarp[0]
        # print(list_of_all_departmets)
        return result_dict_for_one

    except Exception:
        print('error')
        # print(f'restart with {one_object_at_list_derarp[0][1]}')
        get_data_of_department(one_object_at_list_derarp)


def main():
    result = []
    list_all_dep = get_all_departmets()
    for dep in list_all_dep:
        res = get_data_of_department(dep)
        result.append(res)


if __name__ == '__main__':
    session = HTMLSession()
    main()
