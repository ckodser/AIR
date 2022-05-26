import scrapy
import random
import re


class QuotesSpider(scrapy.Spider):
    name = "WIKIcookbook"

    start_urls = [
        'https://fa.wikibooks.org/wiki/%DA%A9%D8%AA%D8%A7%D8%A8_%D8%A2%D8%B4%D9%BE%D8%B2%DB%8C'
    ]

    def parse(self, response):
        wikis = []
        for link in response.xpath('//div[@id="hlist"]/ul/li/a/@href').extract():
            wiki = response.urljoin(link)
            wikis.append(wiki)

        for step, wiki in enumerate(wikis):
            yield scrapy.Request(wiki, callback=self.parser_wiki_page)

    def parser_wiki_page(self, response):
        name = response.xpath('//h1[@id="firstHeading"]/text()').get()
        name = re.sub("کتاب آشپزی/", "", name)
        print("wiki:", name)
        js = {"name": name, "url": response.url}
        text = ""
        for step, e in enumerate(response.css('div#mw-content-text>div>p')):
            para = e.get()
            text += para
        js["Preparation"] = text
        js["ingredients"] = []
        for step, e in enumerate(response.css('div#mw-content-text>div>ol>li')):
            para = e.get()
            js["ingredients"].append(para)

        js['tags'] = response.xpath('//div[@id="mw-normal-catlinks"]/ul/li/a/text()').extract()
        yield js
