from requests_html import HTMLSession
from bs4 import BeautifulSoup

from script_for_site_1 import name_to_coords

session = HTMLSession()
temp = [('/sucursales/79', 'Valparaíso')]

BASE_URL = 'https://oriencoop.cl'
for one_object_soup in temp:
    result_dict_for_one = {
        "address": str(address),
        "latlaon": name_to_coords(address),
        "name": one_object_soup[one_object_soup[1]],
    }

    response = session.get(url=f'{BASE_URL}{one_object_soup[0]}')
    response.html.render()
    raw_data = response.html.find('.s-dato', first=True)
    soup = BeautifulSoup(raw_data.html, 'lxml').find_all('p')
    for one_object_soup in soup:
        address = one_object_soup.span.get_text()
        for include_object_in_one_object in one_object_soup.span:
            print(include_object_in_one_object)

"""<p>
<strong>Dirección:</strong><br/>
<span>Esmeralda 940 L.4 - Valparaíso</span>
</p>, <p>
<strong>Teléfono:</strong><br/>
<span>71-2201096</span>
</p>, <p>
<strong>Agente:</strong><br/>
<span> </span>
</p>, <p>
<strong>Horarios:</strong><br/>
<span><img src="/resources/img/li.png"/> Mañana: 08.50 a 14.10 hrs.</span><br/>
<span><img src="/resources/img/li.png"/> Tarde: 15.00 a 17.10 horas (L a J) / Hasta 16.10 horas (V)</span>
</p>"""