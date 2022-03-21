from schematics.models import Model
from schematics.types import URLType, StringType, ListType, DateTimeType

class Sneakers123Item(Model):
    brand = StringType()
    brand_division = StringType()
    image_urls = ListType(URLType)
    image_uris = ListType(StringType)
    image_reference = StringType()
    product_name = StringType()
    model = StringType()
    sku = StringType(required=True)
    gender = ListType(StringType)
    color = ListType(StringType)
    date_added = StringType()
    breadcrumbs = ListType(StringType)
    url = URLType()
    timestamp = DateTimeType()
    spider = StringType()
    spider_version = StringType()
