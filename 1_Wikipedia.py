
import requests
from lxml import html

# OBJETIVOS:
#     - Extraer los idiomas de la pagina principal de WIKIPEDIA
#     - Aprender a utilizar requests para hacer requerimientos
#     - Aprender a utilizar lxml para parsear el arbol HTML

# USER AGENT PARA PROTEGERNOS DE BANEOS
encabezados = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}

# URL SEMILLA
url = 'https://www.wikipedia.org/'

# REQUERIMIENTO AL SERVIDOR
respuesta = requests.get(url, headers=encabezados)

# Codificar correctamente caracteres extranos
respuesta.encoding = 'utf-8'

# PARSEO DEL ARBOL HTML QUE RECIBO COMO RESPUESTA CON LXML
parser = html.fromstring(respuesta.text)

# ------------------------------------

# EXTRACCION DE IDIOMA INGLES
ingles1 = parser.get_element_by_id("js-link-box-en")
print(ingles1.text_content())

# ------------------------------------

# EXTRACCION SOLO DEL TEXTO QUE DICE INGLES
ingles2 = parser.xpath("//a[@id='js-link-box-en']/strong/text()")
print(ingles2)

# ------------------------------------

# EXTRACCION DE TODOS LOS IDIOMAS POR CLASE
idiomas3 = parser.find_class('central-featured-lang')
for idioma in idiomas3:
    print(idioma.text_content())

# ------------------------------------

# EXTRACCION DE TODOS LOS IDIOMAS POR XPATH
idiomas4 = parser.xpath("//div[contains(@class, 'central-featured-lang')]//strong/text()")
for idioma in idiomas4:
    print(idioma)

# ------------------------------------

