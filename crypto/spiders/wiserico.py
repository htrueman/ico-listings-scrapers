import scrapy

from ..utils import unify_title


class WisericoSpider(scrapy.Spider):
    name = 'wiserico'
    start_urls = [
        'https://wiserico.com/',
        'https://wiserico.com/upcoming',
        'https://wiserico.com/past'
    ]

    def parse(self, response):
        next_pages = response.xpath(
            '//div[contains(@class, "icosBlock-items")]'
            '//child::a[1]/@href').re(regex=r'^[^#]+$')

        for page in next_pages:
            yield response.follow(page, callback=self.parse_pages)

        pag_pages = response.xpath('//ul[contains(@class, "pagination")]//a/@href').extract()
        for page in pag_pages:
            yield response.follow(page, callback=self.parse)

    def parse_pages(self, response):
        try:
            platform = response.xpath(
                '//span[contains(., "Platform")]/text()').extract_first().split(':')[1].strip()
        except IndexError:
            platform = None

        try:
            accepting = response.xpath(
                '//span[contains(., "Accepting")]/text()').extract_first().split(':')[1].strip()
        except IndexError:
            accepting = None

        try:
            starts = response.xpath(
                '//div[contains(@class, "timeline")]'
                '/*[contains(., "Starts")]').re(regex=r'[\d+]{2}\.[\d+]{2}.[\d+]{4}')[0]
        except IndexError:
            starts = None

        try:
            ends = response.xpath('//div[contains(@class, "timeline")]/*[contains(., "Ends")]').re(
                regex=r'[\d+]{2}\.[\d+]{2}.[\d+]{4}')[0]
        except IndexError:
            ends = None
        yield {
            'title': unify_title(
                response.xpath('//div[contains(@class, "title")]/h1/text()').extract_first()),
            'platform': platform,
            'accepting': accepting,
            'starts': starts,
            'ends': ends,
            'description': ''.join(
                response.xpath('//div[contains(., "Content")]//p/text()').extract()),

            'slack': ''.join(
                response.xpath('//div[contains(@class, "socials")]//li/a/@href').re(regex=r'.+slack.+')),
            'facebook': ''.join(response.xpath(
                '//div[contains(@class, "socials")]//li/a/@href').re(regex=r'.+facebook.+')),
            'telegram': ''.join(
                response.xpath('//div[contains(@class, "socials")]//li/a/@href').re(regex=r'.+t\.me.+')),
            'bitcointalk': ''.join(response.xpath(
                '//div[contains(@class, "socials")]//li/a/@href').re(regex=r'.+bitcointalk.+')),
            'twitter': ''.join(response.xpath(
                '//div[contains(@class, "socials")]//li/a/@href').re(regex=r'.+twitter.+')),
            'github': ''.join(response.xpath('//div[contains(@class, "socials")]//li/a/@href').re(regex=r'.+github.+'))
        }
