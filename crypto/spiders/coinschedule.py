import scrapy

from crypto.items import load_organization, CoinscheduleOrganization


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
    # 'PLATFORM': '//ul/li/span[contains(., "Platform")]/following::span[1]/text()',
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
        has_tabs = len(response.xpath('//div[contains(@class, "event-tabs")]/ul/li').extract()) > 1
        has_pre_ico = bool(date_selector.xpath('//ul/li/a[contains(., "Pre")]/text()')
                                        .extract_first())

        pre_ico_date_range_from = \
            pre_ico_date_range_to = \
            ico_date_range_from = \
            ico_date_range_to = ''

        # TODO: refactor
        if has_tabs:
            if response.xpath('//div[contains(@class, "event-tabs")]/ul'
                              '/li[@class="active"]/a[contains(., "Pre")]/text()').extract_first():
                pre_ico_date_range_from = self.get_date(date_selector, '', 'Start')
                pre_ico_date_range_to = self.get_date(date_selector, '', 'End')

                ico_date_range_from = self.get_date(date_selector, 'not', 'Start'),
                ico_date_range_to = self.get_date(date_selector, 'not', 'End'),

            else:
                pre_ico_date_range_from = self.get_date(date_selector, 'not', 'Start')
                pre_ico_date_range_to = self.get_date(date_selector, 'not', 'End')

                ico_date_range_from = self.get_date(date_selector, '', 'Start')
                ico_date_range_to = self.get_date(date_selector, '', 'End')

            total_ico_date_range_from = pre_ico_date_range_from
            total_ico_date_range_to = ico_date_range_to

        elif has_pre_ico:
            pre_ico_date_range_from = self.get_date(date_selector, '', 'Start')
            pre_ico_date_range_to = self.get_date(date_selector, '', 'End')

            total_ico_date_range_from = pre_ico_date_range_from
            total_ico_date_range_to = pre_ico_date_range_to

        else:
            ico_date_range_from = self.get_date(date_selector, '', 'Start')
            ico_date_range_to = self.get_date(date_selector, '', 'End')

            total_ico_date_range_from = ico_date_range_from
            total_ico_date_range_to = ico_date_range_to

        return load_organization(response, XPATHS, context={
            'source': self.name,
            'pre_ico_date_range_from': pre_ico_date_range_from,
            'pre_ico_date_range_to': pre_ico_date_range_to,
            'ico_date_range_from': ico_date_range_from,
            'ico_date_range_to': ico_date_range_to,
            'total_ico_date_range_from': total_ico_date_range_from,
            'total_ico_date_range_to': total_ico_date_range_to,
        }, item_cls=CoinscheduleOrganization)
