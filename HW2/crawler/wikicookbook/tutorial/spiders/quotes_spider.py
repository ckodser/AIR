import scrapy
import random
import re


class QuotesSpider(scrapy.Spider):
    name = "WIKIcookbook"

    start_urls = [
        'https://fa.wikibooks.org/wiki/%DA%A9%D8%AA%D8%A7%D8%A8_%D8%A2%D8%B4%D9%BE%D8%B2%DB%8C/%D9%81%D9%87%D8%B1%D8%B3%D8%AA_%D8%BA%D8%B0%D8%A7%D9%87%D8%A7%DB%8C_%D9%85%D8%AD%D9%84%DB%8C_%D8%A7%DB%8C%D8%B1%D8%A7%D9%86'
    ]

    def parse(self, response):
        wikis = []
        for link_sec in response.css('.mw-parser-output'):
            link_sec = link_sec.css("ol")
            for links in link_sec.css("li"):
                wiki = response.urljoin(links.css("a::attr(href)").get())
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
