from requests_html import HTMLSession
from bs4 import BeautifulSoup

session = HTMLSession()
temp = [('/sucursales/79', 'Valparaíso')]

BASE_URL = 'https://oriencoop.cl'
for i in temp:
    NAME = i[1]
    response = session.get(url=f'{BASE_URL}{i[0]}')
    response.html.render()
    raw_data = response.html.find('.s-dato', first=True)
    soup = BeautifulSoup(raw_data.html, 'lxml').find_all('p')
    for i in soup:
        print(i)
        print(i.strong.get_text(), i.span.get_text())
        for j in i.span:
            print(j)

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