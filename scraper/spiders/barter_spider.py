from scrapy.spider import Spider
from scrapy.selector import Selector
from scraper.items import CraigslistAnchorTag
import MySQLdb

mydb = MySQLdb.connect(host='localhost',
    user='scraper',
    passwd='getmein123',
    db='craigslist')
cursor = mydb.cursor()


class BarterSpider(Spider):
    name = "barter"
    allowed_domains = ["craigslist.org"]
    start_urls = [
        "http://newyork.craigslist.org/bar/"
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
        self.db_import(items)

    def db_import(self, items):
        for item in items:
            keys = item.keys()
            if len(item[keys[0]]) == 0:
                item_1 = ''
            else:
                item_1 = item[keys[0]][0]
            if len(item[keys[1]]) == 0:
                item_2 = ''
            else:
                item_2 = item[keys[1]][0]

            cursor.execute(
                'INSERT INTO barter(%s, %s) VALUES("%s", "%s")' % (
                    keys[0],
                    keys[1],
                    item_1.replace('"', '\\"'),
                    item_2.replace('"', '\\"')
                )
            )

        mydb.commit()
        cursor.close()
        print "Imported to database."
