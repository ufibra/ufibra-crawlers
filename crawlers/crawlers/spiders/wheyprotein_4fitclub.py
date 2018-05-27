# -*- coding: utf-8 -*-
import scrapy

from crawlers.items import ProductItem
from crawlers.utils import parse, product_type

class Wheyprotein4fitclubSpider(scrapy.Spider):
    name = 'wheyprotein-4fitclub'
    store = '4fitclub'
    start_urls = ['http://www.4fitclub.com.br/whey-protein-s1000//']

    def parse(self, response):
        products = response.css('.products li')
        for product in products:
            yield self.parse_product(product)

        next_url = self.next_page(response)
        if next_url:
            yield scrapy.Request(url=next_url, callback=self.parse)

    def parse_product(self, product):
        name = product.css('.product-name ::text').extract_first()
        price = parse.parse_price(product.css('.price .sale ::text').extract_first())
        image = 'https://www.4fitclub.com.br' + product.css('.photo img::attr(data-src)').extract_first()
        weight = parse.parse_weight(name)
        item = self.to_item(store=self.store, name=name, price=price, image=image, weight=weight, category=product_type.WHEY_PROTEIN)
        return item

    def next_page(self, response):
        href = response.css(".page-number .page-next > a::attr('href')").extract_first()
        url = response.urljoin(href)
        return url if href else None

    def to_item(self, **kwargs):
        item = ProductItem()
        item['store'] = kwargs.get('store')
        item['name'] = kwargs.get('name')
        item['price'] = kwargs.get('price')
        item['image'] = kwargs.get('image')
        item['weight'] = kwargs.get('weight')
        item['category'] = kwargs.get('category')
        return item
