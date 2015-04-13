import scrapy, json, re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request
from manga.items import MangaItem


class mangaSpider(CrawlSpider):
    name = "manga"
    allowed_domains = ['manhua.dmzj.com']
    start_urls = ["http://manhua.dmzj.com"]

    rules = (
        # Rule(LinkExtractor(allow=("http://manhua.dmzj.com/tags/*+"))),
        Rule(LinkExtractor(allow=("http://manhua.dmzj.com/*+",)), callback='parse_item')
    )

    def parse_item(self, response):
        item = MangaItem()

        manga_attr = response.xpath("//table/tr/td")      
        item['tag'] = []

        #title
        item['title'] = response.css(".odd_anim_title_m").xpath(".//h1/text()").extract()
        #synonym
        item['synonym'] = manga_attr[0].xpath("./text()").extract()
        #og name
        item['og_name'] = manga_attr[1].xpath("./text()").extract()
        #author url
        item['author_url'] = manga_attr[2].xpath('./a/@href').extract()
        #author
        item['author'] = manga_attr[2].xpath("./a/text()").extract()
        #area tag
        item['tag'] += manga_attr[3].xpath("./a/text()").extract()
        #status tag
        item['tag'] += manga_attr[4].xpath("./a/text()").extract()
        #hits
        item['hits'] = manga_attr[5].xpath("./a/text()").extract()
        #type tag
        item['tag'] += manga_attr[6].xpath("./a/text()").extract()
        #category tag
        item['tag'] += manga_attr[7].xpath("./a/text()").extract()
        #cover
        item['cover'] = response.css("div.anim_intro_ptext > a > img::attr(src)").extract()

        urls = response.css("div.cartoon_online_border > ul > li > a::attr(href)").extract()
        nums = range(1,len(urls)+1)
        item['chapters'] = dict(zip(nums,urls))
        
        id_text = response.xpath("//script")[4].extract()
        m = re.search(r"\"([0-9]+)\"",id_text)
        if m:
            id = m.group(1)
            req = Request(url="http://manhua.dmzj.com/hits/" + id + ".json", callback=self.parse_item2)
            req.meta["item"] = item
            return req
        else:
            return item

        return item

    def parse_item2(self, response):
        item = response.meta['item']
        res = json.loads(response.body)
        hits = res['hot_hits']
        #ex: u'3707627\u2103' remove the degree sign \u2103 from hits
        hits = hits[0:hits.find(u'\u2103')]
        item['hits'] = hits
        return item
