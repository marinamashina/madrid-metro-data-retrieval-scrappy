# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MetroItem(scrapy.Item):
    # define the fields for your item here like:
    line = scrapy.Field()
    stop_name = scrapy.Field()
    station_sequence = scrapy.Field()
    stop_url = scrapy.Field()
    elevator = scrapy.Field()
    escalator = scrapy.Field()

class LightMetroItem(scrapy.Item):
    # define the fields for your item here like:
    line = scrapy.Field()
    stop_name = scrapy.Field()
    station_sequence = scrapy.Field()
    stop_url = scrapy.Field()
    elevator = scrapy.Field()
    escalator = scrapy.Field()
