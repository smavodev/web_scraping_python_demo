
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup

# OBJETIVO:
#     - Extraer informacion sobre los productos en la pagina de Mercado Libre monitores-accesorios
#     - Aprender a realizar extracciones verticales y horizontales utilizando reglas

class Articulo(Item):
    titulo = Field()
    precio = Field()
    descripcion = Field()

class MercadoLibreCrawler(CrawlSpider):
    name = 'mercadoLibre'

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 20
        # Numero maximo de paginas en las cuales voy a descargar items. Scrapy se cierra cuando alcanza este numero
    }

    # Utilizamos 2 dominios permitidos, ya que los articulos utilizan un dominio diferente
    allowed_domains = ['articulo.mercadolibre.com.ec', 'listado.mercadolibre.com.ec']

    start_urls = ['https://computacion.mercadolibre.com.ec/monitores-accesorios/']

    download_delay = 1

    # Tupla de reglas
    rules = (
        Rule( # REGLA #1 => HORIZONTALIDAD POR PAGINACION
            LinkExtractor(
                allow=r'/_Desde_\d+' # Patron en donde se utiliza "\d+", expresion que puede tomar el valor de cualquier combinacion de numeros
            ), follow=True),
        Rule( # REGLA #2 => VERTICALIDAD AL DETALLE DE LOS PRODUCTOS
            LinkExtractor(
                allow=r'/MEC-'
            ), follow=True, callback='parse_items'), # Al entrar al detalle de los productos, se llama al callback con la respuesta al requerimiento
    )

    def parse_items(self, response):
        item = ItemLoader(Articulo(), response)
        item.encoding = 'utf-8'

        # Utilizo Map Compose con funciones anonimas
        # PARA INVESTIGAR: Que son las funciones anonimas en Python?
        item.add_xpath('titulo', '//h1/text()', MapCompose(lambda i: i.replace('\n', ' ').replace('\r', ' ').strip()))
        item.add_xpath('descripcion', '//div[@class="ui-pdp-description"]/p/text()', MapCompose(lambda i: i.replace('\n', ' ').replace('\r', ' ').strip()))

        soup = BeautifulSoup(response.body)
        precio = soup.find(class_="andes-money-amount__fraction")
        precio_completo = precio.text.replace('\n', ' ').replace('\r', ' ').replace(' ', '') # texto de todos los hijos
        item.add_value('precio', precio_completo)

        yield item.load_item()


# EJECUCION
# scrapy runspider 08_extracion_Vertical_Horizontal_MercadoLibre.py -o mercado_libre_mixto.json -t json