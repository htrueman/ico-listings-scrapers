import scrapy

from crypto.items import load_organization


class CoinscheduleBaseSpider(scrapy.Spider):
    start_urls = [
        'https://www.coinschedule.com/?live_view=2',
    ]

    def parse(self, response):
        next_pages = response.xpath(
            '//div[contains(@class, "divTableRow")]//div[1]//a/@href').extract()

        for page in next_pages:
            yield response.follow(page, callback=self.parse_pages)


XPATHS = {
    # general
    'NAME': '//div[contains(@class, "company-info")]//h1/text()',
    'SITE': '//ul/li/span[contains(., "Website")]/following::span[1]/a/@href',
    'COUNTRY': '//ul/li/span[contains(., "Jurisdiction")]/following::span[1]/text()',
    'WHITEPAPER': '//ul/li/span[contains(., "White Paper")]/following::span[1]/a/@href',

    # social links
    'SOCIAL_LINK': '//ul[contains(@class, "socials-list")]/li/a[contains(@href, "{href_contains}")]/@href',

    # extra
    'DESCRIPTION': '//div[contains(@class, "project-description")]//text()',
    'PLATFORM': '//ul/li/span[contains(., "Platform")]/following::span[1]/text()',
}


class CoinscheduleSpider(CoinscheduleBaseSpider):
    name = 'coinschedule'

    @staticmethod
    def get_date(date_selector, parameter, date_type):
        date = date_selector.xpath(
            '//div[contains(@class, "tab-pane") and {}(contains(@class, "active"))]'
            '//h6[contains(., "{}")]/following::*/text()'
            .format(parameter, date_type)
        ).extract_first()
        return date or ''

    def parse_pages(self, response):
        date_selector = response.xpath('//div[contains(@class, "event-tabs")]')
        has_tabs = bool(
            date_selector.xpath('//ul/li/a[contains(., "Pre-Sale")]/text()')
                         .extract_first()
        )

        pre_ico_date_range = None
        if has_tabs:
            pre_ico_date_range = ' - '.join([
                self.get_date(date_selector, '', 'Start'),
                self.get_date(date_selector, '', 'End')
            ])

            ico_date_range = ' - '.join([
                self.get_date(date_selector, 'not', 'Start'),
                self.get_date(date_selector, 'not', 'End')
            ])
        else:
            ico_date_range = ' - '.join([
                self.get_date(date_selector, '', 'Start') or '',
                self.get_date(date_selector, '', 'End') or ''
            ])

        return load_organization(response, XPATHS, context={
            'source': self.name,
            'pre_ico_date_range': pre_ico_date_range,
            'ico_date_range': ico_date_range,
        })
