from requests_html import HTMLSession

from script_for_site_3 import name_to_coords

session = HTMLSession()


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


print(get_data_for_one_shop(('/our-shops/voronezh-tts-galereya-chizhova/',
                             ' Россия, Воронеж, ул. Кольцовская, д. 35, ТЦ "Галерея Чижова", 1 этаж ')))
