# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from os import environ, path

class MdxMarketplacePipeline:
    def process_item(self, item, spider):
        item["Execution_id"] = environ.get('SHUB_JOBKEY', None)

        return item
