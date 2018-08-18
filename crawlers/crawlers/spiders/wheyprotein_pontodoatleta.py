# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

from crawlers.items import ProductItem
from crawlers.utils import parse, product_type

class WheyproteinPontodoatletaSpider(scrapy.Spider):
    name = 'wheyprotein-pontodoatleta'
    store = 'pontodoatleta'
    start_urls = ['http://www.pontodoatleta.com.br/massa-muscular/whey-protein/']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 2.0})

    def parse(self, response):
        products = response.css('.product-item')
        for product in products:
            yield self.parse_product_page(response, product)

        next_url = self.next_page(response)
        if next_url:
            yield SplashRequest(next_url, self.parse, args={'wait': 2.0})

    def next_page(self, response):
        page_numbers = response.css('.pages .page-number ::text').extract()
        cur_page = str(int(response.css('.page-number.pgCurrent ::text').extract_first()) + 1)
        url = response.urljoin('#'+cur_page)
        return url if (cur_page in page_numbers) else None

    def parse_product_page(self, response, product):
        href = product.css('a ::attr(href)').extract_first()
        next_url = response.urljoin(href)
        return SplashRequest(next_url, self.parse_product, args={'wait': 2.0})

    def parse_product(self, response):
        name = response.css('.productName ::text').extract_first().strip()
        price = parse.parse_price(response.css('.skuBestPrice ::text').extract_first())
        url = response.url
        weights = response.css('.group_1 label ::text').extract()
        weight = parse.parse_price(weights[-1])
        image = response.css('#image-main ::attr(src)').extract_first()
        item = self.to_item(store=self.store, name=name, price=price, image=image, weight=weight, url=url, category=product_type.WHEY_PROTEIN)
        return item

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
