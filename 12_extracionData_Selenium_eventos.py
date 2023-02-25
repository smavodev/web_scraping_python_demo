
import random
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# OBJETIVO:
#     - Extraer el precio y el título de los anuncios en la página de OLX.
#     - Aprender a utilizar la espera por eventos de Selenium.
#     - Aprender a optimizar el tiempo de ejecución de nuestras extracciones por Selenium de manera inteligente

# Instance el driver de selenium que va a controlar el navegador
# A partir de este objeto voy a realizar el web scraping e interacciones
driver = webdriver.Chrome('./chromedriver/chromedriver.exe') # REMPLAZA AQUI EL NOMBRE DE TU CHROME DRIVER

# Voy a la página que requiero
driver.get('https://www.olx.com.ar')


for i in range(3): # Voy a darle click en cargar mas 3 veces
    sleep(1) # Solución a bug extraño en carga inicial
    try:
        # Esperamos a que el botón se encuentre disponible a través de una espera por eventos
        # Espero un máximo de 10 segundos, hasta que se encuentre el botón dentro del DOM
        boton = WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.XPATH, '//button[@data-aut-id="btnLoadMore"]'))
        )
        # le doy clic al boton que espere
        boton.click()
        nAnuncios = 20 + (( i + 1 ) * 20 ) # 20 anuncios de carga inicial, y luego 20 anuncios por cada click que he dado
        # Espero hasta 10 segundos a que toda la información del último anuncio esté cargada
        WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.XPATH, '//li[@data-aut-id="itemBox"][' + str(nAnuncios) + ']'))
        )
        # Luego de que se hallan todos los elementos cargados, seguimos la ejecucion
    except Exception as e:
        print (e)
        # Si hay algún error, rompo el lazo. No me complico.
        break

# Encuentro cuál es el XPATH de cada elemento donde está la información que quiero extraer
# Esto es una LISTA. Por eso el método está en plural
autos = driver.find_elements('xpath', '//li[@data-aut-id="itemBox"]')

# Recorro cada uno de los anuncios que he encontrado
for auto in autos:
    # Por cada anuncio hallo el precio, que en esta pagina principal, rara vez suele no estar, por eso hacemos esta validacion.
    try:
      precio = auto.find_element('xpath', './/span[@data-aut-id="itemPrice"]').text
    except:
      precio = 'NO DISPONIBLE'
    print (precio)

    # Por cada anuncio hallo la descripcion
    descripcion = auto.find_element('xpath', './/span[@data-aut-id="itemTitle"]').text
    print (descripcion)

    location = auto.find_element('xpath', '.// span[@data-aut-id="item-location"]').text
    print(location)

# Existen mas eventos que yo puedo esperar (VER RECURSOS)