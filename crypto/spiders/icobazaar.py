import scrapy

from crypto.items import load_organization


XPATHS = {
    'TITLE': '//*[@id="ico-profile"]/div[1]/div[1]/div/div[2]/h1',
    'UPDATED': '//*[@id="ico-profile"]/div[1]/div[1]/div/div[2]/div/span',
    'DESCRIPTION': '//*[@id="ico-profile"]/div[1]/div[1]/div/div[2]/p',
    'WHITEPAPER': '//*[@id="ico-profile"]/div[1]/div[1]/div/div[2]/ul/'
                  'li/a[text()[contains(., "Whitepaper")]]/@href',
    'WEBSITE': '//*[@id="ico-profile"]/div[1]/div[1]/div/div[2]/ul/li/a[text()[contains(., "Website")]]/@href',
    'RATING': '/html/body/div[1]/main/div/div/div[2]/div[1]/div/div[2]/div[1]',
    'STATUS': '/html/body/div[1]/main/div/div/div[2]/div[1]/div/div/'
              'div[span[contains(., "Status")]]/child::span[2]/span',
    'PUBLIC_SALE': '/html/body/div[1]/main/div/div/div[2]/div[1]/'
                   'div/div/div[span[contains(., "Public sale")]]/child::span[2]',
    'CAP': '/html/body/div[1]/main/div/div/div[2]/div[1]/'
           'div/div/div[span[contains(., "Cap")]]/child::span[2]',
    'GOAL': '/html/body/div[1]/main/div/div/div[2]/div[1]/div/'
            'div/div[span[contains(., "Goal")]]/child::span[2]',
    'PRICE': '/html/body/div[1]/main/div/div/div[2]/div[1]/'
             'div/div/div[span[contains(., "Price")]]/child::span[2]',
    'SOCIAL_LINK': '/html/body/div[1]/main/div/div/div[2]/div[1]/'
                   'div/div/div/div/a/@href[contains(., "{href_contains}")]',
}

MAX_PAGE = 1


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
