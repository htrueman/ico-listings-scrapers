import scrapy
from scrapy.loader import ItemLoader

from crypto.items import Organization, SOCIAL_LINK_BASES, load_organization

XPATHS = {
    # general
    'NAME': '//*[@class="main-container"]//h1[@class="h2"]/text()',
    'SITE': '//*[@class="main-container"]//a[text()[contains(., "Website")]]/@href',
    'COUNTRY': '//*[@class="main-container"]//table/tbody/tr[./th[contains(., "Country")]]/child::td[1]/a/text()',
    'WHITEPAPER': '//*[@class="main-container"]//a[text()[contains(., "Whitepaper")]]/@href',

    # social links
    'SOCIAL_LINK': '//*[@class="main-container"]//a[@href[contains(., "{href_contains}")]]/@href',

    # statistics
    'HARDCAP': '//*[@id="tab-financial"]//table/tbody/tr[./th[contains(., "Hard cap")]]/child::td[1]/text()',
    'RATING': '//*[@class="main-container"]//div[footer[contains(., "rating")]]//strong/text()',
    'NUMBER_OF_TOKENS': '//*[@id="tab-financial"]//table/tbody/tr[./th[contains(., "Token supply")]]/child::td[1]/text()',
    'SOFTCAP': '//*[@id="tab-financial"]//table/tbody/tr[./th[contains(., "Soft cap")]]/child::td[1]/text()',

    # dates
    'PRE_ICO_DATE_RANGE': '//*[@class="main-container"]//table/tbody/tr[./th[contains(., "Pre-Sale")]]/child::td[1]/text()',
    'ICO_DATE_RANGE': '//*[@class="main-container"]//table/tbody/tr[./th[contains(., "Token Sale")]]/child::td[1]/text()',

    # extra
    'ACCEPTING': '//*[@id="tab-financial"]//table/tbody/tr[./th[contains(., "Accepting")]]/child::td[1]/text()',
    'BONUS': '//*[@id="tab-financial"]//table/tbody/tr[./th[contains(., "Bonus")]]/child::td[1]/p/text()',
    'KNOW_YOUR_CUSTOMER': '//*[@id="tab-financial"]//'
                          'table/tbody/tr[./th[contains(., "Know Your Customer")]]/child::td[1]/text()',
    'PLATFORM': '//*[@id="tab-financial"]//table/tbody/tr[./th[contains(., "Platform")]]/child::td[1]/a/text()',
    'RESTRICTED_COUNTRIES': '//*[@id="tab-financial"]//'
                            'table/tbody/tr[./th[contains(., "Restricted countries")]]/child::td[1]/text()',
    'TOKEN_PRICE': '//*[@id="tab-financial"]//table/tbody/tr[./th[contains(., "Token Price")]]/child::td[1]',
    'TOKENS_FOR_SALE': '//*[@id="tab-financial"]//'
                       'table/tbody/tr[./th[contains(., "Token for sale")]]/child::td[1]/text()',
    'WHITELIST': '//*[@id="tab-financial"]//table/tbody/tr[./th[contains(., "Whitelist")]]/child::td[1]/text()',
}
MAX_PAGE = 164


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

    def parse_ico(self, response):
        return load_organization(response, XPATHS, context={'source': self.name})
