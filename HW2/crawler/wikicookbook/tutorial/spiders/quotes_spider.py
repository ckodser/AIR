import scrapy
import random
import re


class QuotesSpider(scrapy.Spider):
    name = "WIKIcookbook"
    num=0
    start_urls = [
        'https://fa.wikibooks.org/wiki/%DA%A9%D8%AA%D8%A7%D8%A8_%D8%A2%D8%B4%D9%BE%D8%B2%DB%8C'
    ]

    def parse(self, response):
        wikis = []
        good_steps=[2,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]
        # print(response.xpath('//div[@class="hlist"]/ul/li/a/@href').extract())
        for step, part in enumerate(response.xpath('//div[@class="hlist"]/ul')):
            if step  in good_steps:
              for link in part.xpath("li/a/@href").extract():
                wiki = response.urljoin(link)
                wikis.append(wiki)

        for step, wiki in enumerate(wikis):
            yield scrapy.Request(wiki, callback=self.parser_wiki_page)

    def parser_wiki_page(self, response):
        self.num+=1
        name = response.xpath('//h1[@id="firstHeading"]/text()').get()
        name = re.sub("کتاب آشپزی/", "", name)
        print("wiki:", self.num,name)
        js = {"name": name, "url": response.url, "tags":response.xpath('//div[@id="mw-normal-catlinks"]/ul/li/a/text()').extract()}
        js["Preparation"] = ""
        js["ingredients"] = []
        for e in response.xpath('//div[@class="mw-parser-output"]/p|//div[@class="mw-parser-output"]/h2|//div[@class="mw-parser-output"]/ol'):
          if e.root.tag=="p":
            js["Preparation"]+="\n".join(e.xpath("text()").extract())
          if e.root.tag=="ol":
            js["ingredients"]=e.xpath("//li/text()").extract()
          if e.root.tag=="h2":
            h=e.xpath('span[@class="mw-headline"]/text()').extract()
            if len(h)>=1:
              h=h[0]
              if h.startswith("دستور شماره"):
                if len(js["Preparation"])>0:
                  yield js
                  js["Preparation"] = ""
                  js["ingredients"] = []
        yield js
