import requests
from bs4 import BeautifulSoup

# OBJETIVO:
#   - Extraer las preguntas de la pagina principal de Stackoverflow
#   - Aprender a utilizar Beautiful Soup para parsear el arbol HTML

# USER AGENT PARA PROTEGERNOS DE BANEOS
encabezados = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}

# URL SEMILLA
url = 'https://stackoverflow.com/questions'

# REQUERIMIENTO AL SERVIDOR
respuesta = requests.get(url, headers=encabezados)

# PARSEO DEL ARBOL CON BEAUTIFUL SOUP
soup = BeautifulSoup(respuesta.text, features="lxml")
# ENCONTRAR UN ELEMENTO POR ID
contenedor_de_preguntas = soup.find(id='questions')
# ENCONTRAR VARIOS ELEMENTOS POR TAG Y POR CLASE
lista_de_preguntas = contenedor_de_preguntas.find_all('div',class_="s-post-summary")

# ITERAR ELEMENTO POR ELEMENTO
for pregunta in lista_de_preguntas:
    # METODO #1: METODO TRADICIONAL
    texto_pregunta = pregunta.find('h3').text # DENTRO DE CADA ELEMENTO ITERADO ENCONTRAR UN TAG
    descripcion_pregunta = pregunta.find(class_='s-post-summary--content-excerpt').text # ENCONTRAR POR CLASE
    descripcion_pregunta = descripcion_pregunta.replace('\n', '').replace('\r', '').strip() # LIMPIEZA DE TEXTO
    print(texto_pregunta)
    print(descripcion_pregunta)


for pregunta2 in lista_de_preguntas:
    # METODO #2: APROVECHANDO EL PODER COMPLETO DE BEAUTIFUL SOUP
    contenedor_pregunta = pregunta2.find('h3')
    texto_pregunta2 = contenedor_pregunta.text
    descripcion_pregunta2 = contenedor_pregunta.find_next_sibling('div')  # TRAVERSANDO EL ARBOL DE UNA MENERA DIFERENTE
    texto_descripcion_pregunta = descripcion_pregunta2.text

    texto_descripcion_pregunta = texto_descripcion_pregunta.replace('\n', '').replace('\t', '').strip()
    print(texto_pregunta2)
    print(texto_descripcion_pregunta)