# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GzjsItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    price = scrapy.Field()
    salesVolume = scrapy.Field()
    pid = scrapy.Field()
    brand = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)


class CommentItem(scrapy.Item):
    pid = scrapy.Field()
    sentiment = scrapy.Field()
    keywords = scrapy.Field()
    summary = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)