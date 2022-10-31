# Importing required libraries
import scrapy
import json
import datetime

from os import environ
from ..items import MdxMarketplaceItem
class MdxSpider(scrapy.Spider):
    name = 'AEID-4666_mdxtechnology'
    start_url = 'https://app.mdxtechnology.com/graphql'
    # Mandatory data
    # AEID_project_id = ''
    site = 'https://app.mdxtechnology.com/catalogue/products'
    source_country = 'Global'
    context_identifier = ''
    file_create_dt = datetime.datetime.utcnow().strftime('%Y-%m-%d %T')[0:10]
    record_created_by = ""
    execution_id = "622153"  # This will be taken automatically from zyte, for now this is hardcoded
    feed_code = "AEID-4666"
    type = ""
    row = 0

    # settings for Crawling
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'CONCURRENT_REQUESTS': 20,
        'COOKIES_ENABLED': False,
        'COOKIES_DEBUG': False,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 500,
        'DOWNLOAD_DELAY': 0,
        'AUTOTHROTTLE_ENABLED': False,
        'DOWNLOAD_TIMEOUT': 20,
        'DUPEFILTER_DEBUG': True,
    }
    # Function to call start url
    def start_requests(self):
        headers = {
            'accept': '* / *',
            'content-type': 'application/json',
            }
        payload = {"query": "query ($params: JSON) {\n  searchProducts(params: $params) {\n    products {\n      id\n      name\n      excerpt\n      is_hidden\n      has_sample\n      provider {\n        id\n        name\n        logo_url\n        is_hidden\n        __typename\n      }\n      __typename\n    }\n    buckets\n    __typename\n  }\n}\n",
                   "variables": {"params": {}}}
        yield scrapy.Request(self.start_url, method="POST", headers = headers, body=json.dumps(payload), callback=self.parse)

    # function to call product url
    def parse(self, response):
        # To convert response in JSON format
        data = json.loads(response.text)
        product = data["data"]['searchProducts']['products']
        for i in product:
            print("id====", i['id'])
            headers = {
                'accept': '* / *',
                'content-type': 'application/json',
            }
            payload = {"query": "query ($id: String!) {\n  product(id: $id) {\n    id\n    name\n    permission\n    description\n    data_dictionary\n    accessRequest {\n      id\n      __typename\n    }\n    subscription(expired: false) {\n      id\n      __typename\n    }\n    provider {\n      id\n      name\n      logo_url\n      __typename\n    }\n    pages {\n      id\n      name\n      ppd_tag\n      __typename\n    }\n    related_products {\n      id\n      name\n      __typename\n    }\n    sample {\n      id\n      accessRequest {\n        id\n        __typename\n      }\n      subscription(expired: false) {\n        id\n        __typename\n      }\n      downloads {\n        id\n        name\n        type\n        __typename\n      }\n      pages {\n        id\n        name\n        ppd_tag\n        __typename\n      }\n      __typename\n    }\n    facet_values {\n      id\n      label\n      facet {\n        name\n        is_multi\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
                        "variables": {"id": i['id']}}
            yield scrapy.Request(self.start_url, method="POST", headers=headers, body=json.dumps(payload), callback=self.parse_details)

    # Function to process data
    def parse_details(self, response):
        self.row += 1
        # To convert response in JSON format
        data = json.loads(response.text)
        product = data["data"]
        print("product------", product)
        region = []
        cat_name = ""
        data_quality = ""
        dat_source = ""
        Asset_Class = ""
        data_id = ""
        Data_Type = ""
        # To store data in items.py
        item = MdxMarketplaceItem()
        # loop to salect data and allocate then to specific item fields
        for i in data["data"]['product']['facet_values']:
            if i['facet']['name'] == 'Data Quality':
                data_quality = i['label']
            if i['facet']['name'] == 'Region':
                region.append(i['label'])
            if i['facet']['name'] == 'Data Class':
                cat_name = i['label']
            if i['facet']['name'] == 'Data Source':
                dat_source = i['label']
            if i['facet']['name'] == 'Asset Class':
                Asset_Class = i['label']
            if i['facet']['name'] == 'Data Type':
                Data_Type = i['label']
                data_id = i['id']

        item["Feed_code"] = self.feed_code
        item["Site"] = self.site
        item["Source_country"] = self.source_country
        item["Record_create_by"] = self.name
        item['Execution_id'] = environ.get('SHUB_JOBKEY', None)
        #item["Execution_id"] = self.execution_id
        item["Record_create_dt"] = datetime.datetime.utcnow().strftime('%Y-%m-%d %T')
        item['file_create_dt'] = self.file_create_dt
        item['AEIDprojectId'] = "AEID-4666"
        item['datasetId'] = data["data"]['product']['id']
        item['row'] = self.row
        item['category_id'] = data_id
        item['seller_id'] = data["data"]['product']['provider']['id'] + '-' + (data["data"]['product']['provider']['name']).lower().replace(" ", "-")
        item['seller_title'] = data["data"]['product']['provider']['name']
        item['seller_url'] = 'https://app.mdxtechnology.com/catalogue/providers/' + data["data"]['product']['provider']['id'] + '-' + (data["data"]['product']['provider']['name']).lower().replace(" ", "-")
        item['product_name'] = data["data"]['product']['name']
        item['format'] = data_quality
        item['delivery'] = data_quality
        item['frequency'] = ""
        description = data["data"]['product']['description']
        omit = ['<h3>', 'alt="', '<=""', '<br>', '<="', '">', '<p>', '</p>', '</h3>', '<li>', '</li>', '<ul>', '</ul>', '<a href="', '</a>', '<strong>', '</strong>', '<br />', '&bull;', '&#x26;', 'img src', 'alt=""', '" alt="', '/>']
        for i in omit:
            if i == '">':
                description = description.replace(i, " ")
            else:
                description = description.replace(i,"")
        item['description'] = description
        item['region'] = region
        item['category_name'] = Data_Type
        item['history'] = ""
        item['price_raw'] = ""
        item['Data_Type'] = Data_Type
        item['Data_Quality'] = data_quality
        item['Data_Source'] = dat_source
        item['Data_Class'] = cat_name
        item['Asset_Class'] = Asset_Class
        item['Source'] = 'https://app.mdxtechnology.com/catalogue/products/' + data["data"]['product']['id'] + '-' + (data["data"]['product']['name']).lower().replace(" ", "-")
        yield item

