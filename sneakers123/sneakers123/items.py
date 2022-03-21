# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field
from scrapy.item import Item


class Sneakers123Item(Item):
    brand = Field()
    brand_division = Field()
    image_urls = Field()
    image_uris = Field()
    image_reference = Field()
    product_name = Field()
    model = Field()
    sku = Field()
    gender = Field()
    color = Field()
    date_added = Field()
    breadcrumbs = Field()
    url = Field()
    timestamp = Field()
    spider = Field()
    spider_version = Field()
