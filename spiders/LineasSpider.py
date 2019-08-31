# -*- coding: utf-8 -*-
"""
Spyder Editor

Obtención de datos
"""

import scrapy
import json
import codecs
from scrapy.loader import ItemLoader
from metro.items import MetroItem
import re

# 
# Definimos la clase LineasSpider que se invoca desde el root del proyecto Spider mediante la 
# abreviación "lineas".
# 
class LineasSpider(scrapy.Spider):
    name = "lineas"

   	# Comenzamos desde la URL de la primera línea de Metro Linea 1.
    start_urls = [
        'https://www.crtm.es/tu-transporte-publico/metro/lineas/4__1___.aspx',
    ]
   
#
# Definimos la función parse que recorrerá todas las estaciones de una línea partiendo 
# de la URL de la linea 1. La función luego sigue enlaces a siguientes lineas 
# construyendo sus enlaces a partir de la URL de Linea 1
#
    def parse(self, response):

        station_seq = 0
        item = MetroItem()

        stations_list = response.xpath('//*[@id="colCentro"]/div[3]/div[1]/table/tbody/tr/td[1]/a/@href').extract()

	# Itera por las estaciones.
        #for i in stations_list[1:2]:
        for i in stations_list:
            item['stop_url'] = i
            station_seq += 1
            item['station_sequence'] = station_seq
            line = response.url.split("__")[-2]
            if line == 'r':
                item['line'] = '13'
            else:            
                item['line'] = line
            request = scrapy.Request(response.urljoin(i), callback = self.parse_station)
            request.meta['item'] = item.copy()
            yield request
        
        # Sigue los enlaces a siguientes estaciones. Se pasan los datos de la línea en curso 
	# mediante metadatos
        line = response.url.split("__")[-2]
        if (line != '12' and line != 'r'):
            next_line = str(int(line)+1)
            href = '//*[@id="ContentPlaceHolderDefault_BodyContent_Metro_16_botonesLineas"]/ul/li[%s]/a/@href' % next_line
            url = response.xpath(href).extract_first()
        elif line == '12':
            url = 'https://www.crtm.es/tu-transporte-publico/metro/lineas/4__r___.aspx'
        else:       
            return

        if url is not None:
            yield response.follow(url, self.parse)
      

#
# Función para procesar la info de cada estación. Se construye un diccionario a partir de la 
# estructura definida en items.py.
#     
    def parse_station(self, response):

        item = response.meta['item']

        yield{
                'line': item['line'],
                'stop_name': response.xpath('//*[@id="divMigas"]/ol/li[5]/text()').extract_first(),
                'station_sequence': item['station_sequence'],
                'stop_url': item['stop_url'],
                'elevator': 'Yes' if response.xpath('//*[@id="colCentro"]/div[4]/div[2]/ul/li[1]/span/img/@alt[contains(.,"ascensor")]').extract()
                                    else 'No',
                'escalator': 'Yes' if response.xpath('//*[@id="colCentro"]/div[4]/div[2]/ul/li[1]/span/img/@alt[contains(.,"escaleras")]').extract()
                                    else 'No'
                
                }
