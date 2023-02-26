# -*- coding: utf-8 -*-

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# OBJETIVO: - Extraer el precio, título y descripción de productos en Mercado Libre. - Aprender a realizar
# extracciones verticales y horizontales con Selenium. - Demostrar que Selenium no es óptimo para realizar
# extracciones que requieren atravesar mucho a través de varias páginas de una web - Aprender a manejar el "retroceso"
# del navegador - Aprender a definir user_agents en Selenium

website = 'https://listado.mercadolibre.com.ec/herramientas-vehiculos/'
path = './chromedriver/chromedriver.exe'  # REMPLAZA AQUÍ EL NOMBRE DE TU CHROME DRIVER

opts = Options()
opts.headless = True
# Definimos el User Agent en Selenium utilizando la clase Options
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")
opts_service = Service(executable_path=path)
driver = webdriver.Chrome(service=opts_service, options=opts)

# URL SEMILLA
driver.get(website)

# LOGICA DE MAXIMA PAGINACIÓN CON LAZO WHILE
# VECES VOY A PAGINAR HASTA UN MÁXIMO DE 10
PAGINACION_MAX = 2
PAGINACION_ACTUAL = 1

sleep(3)  # Esperar a que todo cargue correctamente

# Debemos darle click al botón de disclaimer para que no interrumpa nuestras acciones
try:  # Encerramos todo en un try catch para que si no aparece el discilamer, no se caiga el codigo
    disclaimer = driver.find_element(By.XPATH, '//button[@data-testid="action:understood-button"]')
    disclaimer.click()  # lo obtenemos y le damos clic
except Exception as e:
    print(e)
    None

# Mientras la página en la que me encuentre, sea menor que la maxima página que voy a sacar... sigo ejecutando...
while PAGINACION_MAX > PAGINACION_ACTUAL:

    links_productos = driver.find_elements(By.XPATH, '//a[@class="ui-search-item__group__element shops__items-group-details ui-search-link"]')
    links_de_la_pagina = []
    for a_link in links_productos:
        links_de_la_pagina.append(a_link.get_attribute("href"))

    # Q: Pero leaonrdo, porque no hiciste for link in link_productos, y simplemente ibas y volvias haciendo click en el contenedor que me lleva a la otra pagina?
    # A: Porque al yo irme y volver, pierdo la referencia de links_productos que tuve inicialmente. Y selenium me daria error porque le intentaria dar click a algo que no existe en el DOM actual.
    # Es por esto que, la mejor estrategia es obtener todos los links como cadenas de texto y luego iterarlos.

    for link in links_de_la_pagina:
        sleep(2)  # Prevenir el baneo de nuestra IP
        try:
            # Voy a cada uno de los links de los detalles de los productos
            driver.get(link)

            # Rara vez da error si no utilizamos una espera por eventos:
            # precio_element = WebDriverWait(driver, 10).until(
            #   EC.presence_of_element_located((By.XPATH, '//span[contains(@class,"price-tag")]'))
            # )
            titulo = driver.find_element(By.XPATH, '//h1').text
            precio = driver.find_element(By.XPATH, '//span[contains(@class,"ui-pdp-price")]/span[@class="andes-money-amount__fraction"]').text
            imagen = driver.find_element(By.XPATH, '//figure[@class="ui-pdp-gallery__figure"]/img').get_attribute('src')
            # preprecio = precio.replace('\n', '').replace('\t', '')
            print(titulo + "|" + "U$S" + precio + "|" + imagen)

            # Aplasto el botón de retroceso
            driver.back()
        except Exception as e:
            print(e)
            # Si sucede algún error dentro del detalle, no me complico. Regreso a la lista y sigo con otro producto.
            driver.back()

    # Logica de detección de fin de paginación
    try:
        # Intento obtener el botón de SIGUIENTE y le intento dar clic
        puedo_seguir_horizontal = driver.find_element(By.XPATH, '//span[text()="Siguiente"]')
        puedo_seguir_horizontal.click()
    except:
        # Si obtengo un error al intentar darle clic al botón, quiere decir que no existe
        # Lo cual me indica que ya no puedo seguir paginando, termina el While
        break

    PAGINACION_ACTUAL += 1
