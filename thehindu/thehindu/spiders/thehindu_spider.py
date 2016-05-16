from scrapy.spiders import CrawlSpider,Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from thehindu.items import ThehinduItem
import thehindu.settings    

class TheHindu(CrawlSpider):
    name = "thehindu"
    allowed_domains = ["thehindu.com"]
    start_urls = [ "http://www.thehindu.com" ]
    rules = (
        Rule(
            LinkExtractor(
                allow_domains=thehindu.settings.CRAWLER_DOMAINS,
                allow=thehindu.settings.CRAWLER_ALLOW_REGEX,
                deny=thehindu.settings.CRAWLER_DENY_REGEX,
                canonicalize=True,
                unique=True
            ),
            follow=True,
            callback='parse_item',
            process_links='filter_links'
        ),
    )

    def filter_links(self, links):
        return_links = list()
        if links:
            for link in links:
                if not link.nofollow:
                    return_links.append(link)
                else:
                    self.logger.debug('Dropped link %s because nofollow attribute was set.' % link.url)
        return return_links

    def parse_item(self, response):
        item =ThehinduItem()
        item['title'] = response.xpath("//title/text()").extract()
        item['heading'] = response.xpath('//div[@class="article-text"]').xpath(".//h2/text()").extract()
        item['text'] = response.xpath('//div[@class="article-text"]').xpath(".//p/text()").extract()
        item['keywords'] =  response.xpath('//div[@id="articleKeywords"]').xpath(".//a/text()").extract()
        return item

