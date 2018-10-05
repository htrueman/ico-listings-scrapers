import scrapy

from crypto.items import load_organization


XPATHS = {
    # general
    'NAME': '//*[@id="ico-profile"]/div[1]/div[1]/div/div[2]/h1/text()',
    'SITE': '//*[@id="ico-profile"]/div[1]/div[1]/div/div[2]/ul/li/a[text()[contains(., "Website")]]/@href',
    'WHITEPAPER': '//*[@id="ico-profile"]/div[1]/div[1]/div/div[2]/ul/'
                  'li/a[text()[contains(., "Whitepaper")]]/@href',

    # social link
    'SOCIAL_LINK': '//div[@class="com-sidebar__socialbar"]//a/@href[contains(., "{href_contains}")]',

    # statistics
    'HARDCAP': '//div[@class="com-sidebar__info"]//div[span[contains(., "Cap")]]/child::span[2]/text()',

    # dates
    'ICO_DATE_RANGE': '//div[@class="com-sidebar__info"]//div[span[contains(., "Public sale")]]/child::span[2]/text()',

    # extra
    'DESCRIPTION': '//*[@id="ico-profile"]/div[1]/div[1]/div/div[2]/p/text()',
    'GOAL': '/html/body/div[1]/main/div/div/div[2]/div[1]/div/'
            'div/div[span[contains(., "Goal")]]/child::span[2]/text()',
    'RATING': '/html/body/div[1]/main/div/div/div[2]/div[1]/div/div[2]/div[1]/text()',
    'STATUS': '/html/body/div[1]/main/div/div/div[2]/div[1]/div/div/'
              'div[span[contains(., "Status")]]/child::span[2]/span/text()',
    'TOKEN_PRICE': '/html/body/div[1]/main/div/div/div[2]/div[1]/'
                   'div/div/div[span[contains(., "Price")]]/child::span[2]',
    'UPDATED': '//*[@id="ico-profile"]/div[1]/div[1]/div/div[2]/div/span/text()',

}

MAX_PAGE = 31


class IcobazaarSpider(scrapy.Spider):
    name = "icobazaar"

    def start_requests(self):
        urls = ('https://icobazaar.com/v2/ico-list?page={}'.format(i) for i in range(1, MAX_PAGE + 1))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        next_pages = response.xpath('//div[contains(@class, "ico")]/a[@class="ico-link"]/@href').extract()
        names = response.xpath('//div[contains(@class, "ico")]/h5/text()').extract()
        for next_page, name in zip(next_pages, names):
            yield response.follow(next_page, callback=self.parse_ico, meta={'name': name})

    @staticmethod
    def parse_ico(response):
        return load_organization(response, XPATHS, context={'name': response.meta['name']})
