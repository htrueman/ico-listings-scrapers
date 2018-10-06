import scrapy

from crypto.items import load_organization

XPATHS = {
    # general
    'NAME': '//div[@class="ico-titles-in-view"]/h1/text()',
    'SITE': '//div[@class="links-right"]//a[contains(@title, "website")]/@href',
    'WHITEPAPER': '//div[@class="links-right"]//a[contains(@title, "whitepaper")]/@href',
    'COUNTRY': '//div[contains(@class, "ico-more-info")]/*[div[contains(., "Registered Country")]]/text()[2]',

    # social links
    'SOCIAL_LINK': '//div[@id="activity"]//a[@href[contains(., "{href_contains}")]]/@href',

    # statistics
    'HARDCAP': '//div[contains(@class, "periods")]/div[@class="ico-list-row"][1]'
               '//div[@class="assets"]/div[span[contains(., "Hard cap")]]/text()',
    'NUMBER_OF_TOKENS': '//div[contains(@class, "ico-more-info")]/*[div[contains(., "Total supply")]]/text()',
    'SOFTCAP': '//div[contains(@class, "periods")]/div[@class="ico-list-row"][1]'
               '//div[@class="assets"]/div[span[contains(., "Cap")]]/text()',

    # extra_dates
    'LAST_STAGE_DATE_START': '//div[contains(@class, "periods")]/div[@class="ico-list-row"][1]//'
                             'div[@class="ico-list-date-from"]/text()',
    'LAST_STAGE_DATE_END': '//div[contains(@class, "periods")]/div[@class="ico-list-row"][1]//'
                           'div[@class="ico-list-date-to"]/text()',
    'LAST_STAGE_NAME': '//div[contains(@class, "periods")]/div[@class="ico-list-row"][1]/div[@class="title"]/text()',
    'LAST_STAGE_STATUS': '//div[contains(@class, "periods")]/div[@class="ico-list-row"][1]'
                         '//span[contains(@class, "badge")]/text()',

    # extra
    'ACCEPTING': '//div[contains(@class, "ico-more-info")]/*[div[contains(., "Accepted Currencies")]]/text()',
    'DESCRIPTION': '//div[@class="description-value"]/text()',
    'HAS_MVP': '//div[contains(@class, "ico-more-info")]/*[div[contains(., "MVP/Prototype")]]/text()',
    'KNOW_YOUR_CUSTOMER': '//div[contains(@class, "ico-more-info")]/*[div[contains(., "KYC")]]/text()',
    'PLATFORM': '//div[contains(@class, "ico-more-info")]/*[div[contains(., "Platform")]]/text()',
    'RESTRICTED_COUNTRIES': '//div[contains(@class, "ico-more-info")]'
                            '/*[div[contains(., "Restricted Countries")]]/text()',
    'TOKEN_DISTRIBUTION': '//div[contains(@class, "ico-more-info")]'
                          '/div[div[contains(., "Token Distribution")]]/div/text()',
    'TOKEN_NAME': '//div[contains(@class, "ico-more-info")]/*[div[contains(., "Ticker")]]/text()',
    'TOKEN_PRICE': '//div[contains(@class, "periods")]/div[@class="ico-list-row"][1]//div[@class="prices"]//div',
    'WHITELIST': '//div[contains(@class, "ico-more-info")]/*[div[contains(., "Whitelist")]]/text()',
}

MAX_PAGE = 464


class IcoholderSpider(scrapy.Spider):
    name = "icoholder"

    def start_requests(self):
        urls = (
            'https://icoholder.com/en/icos/all?page={}&sort=r.general&direction=desc'.format(i)
            for i in range(1, MAX_PAGE + 1)
        )
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        next_pages = response.xpath('//div[@class="ico-list-name-d"]/a/@href').extract()

        for next_page in next_pages:
            yield response.follow(next_page, callback=self.parse_ico)

    @staticmethod
    def parse_ico(response):
        return load_organization(response, XPATHS)
