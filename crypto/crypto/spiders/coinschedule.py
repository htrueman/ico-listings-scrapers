import scrapy

from crypto.crypto.utils import unify_title


class CoinscheduleSpider(scrapy.Spider):
    name = 'coinschedule'
    start_urls = [
        'https://www.coinschedule.com/?live_view=2',
    ]

    def parse(self, response):
        next_pages = response.xpath(
            '//div[contains(@class, "divTableRow")]//div[1]//a/@href').extract()

        for page in next_pages:
            yield response.follow(page, callback=self.parse_pages)

    def parse_pages(self, response):
        yield {
            'title': unify_title(response.xpath(
                '//div[contains(@class, "company-info")]'
                '//h1/text()').extract_first().replace('\n', '')),
            'description': ''.join(
                response.xpath(
                    '//div[contains(@class, "project-description")]//text()').extract()),
            'category': response.xpath(
                '//ul/li/span[contains(., "Category")]'
                '/following::span[1]/text()').extract_first().replace('\n', ''),
            'website': response.xpath(
                '//ul/li/span[contains(., "Website")]/following::span[1]/a/@href').extract_first(),
            'project_type': response.xpath(
                '//ul/li/span[contains(., "Project Type")]'
                '/following::span[1]/text()').extract_first().replace('\n', ''),
            'white_paper': response.xpath(
                '//ul/li/span[contains(., "White Paper")]/following::span[1]/a/@href').extract_first(),
            'platform': response.xpath(
                '//ul/li/span[contains(., "Platform")]/following::span[1]/text()').extract_first().replace('\n', ''),
            'bitcoin_talk': response.xpath(
                '//ul/li/span[contains(., "Bitcoin")]/following::span[1]/a/@href').extract_first(),
            'jurisdiction': response.xpath(
                '//ul/li/span[contains(., "Jurisdiction")]/following::span[1]/text()').extract_first().replace('\n', ''),
        }
