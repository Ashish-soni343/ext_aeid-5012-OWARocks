# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MdxMarketplaceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Feed_code = scrapy.Field()
    Site = scrapy.Field()
    Source_country = scrapy.Field()
    Record_create_by = scrapy.Field()
    Execution_id = scrapy.Field()
    Record_create_dt = scrapy.Field()
    file_create_dt = scrapy.Field()
    row = scrapy.Field()
    AEIDprojectId = scrapy.Field()
    datasetId = scrapy.Field()
    category_id = scrapy.Field()
    seller_id = scrapy.Field()
    seller_title = scrapy.Field()
    seller_url = scrapy.Field()
    product_name = scrapy.Field()
    format = scrapy.Field()
    delivery = scrapy.Field()
    frequency = scrapy.Field()
    description = scrapy.Field()
    region = scrapy.Field()
    category_name = scrapy.Field()
    history = scrapy.Field()
    price_raw = scrapy.Field()
    Data_Type = scrapy.Field()
    Data_Quality = scrapy.Field()
    Data_Source = scrapy.Field()
    Source = scrapy.Field()
    Data_Class = scrapy.Field()
    Asset_Class = scrapy.Field()
    pass
