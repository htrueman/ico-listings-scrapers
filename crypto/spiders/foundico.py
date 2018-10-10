import scrapy

from crypto.items import load_organization, FoundicoOrganization


class FoundicoBaseSpider(scrapy.Spider):
    start_urls = [
        'https://foundico.com/icos/'
    ]

    def parse(self, response):
        company_pages = response.xpath(
            '//table[contains(@id, "mn-icos-cont")]'
            '/tbody/tr/td/child::div[1]/a/@href').extract()
        for company_page in company_pages:
            yield response.follow(company_page, callback=self.parse_company_page)

        next_page = response.xpath('//i[.="chevron_right"]/parent::a/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        else:
            return 'Done'

    @staticmethod
    def parse_company_page(self, response):
        yield {}


XPATHS = {
    # general
    'NAME': '//h1/text()',
    'SITE': '//tr[./td[contains(., "Website")]]/child::td[3]/a/text()',
    'WHITEPAPER': '//tr[./td[contains(., "White paper")]]/child::td[3]/a/@href',

    # social link
    'SOCIAL_LINK': '//tr[./td[contains(., "Links")]]/child::td[3]/a[contains(@href, "{href_contains}")]/@href',

    # statistics
    'HARDCAP': '//tr[./td[contains(., "Hard cap")]]/child::td[3]/text()',
    'SOFTCAP': '//tr[./td[contains(., "Soft cap")]]/child::td[3]/text()',

    # dates
    'ICO_DATE_RANGE_FROM': '//div[@id="ico-start"]//text()',
    'ICO_DATE_RANGE_TO': '//div[@id="ico-end"]//text()',

    'TOTAL_ICO_DATE_RANGE_FROM': '//div[@id="ico-start"]//text()',
    'TOTAL_ICO_DATE_RANGE_TO': '//div[@id="ico-end"]//text()',

    # extra
    'ACCEPTING': '//tr[./td[contains(., "Currencies")]]/child::td[3]/text()',
    'AIRDROP_PROGRAM': '//tr[./td[contains(., "Airdrop program")]]/child::td[3]/text()',
    'BOUNTY_PROGRAM': '//tr[./td[contains(., "Bounty program")]]/child::td[3]/text()',
    'COUNTRY': '//tr[./td[contains(., "Location")]]/child::td[3]//text()',
    # 'HAS_MVP': '//tr[./td[contains(., "Have working prototype")]]/child::td[3]/text()',
    # 'KNOW_YOUR_CUSTOMER': '//tr[./td[contains(., "KYC of investors")]]/child::td[3]/text()',
    # 'RESTRICTED_COUNTRIES': '//tr[./td[contains(., "Restricted areas")]]/child::td[3]/text()',
    'TOKEN_PRICE': '//tr[./td[contains(., "Token price")]]/child::td[3]/text()',
    'TOKENS_FOR_SALE': '//tr[./td[contains(., "Tokens for sale")]]/child::td[3]/text()',
    'WHITELIST': '//tr[./td[contains(., "Whitelist of investors")]]/child::td[3]/text()'

}


class FoundicoSpider(FoundicoBaseSpider):
    name = 'foundico'

    def parse_company_page(self, response):
        return load_organization(response, XPATHS, context={'source': self.name}, item_cls=FoundicoOrganization)
