# -*- coding: utf-8 -*-
import scrapy

from crawlers.items import ProductItem
from crawlers.utils import parse, product_type

class WheyproteinCentralfitSpider(scrapy.Spider):
    name = 'wheyprotein-centralfit'
    store = 'centralfit'
    start_urls = ['http://www.centralfit.com.br/massa-e-energia/principais-ingredientes/whey-protein.html/']

    def parse(self, response):
        products = response.css('.products-grid .item')
        for product in products:
            yield self.parse_product(product)

        next_url = self.next_page(response)
        if next_url:
            yield scrapy.Request(url=next_url, callback=self.parse)

    def parse_product(self, product):
        name = product.css('.product-name ::text').extract_first()
        if product_type.is_wheyprotein(name):
            price = parse.parse_price(product.css('.price_boleto_discount ::text').extract_first())
            image = product.css('img::attr(src)').extract_first()
            weight = parse.parse_weight(name)
            url = product.css('.product-image ::attr(href)').extract_first()
            item = self.to_item(store=self.store, name=name, price=price, image=image, weight=weight, url=url, category=product_type.WHEY_PROTEIN)
            return item

    def next_page(self, response):
        href = response.css(".pages .next > a::attr('href')").extract_first()
        url = response.urljoin(href)
        return url if href else None

    def to_item(self, **kwargs):
        item = ProductItem()
        item['store'] = kwargs.get('store')
        item['name'] = kwargs.get('name')
        item['price'] = kwargs.get('price')
        item['image'] = kwargs.get('image')
        item['url'] = kwargs.get('url')
        item['weight'] = kwargs.get('weight')
        item['category'] = kwargs.get('category')
        return item
