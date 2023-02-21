from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader


# OBJETIVO:
#     - Extraer informacion sobre los hoteles de Guayaquil en hhttp://books.toscrape.com/.
#     - Aprender a realizar extracciones verticales utilizando reglas
#     - Aprender a utilizar MapCompose para realizar limpieza de datos

class Datos(Item):
    imagen = Field()
    nombre = Field()
    # autor = Field()  # El precio ahora carga dinamicamente. Por eso ahora obtenemos el score del hotel
    precio = Field()
    status = Field()


# CLASE CORE - Al querer hacer extraccion de multiples paginas, heredamos de CrawlSpider
class Toscrape(CrawlSpider):
    name = 'topscrape'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }

    # Reduce el espectro de busqueda de URLs. No nos podemos salir de los dominios de esta lista
    allowed_domains = ['books.toscrape.com']

    # Url semilla a la cual se hara el primer requerimiento
    start_urls = ['http://books.toscrape.com/catalogue/category/books_1/index.html']

    # Tiempo de espera entre cada requerimiento. Nos ayuda a proteger nuestra IP.
    download_delay = 2

    # Tupla de reglas para direccionar el movimiento de nuestro Crawler a traves de las paginas
    rules = (
        Rule(  # Regla de movimiento VERTICAL hacia el detalle de los hoteles
            LinkExtractor(
                allow=r'/catalogue/'  # Si la URL contiene este patron, haz un requerimiento a esa URL
            ), follow=True, callback="parse_toscrape"
        ),  # El callback es el nombre de la funcion que se va a llamar con la respuesta al requerimiento hacia estas URLs
    )

    # Callback de la regla
    def parse_topscrape(self, response):
        sel = Selector(response)

        item = ItemLoader(Datos(), sel)
        item.add_xpath('imagen', '//img/@src')
        item.add_xpath('nombre', '//div/h1/text()')
        item.add_xpath('precio', '//p[@class="price_color"]/text()')
        item.add_xpath('status', '//p[@class="instock availability"]/text()')
        yield item.load_item()

# EJECUCION
# scrapy runspider 07_extracionVertical_libros.py -o toscrape_scraping_vertical.csv
