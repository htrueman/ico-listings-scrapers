import scrapy


class WisericoSpider(scrapy.Spider):
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

    def parse_pages(self, response):
        yield {
            'platform': '',
            'accepting': '',
            'starts': '',
            'ends': '',

            'slack': '',
            'facebook': '',
            'telegram': '',
            'bitcointalk': '',
            'twitter': '',
        }

