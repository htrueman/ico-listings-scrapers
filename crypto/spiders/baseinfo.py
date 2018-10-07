import scrapy

from crypto.items import load_organization, BaseInfoOrganization

XPATHS = {
    # general
    'NAME': '//*[contains(@class, "icos-title")]//h1/text()',
    'SITE': '//*[@class="single-ico-menu"]//li[1]/a/@href',

    # social links
    'SOCIAL_LINK': '//*[@class="single-ico-menu"]//li/a[contains(@href, "{href_contains}")]/@href',

    # statistics
    'RATING': '//*[@class="rating-block"]//div[@class="rb-rate"]/text()',

    # dates
    'ICO_DATE_RANGE': '//*[contains(@class, "icoContent__timeline")]//div[@class="item-time"]/text()'
}


class WisericoSpider(scrapy.Spider):
    name = 'baseinfo'
    start_urls = [
        'https://base.info/ico',
        'https://base.info/ico/upcoming',
        'https://base.info/ico/past',
    ]

    def parse(self, response):
        next_pages = response.xpath(
            '//div[@class="ico-table"]//tr//div[@class="link-block"]//''a[@class="table-link"]/@href'
        )

        for page in next_pages:
            yield response.follow(page, callback=self.parse_pages)

        pag_pages = response.xpath('//ul[contains(@class, "pagination")]//a/@href').extract()
        for page in pag_pages:
            yield response.follow(page, callback=self.parse)

    def parse_pages(self, response):
        return load_organization(response, XPATHS, context={'source': self.name}, item_cls=BaseInfoOrganization)
