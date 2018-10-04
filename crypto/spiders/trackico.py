import scrapy
from scrapy.loader import ItemLoader

from crypto.items import Organization, SOCIAL_LINK_BASES


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

    @staticmethod
    def parse_ico(response):
        loader = ItemLoader(item=Organization(), response=response)

        # general
        loader.add_xpath('name', XPATHS['NAME'])
        loader.add_xpath('site', XPATHS['SITE'])
        loader.add_xpath('country', XPATHS['COUNTRY'])
        loader.add_xpath('whitepaper', XPATHS['WHITEPAPER'])

        # social links
        for key, value in SOCIAL_LINK_BASES.items():
            loader.add_xpath(key, XPATHS['SOCIAL_LINK'].format(href_contains=value))

        # statistics
        loader.add_xpath('hardcap', XPATHS['HARDCAP'])
        loader.add_xpath('rating', XPATHS['RATING'])
        loader.add_xpath('number_of_tokens', XPATHS[' NUMBER_OF_TOKENS'])
        loader.add_xpath('softcap', XPATHS['SOFTCAP'])

        # dates
        loader.add_xpath('ico_date_range', XPATHS['ICO_DATE_RANGE'])
        loader.add_xpath('pre_ico_date_range', XPATHS['PRE_ICO_DATE_RANGE'])

        # extra
        loader.add_xpath('accepting', XPATHS['ACCEPTING'])
        loader.add_xpath('bonus', XPATHS['BONUS'])
        loader.add_xpath('know_your_customer', XPATHS['KNOW_YOUR_CUSTOMER'])
        loader.add_xpath('platform', XPATHS['PLATFORM'])
        loader.add_xpath('restricted_countries', XPATHS['RESTRICTED_COUNTRIES'])
        loader.add_xpath('token_price', XPATHS['TOKEN_PRICE'])
        loader.add_xpath('tokens_for_sale', XPATHS['TOKENS_FOR_SALE'])
        loader.add_xpath('whitelist', XPATHS['WHITELIST'])

        return loader.load_item()
