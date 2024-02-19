from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class Spider(CrawlSpider):
    name = "crawler"
    allowed_domains = ["localhost"]
    start_urls = ["http://localhost:8000"]
    # Opt-in to 404 errors
    handle_httpstatus_list = [404]

    rules = [Rule(LinkExtractor(), callback="parse", follow=True)]

    def parse(self, response):
        if response.status == 404:
            yield {"url": response.url}
