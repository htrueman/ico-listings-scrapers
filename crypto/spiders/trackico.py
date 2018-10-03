import scrapy
from scrapy.loader import ItemLoader

from crypto.items import Organization, SOCIAL_LINK_BASES


XPATHS = {
    'TITLE': '//*[@class="main-container"]//h1[@class="h2"]/text()',
    'WEBSITE': '//*[@class="main-container"]//a[text()[contains(., "Website")]]/@href',
    'COUNTRY': '//*[@class="main-container"]//table/tbody/tr[./th[contains(., "Country")]]/child::td[1]/a/text()',

    'SOCIAL_LINK': '//*[@class="main-container"]//a[@href[contains(., "{href_contains}")]]/@href',

    'HARD_CAP': '//*[@id="tab-financial"]//table/tbody/tr[./th[contains(., "Hard cap")]]/child::td[1]',
    'RATING': '//*[@class="main-container"]//div[footer[contains(., "rating")]]//strong',
    'TOKENS_FOR_SALE': '//*[@id="tab-financial"]//table/tbody/tr[./th[contains(., "Token for sale")]]/child::td[1]',
    'SOFT_CAP': '//*[@id="tab-financial"]//table/tbody/tr[./th[contains(., "Soft cap")]]/child::td[1]',

    'WHITEPAPER': '//*[@class="main-container"]//a[text()[contains(., "Whitepaper")]]/@href',
    'PRE_SALE': '//*[@class="main-container"]//table/tbody/tr[./th[contains(., "Pre-Sale")]]/child::td[1]',
    'TOKEN_SALE': '//*[@class="main-container"]//table/tbody/tr[./th[contains(., "Token Sale")]]/child::td[1]',
    'PLATFORM': '//*[@id="tab-financial"]//table/tbody/tr[./th[contains(., "Platform")]]/child::td[1]/a',
    'TOKEN_PRICE': '//*[@id="tab-financial"]//table/tbody/tr[./th[contains(., "Token Price")]]/child::td[1]',
    'TOKEN_SUPPLY': '//*[@id="tab-financial"]//table/tbody/tr[./th[contains(., "Token supply")]]/child::td[1]',
    'ACCEPTING': '//*[@id="tab-financial"]//table/tbody/tr[./th[contains(., "Accepting")]]/child::td[1]',
    'RESTRICTED_COUNTRIES': '//*[@id="tab-financial"]//'
                            'table/tbody/tr[./th[contains(., "Restricted countries")]]/child::td[1]',
    'KYC': '//*[@id="tab-financial"]//table/tbody/tr[./th[contains(., "Know Your Customer")]]/child::td[1]',
    'WHITELIST': '//*[@id="tab-financial"]//table/tbody/tr[./th[contains(., "Whitelist")]]/child::td[1]',
    'BONUS': '//*[@id="tab-financial"]//table/tbody/tr[./th[contains(., "Bonus")]]/child::td[1]/p/text()',
}
MAX_PAGE = 1


class TrackicoSpider(scrapy.Spider):
    name = "trackico"

    def start_requests(self):
        urls = ('https://www.trackico.io/{}/'.format(i) for i in range(1, MAX_PAGE + 1))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        next_pages = response.css(
            '.row.equal-height .col-md-6.col-xl-4 a::attr(href)'
        ).extract()
        for next_page in next_pages:
            yield response.follow(next_page, callback=self.parse_ico)

    @staticmethod
    def parse_ico(response):
        loader = ItemLoader(item=Organization(), response=response)

        # general
        loader.add_xpath('name', XPATHS['TITLE'])
        loader.add_xpath('site', XPATHS['WEBSITE'])
        loader.add_xpath('country', XPATHS['COUNTRY'])

        # social links
        for key, value in SOCIAL_LINK_BASES.items():
            loader.add_xpath(key, XPATHS['SOCIAL_LINK'].format(href_contains=value))

        # statistics
        loader.add_xpath('hardcap', XPATHS['HARD_CAP'])
        loader.add_xpath('rating', XPATHS['RATING'])
        loader.add_xpath('number_of_tokens', XPATHS['TOKENS_FOR_SALE'])
        loader.add_xpath('softcap', XPATHS['SOFT_CAP'])

        return loader.load_item()
