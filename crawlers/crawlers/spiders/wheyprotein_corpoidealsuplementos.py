# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

from crawlers.items import ProductItem
from crawlers.utils import parse, product_type

class WheyproteinCorpoidealsuplementosSpider(scrapy.Spider):
    name = 'wheyprotein-corpoidealsuplementos'
    store = 'corpoidealsuplementos'
    start_urls = ['https://www.corpoidealsuplementos.com.br/massa_muscular/proteinas']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        products = response.css('.wd-product-line.available')
        for product in products:
            yield self.parse_product(product)

        next_url = self.next_page(response)
        if next_url:
            yield SplashRequest(next_url, self.parse, args={'wait': 0.5})

    def parse_product(self, product):
        name = product.css('a.name ::text').extract_first().strip()
        price = parse.parse_price(product.css('.condition.generic-price ::attr(data-price)').extract_first())
        image = product.css('img::attr(src)').extract_first()
        weight = parse.parse_weight(name)
        url = product.css('.link::attr(href)').extract_first()
        item = self.to_item(store=self.store, name=name, price=price, image=image, weight=weight, url=url, category=product_type.WHEY_PROTEIN)
        return item

    def next_page(self, response):
        pages = response.css('.divPaginacao')[0].css('li')
        count = len(pages)
        page_index = count
        for index, page in enumerate(pages):
            cur_page = page.css('.active ::text').extract_first()
            if cur_page:
                page_index = index + 1
                break

        if page_index != count:
            page_url = pages[page_index].css('::text').extract_first()
            return response.urljoin(f'#cp%3D{page_url}%2B')

        return None

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
