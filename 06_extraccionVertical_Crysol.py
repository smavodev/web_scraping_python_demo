from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader


# OBJETIVO:
#     - Extraer informacion sobre los hoteles de Guayaquil en https://www.crisol.com.pe/.
#     - Aprender a realizar extracciones verticales utilizando reglas
#     - Aprender a utilizar MapCompose para realizar limpieza de datos

class Hotel(Item):
    nombre = Field()
    autor = Field()  # El precio ahora carga dinamicamente. Por eso ahora obtenemos el score del hotel
    precio = Field()
    # amenities = Field()


# CLASE CORE - Al querer hacer extraccion de multiples paginas, heredamos de CrawlSpider
class Crisol(CrawlSpider):
    name = 'crisolLibros'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }

    # Reduce el espectro de busqueda de URLs. No nos podemos salir de los dominios de esta lista
    allowed_domains = ['crisol.com.pe']

    # Url semilla a la cual se hara el primer requerimiento
    start_urls = ['https://www.crisol.com.pe/los-mas-vendidos']

    # Tiempo de espera entre cada requerimiento. Nos ayuda a proteger nuestra IP.
    download_delay = 2

    # Tupla de reglas para direccionar el movimiento de nuestro Crawler a traves de las paginas
    rules = (
        Rule(  # Regla de movimiento VERTICAL hacia el detalle de los hoteles
            LinkExtractor(
                allow=r'/libro-'  # Si la URL contiene este patron, haz un requerimiento a esa URL
            ), follow=True, callback="parse_crisol"
        ),  # El callback es el nombre de la funcion que se va a llamar con la respuesta al requerimiento hacia estas URLs
    )

    # Callback de la regla
    def parse_crisol(self, response):
        sel = Selector(response)

        item = ItemLoader(Hotel(), sel)
        item.add_xpath('nombre', '//h1/span[@class="base"]/text()')  # $x('//h1/span[@class="base"]/text()') .map(x => x.value)
        item.add_xpath('autor', '//div[@class="author"]/span/text()')  # $x('//div[@class="product-info-price"]/div/span/span/span/text()')
        item.add_xpath('precio', '//div[@class="product-info-price"]/div/span/span/span/text()')  # $x('//div[@class="product-info-main"]/div[@class="product-info-price"]/div/span/span/span/text()')

        yield item.load_item()

# EJECUCION
# scrapy runspider 06_extracionVertical_Crysol.py -o crisol_scraping_vertical.csv
