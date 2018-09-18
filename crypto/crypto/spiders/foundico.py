from contextlib import suppress

import scrapy


class FoundicoSpider(scrapy.Spider):
    name = 'foundico'
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

    def parse_company_page(self, response):
        token_price = response.xpath(
                '//tr[./td[contains(., "Token price")]]/child::td[3]/text()').extract_first()
        start_time = response.xpath(
                '//div[@id="ico-start"]/span[@class="ico-c-month"]/text()').re(regex=r'\w+\s\w+')
        end_time = response.xpath(
                '//div[@id="ico-end"]/span[@class="ico-c-month"]/text()').re(regex=r'\w+\s\w+')

        data = {
            'title': response.xpath('//h1/text()').extract_first(),
            'type': response.xpath(
                '//tr[./td[contains(., "Type")]]/child::td[3]/text()').extract_first(),
            'category': response.xpath(
                '//tr[./td[contains(., "Category")]]/child::td[3]/a/@href').extract_first(),
            'verified team': response.xpath(
                '//tr[./td[contains(., "Verified team")]]/child::td[3]/text()').extract_first(),
            'whitelist_of_investors': response.xpath(
                '//tr[./td[contains(., "Whitelist of investors")]]/child::td[3]/text()').extract_first(),
            'kyc_of_investors': response.xpath(
                '//tr[./td[contains(., "KYC of investors")]]/child::td[3]/text()').extract_first(),
            'goal_of_funding': response.xpath(
                '//tr[./td[contains(., "Goal of funding")]]/child::td[3]/text()').extract_first(),
            'tokens_for_sale': response.xpath(
                '//tr[./td[contains(., "Tokens for sale")]]/child::td[3]/text()').extract_first(),
            'token_price': token_price.replace('\t', '') if token_price else None,
            'minimum_purchase': response.xpath(
                '//tr[./td[contains(., "Minimum purchase")]]/child::td[3]/text()').extract_first(),
            'airdrop_program': response.xpath(
                '//tr[./td[contains(., "Airdrop program")]]/child::td[3]/text()').extract_first(),
            'bounty_program': response.xpath(
                '//tr[./td[contains(., "Bounty program")]]/child::td[3]/text()').extract_first(),
            'have_escrow_agent': response.xpath(
                '//tr[./td[contains(., "Have escrow agent")]]/child::td[3]/text()').extract_first(),
            'have_working_prototype': response.xpath(
                '//tr[./td[contains(., "Have working prototype")]]/child::td[3]/text()').extract_first(),
            'white_paper': response.xpath(
                '//tr[./td[contains(., "White paper")]]/child::td[3]/a/@href').extract_first(),
            'currencies': response.xpath(
                '//tr[./td[contains(., "Currencies")]]/child::td[3]/text()').re(regex=r'\w+'),
            'exchange_markets': response.xpath(
                '//tr[./td[contains(., "Exchange markets")]]/child::td[3]/a/@href').extract(),
            'location': response.xpath(
                '//tr[./td[contains(., "Location")]]/child::td[3]/text()').extract_first(),
            'website': response.xpath(
                '//tr[./td[contains(., "Website")]]/child::td[3]/a/text()').extract_first(),
            'start_time': start_time[0]
                + ', ' + response.xpath('//div[@id="ico-start"]/span[@class="ico-c-year"]/text()').re(regex=r'\d+')[0]
                if start_time else None,
            'end_time': end_time[0]
                + ', ' + response.xpath('//div[@id="ico-end"]/span[@class="ico-c-year"]/text()').re(regex=r'\d+')[0]
                if end_time else None
        }

        links = response.xpath(
            '//tr[./td[contains(., "Links")]]/child::td[3]/a/@href').extract(),

        for link in links:
            with suppress(IndexError):
                print(link)
                data['https://medium.com/@xaya'.split('https://')[1].split('.')[0]] = link
        yield data
