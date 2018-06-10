# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class MongoPipeline(object):

    items = {}

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.save_items()
        self.client.close()

    def save_items(self):
        for category in self.items.keys():
            for store in self.items[category]['store']:
                self.db[category].delete_many({'store': store})
            self.db[category].insert_many(self.items[category]['collections'])

    def add_item(self, item_dict):
        category = item_dict.get('category')
        if category in self.items:
            self.items[category]['store'].add(item_dict.get('store'))
            self.items[category]['collections'].append(item_dict)
        else:
            self.items[category] = {
                'store': set([item_dict.get('store')]),
                'collections': [item_dict]
            }

    def process_item(self, item, spider):
        self.add_item(dict(item))
        return item
