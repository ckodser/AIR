import scrapy
import random
import re


class QuotesSpider(scrapy.Spider):
    name = "iranplit"

    start_urls = [
        'https://fa.wikipedia.org/wiki/%D8%B1%D8%AF%D9%87:%D8%B3%DB%8C%D8%A7%D8%B3%D8%AA_%D8%AF%D8%B1_%D8%A7%DB%8C%D8%B1%D8%A7%D9%86'
    ]
    dict_rade = []
    dict_wiki = []

    def parse(self, response):
        QuotesSpider.dict_rade.append(response.url)
        rades = []
        for link_sec in response.css('.CategoryTreeItem'):
            rade = response.urljoin(link_sec.css("a::attr(href)").get())
            rades.append(rade)
        wikis = []

        for link_sec in response.css('.mw-category-group'):
            link_sec = link_sec.css("ul")
            for links in link_sec.css("li"):
                wiki = response.urljoin(links.css("a::attr(href)").get())
                wikis.append(wiki)

        wikis = [x for x in wikis if x not in rades]
        print(f"in rade-{len(QuotesSpider.dict_rade)} , inside rade:{len(rades)}, inside wiki:{len(wikis)}")
        for wiki in wikis:
            yield scrapy.Request(wiki, callback=self.parser_wiki_page)

        for rade in rades:
            yield scrapy.Request(rade, callback=self.rade_parse)

    def rade_parse(self, response):
        QuotesSpider.dict_rade.append(response.url)
        # print("rade:",len(QuotesSpider.dict_rade))
        rades = []
        for link_sec in response.css('.CategoryTreeItem'):
            rade = response.urljoin(link_sec.css("a::attr(href)").get())
            rades.append(rade)
        wikis = []

        for link_sec in response.css('.mw-category-group'):
            link_sec = link_sec.css("ul")
            for links in link_sec.css("li"):
                wiki = response.urljoin(links.css("a::attr(href)").get())
                wikis.append(wiki)

        wikis = [x for x in wikis if x not in rades]
        print(f"in subrade-{len(QuotesSpider.dict_rade)} , inside rade:{len(rades)}, inside wiki:{len(wikis)}")

        for wiki in wikis:
            yield scrapy.Request(wiki, callback=self.parser_wiki_page)

    def parser_wiki_page(self, response):
        if len(QuotesSpider.dict_wiki) > 6 and random.random() > 0.22:
            return
        QuotesSpider.dict_wiki.append(response.url)
        print("wiki:", len(QuotesSpider.dict_wiki))

        for step, e in enumerate(response.css('div#mw-content-text>div>p')):
            para = e.get()
            # para= re.sub("[a-zA-Z><%\"#]+", "",para)
            yield {'para': para}
