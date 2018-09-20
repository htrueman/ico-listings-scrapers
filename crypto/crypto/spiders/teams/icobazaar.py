import scrapy

from ...utils import xpath_exract_first_text, unify_title

XPATH_TITLE = '//*[@id="ico-profile"]/div[1]/div[1]/div/div[2]/h1'

MAX_PAGE = 32


class IcobazaarMembersSpider(scrapy.Spider):
    name = "icobazaar_members"

    def start_requests(self):
        urls = ('https://icobazaar.com/v2/ico-list?page={}'.format(i) for i in range(1, MAX_PAGE + 1))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        next_pages = response.xpath('//div[contains(@class, "ico")]/a[@class="ico-link"]/@href').extract()
        titles = response.xpath('//div[contains(@class, "ico")]/h5/text()').extract()
        for next_page, title in zip(next_pages, titles):
            yield response.follow(next_page, callback=self.parse_ico, meta={'title': title})

    def parse_ico(self, response):
        ico_title = unify_title(response.meta['title'])

        members_names = response.xpath('//ul[@class="com-teams__wrapper"]//div[@class="user-card__name"]/text()').extract()[:3]
        members_positions = response.xpath('//ul[@class="com-teams__wrapper"]//div[@class="user-card__role"]/text()').extract()[:3]
        member_linkedin_links = response.xpath('//ul[@class="com-teams__wrapper"]//div[@class="user-card__links"]/a/@href').extract()[:3]

        for name, position, link in zip(members_names, members_positions, member_linkedin_links):
            yield {
                'ico_title': ico_title,
                'member_name': name,
                'member_position': position,
                'member_linkedin_link': link,
            }
