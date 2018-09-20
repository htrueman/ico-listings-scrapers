import scrapy

from ...utils import xpath_exract_first_text

XPATH_TITLE = '//*[@class="main-container"]//h1[@class="h2"]'
XPATH_MEMBER_LINKS = ''

MAX_PAGE = 1


class TrackicoSpider(scrapy.Spider):
    name = "trackico"

    def start_requests(self):
        urls = ('https://www.trackico.io/{}/'.format(i) for i in range(1, MAX_PAGE + 1))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        next_pages = response.css(
            '.row.equal-height .col-md-6.col-xl-4 a::attr(href)'
        ).extract()
        for next_page in next_pages:
            yield response.follow(next_page, callback=self.parse_ico)

    def parse_ico(self, response):
        top_3_members = response.xpath(XPATH_MEMBER_LINKS).extract()[:3]

        for member in top_3_members:
            next_page = ''
            yield response.follow(
                next_page,
                callback=self.parse_member,
                meta={'title': xpath_exract_first_text(response, XPATH_TITLE)}
            )

    def parse_member(self, response):

        yield {
            'ico_title': '',
            'member_name': '',
            'member_position': '',
            'member_linkedin_link': '',
        }
