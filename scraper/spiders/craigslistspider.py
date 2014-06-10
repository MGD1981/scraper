from scrapy.spider import Spider
from scrapy.selector import Selector
from scraper.items import CraigslistAnchorTag


class CraigslistSpider(Spider):
    name = "craigslist"
    allowed_domains = ["craigslist.org"]
    start_urls = [
        "http://newyork.craigslist.org/bka/"
    ]

    def parse(self, response):
        sel = Selector(response)
        anchor_tags = sel.xpath("//a")
        items = []
        for anchor_tag in anchor_tags[:100]:
            scrapy_anchor_tag = CraigslistAnchorTag()
            scrapy_anchor_tag['title'] = anchor_tag.xpath("text()").extract()
            scrapy_anchor_tag['link'] = anchor_tag.xpath("@href").extract()
            items.append(scrapy_anchor_tag)
        return items


