# -*- coding: utf-8 -*-
import scrapy

from crawlers.items import ProductItem
from crawlers.utils import parse, product_type

class Wheyprotein4fitclubSpider(scrapy.Spider):
    name = 'wheyprotein-4fitclub'
    store = '4fitclub'
    start_urls = ['https://www.4fitclub.com.br/massa-muscular/whey-protein-proteina-cat.html']

    def parse(self, response):
        products = response.css('.products-grid .item')
        for product in products:
            yield self.parse_product(product)

        next_url = self.next_page(response)
        if next_url:
            yield scrapy.Request(url=next_url, callback=self.parse)

    def parse_product(self, product):
        name = product.css('.product-name a ::text').extract_first()
        price = parse.parse_price(product.css('.price ::text').extract_first())
        image = product.css('.product-image img::attr(src)').extract_first()
        weight = parse.parse_weight(name)
        url = product.css('.product-image ::attr(href)').extract_first()
        item = self.to_item(store=self.store, name=name, price=price, image=image, weight=weight, url=url, category=product_type.WHEY_PROTEIN)
        return item

    def next_page(self, response):
        href = response.css(".pages a.i-next::attr('href')").extract_first()
        url = response.urljoin(href)
        return url if href else None

    def to_item(self, **kwargs):
        item = ProductItem()
        item['store'] = kwargs.get('store')
        item['name'] = kwargs.get('name')
        item['price'] = kwargs.get('price')
        item['image'] = kwargs.get('image')
        item['weight'] = kwargs.get('weight')
        item['url'] = kwargs.get('url')
        item['category'] = kwargs.get('category')
        return item
