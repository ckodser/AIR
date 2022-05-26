import scrapy
import random
import re


class QuotesSpider(scrapy.Spider):
    name = "MamyFood"

    start_urls = [
        'https://mamifood.org/cooking-training/recipe/15280/%D8%B7%D8%B1%D8%B2-%D8%AA%D9%87%DB%8C%D9%87-%D8%A7%D8%B3%D8%AA%D8%A7%D9%86%D8%A8%D9%88%D9%84%DB%8C-%D9%BE%D9%84%D9%88'
    ]

    def parse(self, response):
        yield scrapy.Request(response.url, callback=self.parser_food_page)
        return
        foods = []
        for link_sec in response.css('.Tabel'):
            link_sec = link_sec.css("a")
            print(link_sec)
            for links in link_sec.css("li"):
                food = response.urljoin(links.css("a::attr(href)").get())
                food.append(food)

        for step, food in enumerate(foods):
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
