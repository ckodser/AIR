import scrapy
import random
import re


class QuotesSpider(scrapy.Spider):
    name = "MamyFood"

    start_urls = [
        'https://mamifood.org/cooking-training'
    ]

    def parse(self, response):
        foods_link = []
        for link in response.xpath('//article[@id="Table"]/a/@href').extract():
            food = response.urljoin(link)
            foods_link.append(food)
        print(len(foods_link))
        for step, food in enumerate(foods_link):
            yield scrapy.Request(food, callback=self.parser_food_page)

    def parser_food_page(self, response):
        name = response.xpath('//span[@id="lbltitr"]/text()').get()
        name = re.sub("طرز تهیه", "", name)
        print("mamy:", name)
        js = {"name": name, "url": response.url}
        js["ingredients"] = []
        for e in response.css('.dotbetween'):
            ingredient = e.css('.btnCustomer').xpath('text()').extract()[0]
            amount = e.css(".amount").xpath('text()').extract()[0]
            js["ingredients"].append(ingredient + " " + amount)
        js["Preparation"] = ""
        for e in response.css('.content'):
            text = e.css("p").xpath('text()').extract()
            js["Preparation"] += "\n".join(text)
        js['main_group'] = response.xpath('//a[@id="lnkGName"]/text()').extract()[0]
        js['sub_group'] = response.xpath('//a[@id="lnkSGName"]/text()').extract()[0]
        yield js
