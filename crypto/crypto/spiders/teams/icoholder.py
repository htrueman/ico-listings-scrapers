import scrapy

from ...utils import xpath_exract_first_text, unify_title, unify_website

XPATH_TITLE = '//div[@class="ico-titles-in-view"]/h1'
XPATH_WEBSITE = '//div[@class="links-right"]//a[contains(@title, "website")]/@href'

MAX_PAGE = 464


class IcoholderMembersSpider(scrapy.Spider):
    name = "icoholder_members"

    def start_requests(self):
        urls = ('https://icoholder.com/en/icos/all?page={}&sort=r.general&direction=desc'.format(i) for i in range(1, MAX_PAGE + 1))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        next_pages = response.xpath('//div[@class="ico-list-name-d"]/a/@href').extract()
        for next_page in next_pages:
            yield response.follow(next_page, callback=self.parse_ico)

    def parse_ico(self, response):
        ico_title = unify_title(xpath_exract_first_text(response, XPATH_TITLE))
        ico_website = unify_website(xpath_exract_first_text(response, XPATH_WEBSITE))

        members_names = response.xpath('//*[@id="team"]//div[@class="member-title"]/a/text()').extract()[:3]
        members_positions = response.xpath('//*[@id="team"]//div[@class="member-position"]/text()').extract()[:3]
        member_linkedin_links = response.xpath('//*[@id="team"]//div[@class="member-title"]/a/@href').extract()[:3]

        for name, position, link in zip(members_names, members_positions, member_linkedin_links):
            yield {
                'ico_title': ico_title,
                'ico_website': ico_website,
                'member_name': name,
                'member_position': position.replace('\n', ''),
                'member_linkedin_link': link,
            }
