# -*- coding: utf-8 -*-
"""
Spyder Editor

Obtención de datos
"""

import scrapy
from scrapy.loader import ItemLoader
from metro.items import LightMetroItem

# 
# Definimos la clase LineasSpider que se invoca desde el root del proyecto Spider mediante la 
# abreviación "lineas_ML".
# 
class MLLineasSpider(scrapy.Spider):
    name = "lineas_ML"
    
	# Comenzamos desde el enlace que contiene la lista de lineas de Metro Ligero.
    start_urls = [
        'https://www.crtm.es/tu-transporte-publico/metro-ligero/lineas.aspx',
    ]
    
#
# Definimos la función parse que recorrerá todas las estaciones de una línea partiendo 
# de la URL de la linea 1. La función luego sigue enlaces a siguientes lineas 
# construyendo sus enlaces a partir de la URL de Linea 1
#
    def parse(self, response):

        lines_list = response.xpath('//*[@id="colCentro"]/div[3]/ul/li/a/@href').extract()

	# Itera por la lineas procesando cada linea mediante la función parse_line
        for i in lines_list:
            print(i)
            yield response.follow(i, self.parse_line)
        
#
# Definimos la función parse_line procesa la info de cada linea y llama a la función 
# parse_station para procesar la info de cada estación
#
    def parse_line(self, response):

        station_seq = 0
        item_ML = LightMetroItem()

        stations_list = response.xpath('//*[@id="colCentro"]/div[3]/div[1]/table/tbody/tr/td[1]/a/@href').extract()

	# Se pasan los datos de la línea en curso mediante metadatos
        for i in stations_list:
        #for i in stations_list[1:3]:
            station_seq += 1
            item_ML['line'] = response.xpath('//*[@id="colCentro"]/div[2]/h3/span/text()').extract()
            item_ML['station_sequence'] = station_seq
            item_ML['stop_url'] = i
            request = scrapy.Request(response.urljoin(i), callback = self.parse_station)
            request.meta['item_ML'] = item_ML.copy()
            yield request

            
# 
# Definimos la función de procesado de estación donde creamos el diccionario basado en la definición del 
# fichero items.py.
#
    def parse_station(self, response):

        item_ML = response.meta['item_ML']
       
        yield{
            'line': item_ML['line'],
            'station_sequence': item_ML['station_sequence'],
            'stop_url': item_ML['stop_url'],
            'stop_name': response.xpath('//*[@id="divMigas"]/ol/li[5]/text()').extract_first(),
            'elevator': 'Yes' if response.xpath('//*[@id="colCentro"]/div[4]/div[2]/ul/li[1]/span/img/@alt[contains(.,"ascensor")]').extract()
                                else 'No',
            'escalator': 'Yes' if response.xpath('//*[@id="colCentro"]/div[4]/div[2]/ul/li[1]/span/img/@alt[contains(.,"escaleras")]').extract()
                                else 'No'
            }
        
