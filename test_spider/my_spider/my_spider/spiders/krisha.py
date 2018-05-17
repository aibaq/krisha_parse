# -*- coding: utf-8 -*-
import scrapy
import requests


# class KrishaSpider(scrapy.Spider):
#     name = 'krisha'
#     allowed_domains = ['krisha.kz']
#     start_urls = ['http://krisha.kz/pro/specialist/']

#     def parse(self, response):
#         pass

# def get_file(url):
#     response = requests.get(url)
#     with open('image.jpg', 'rb+') as f:
#         f.write(response.body)


class KrishaSpider(scrapy.Spider):
    name = 'krisha'
    allowed_domains = ['krisha.kz']
    start_urls = ['http://krisha.kz/pro/specialist/']
    initial_next_urls = []
    page = 0

    def parse(self, response):
        self.page += 1
        with open('krisha.csv', 'a') as f:
            realtors = response.xpath("//div[@class='pitem']")
            for i in realtors:
                photo = i.css('div.image_cover').css('img.photo/@href').extract_first()
                name = i.css('div.pr_block').css('a.name::text').extract_first()
                numbers = i.css('div.pr_block').css('div.phones::text').extract_first().replace(' ', '').replace('(', '').replace(')', '').split(',')
                f.write('{},{}\n,{}'.format(name, ','.join(numbers), photo))
        next_page_url = response.xpath("//link[@id='NextLink']/@href").extract_first()
        if next_page_url and next_page_url not in self.initial_next_urls:
            if len(self.initial_next_urls) < 2:
                self.initial_next_urls.append(next_page_url)
            yield scrapy.Request(response.urljoin(next_page_url))
