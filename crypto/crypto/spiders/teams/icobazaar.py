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
        next_pages = response.xpath('//*[@id="PjaxForm"]/div[4]/div/a/@href').extract()
        for next_page in next_pages:
            yield response.follow(next_page + '/team', callback=self.parse_ico)

    def parse_ico(self, response):
        ico_title = unify_title(xpath_exract_first_text(response, XPATH_TITLE))

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
