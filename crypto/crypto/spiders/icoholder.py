from functools import partial

import scrapy

from ..utils import xpath_exract_first_text, parse_social_link, xpath_tolerant, unify_title

MAX_PAGE = 464


XPATH_SOCIAL_LINK = '//div[@id="activity"]//a[@href[contains(., "{href_contains}")]]/@href'
XPATH_TITLE = '//div[@class="ico-titles-in-view"]/h1'
XPATH_DESCRIPTION = '//div[@class="description-value"]'
XPATH_LAST_UPDATE = '//div[@class="analysis"]//div[@class="last-analysis-item"]/p[2]'

XPATH_LATEST_STAGE_NAME = '//div[contains(@class, "periods")]/div[@class="ico-list-row"][1]/div[@class="title"]'
XPATH_DATE_START = '//div[contains(@class, "periods")]/div[@class="ico-list-row"][1]//div[@class="ico-list-date-from"]'
XPATH_DATE_END = '//div[contains(@class, "periods")]/div[@class="ico-list-row"][1]//div[@class="ico-list-date-to"]'
XPATH_STATUS = '//div[contains(@class, "periods")]/div[@class="ico-list-row"][1]//span[contains(@class, "badge")]'
XPATH_SOFT_CAP = '//div[contains(@class, "periods")]/div[@class="ico-list-row"][1]//div[@class="assets"]/div[span[contains(., "Cap")]]'
XPATH_HARD_CAP = '//div[contains(@class, "periods")]/div[@class="ico-list-row"][1]//div[@class="assets"]/div[span[contains(., "Hard cap")]]'

XPATH_PRICE = '//div[contains(@class, "periods")]/div[@class="ico-list-row"][1]//div[@class="prices"]//div'

XPATH_ACCEPTING = '//div[contains(@class, "ico-more-info")]/*[div[contains(., "Accepted Currencies")]]'
XPATH_TICKER = '//div[contains(@class, "ico-more-info")]/*[div[contains(., "Ticker")]]'
XPATH_TOKEN_DISTRIBUTION = '//div[contains(@class, "ico-more-info")]/div[div[contains(., "Token Distribution")]]/div'
XPATH_COUNTRY = '//div[contains(@class, "ico-more-info")]/*[div[contains(., "Registered Country")]]'
XPATH_HAS_MVP = '//div[contains(@class, "ico-more-info")]/*[div[contains(., "MVP/Prototype")]]'
XPATH_PLATFORM = '//div[contains(@class, "ico-more-info")]/*[div[contains(., "Platform")]]'
XPATH_RESTRICTED_COUNTRIES = '//div[contains(@class, "ico-more-info")]/*[div[contains(., "Restricted Countries")]]'
XPATH_CATEGORIES = '//div[contains(@class, "ico-more-info")]/*[div[contains(., "Categories")]]'
XPATH_KYC = '//div[contains(@class, "ico-more-info")]/*[div[contains(., "KYC")]]'
XPATH_WHITELIST = '//div[contains(@class, "ico-more-info")]/*[div[contains(., "Whitelist")]]'
XPATH_SUPPLY = '//div[contains(@class, "ico-more-info")]/*[div[contains(., "Total supply")]]'

XPATH_ABOUT = '//div[contains(@class, "about-row")]//p'

XPATH_CEO_NAME = '//div[@id="team"]//div[contains(., "CEO")]/div[@class="member-title"]/a'
XPATH_CEO_LINK = '//div[@id="team"]//div[contains(., "CEO")]/div[@class="member-title"]/a/@href'
XPATH_CTO_NAME = '//div[@id="team"]//div[contains(., "CTO")]/div[@class="member-title"]/a'
XPATH_CTO_LINK = '//div[@id="team"]//div[contains(., "CTO")]/div[@class="member-title"]/a/@href'


def extract_info(response, xpath_selector):
    try:
        return ''.join(response.xpath(xpath_selector + '/text()').extract()).replace('\n', ' ').strip() or None
    except:
        return None


class IcoholderSpider(scrapy.Spider):
    name = "icoholder"

    def start_requests(self):
        urls = ('https://icoholder.com/en/icos/all?page={}&sort=r.general&direction=desc'.format(i) for i in range(1, MAX_PAGE + 1))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        next_pages = response.xpath('//div[@class="ico-list-name-d"]/a/@href').extract()

        for next_page in next_pages:
            yield response.follow(next_page, callback=self.parse_ico)

    def parse_ico(self, response):
        xpath_wrap = partial(xpath_exract_first_text, response)
        parse_social_wrap = partial(parse_social_link, response, XPATH_SOCIAL_LINK)

        extract_info_wrap = partial(extract_info, response)

        yield {
            'title': unify_title(xpath_wrap(XPATH_TITLE)),
            'description': xpath_wrap(XPATH_DESCRIPTION),
            'last_updated': xpath_wrap(XPATH_LAST_UPDATE),

            'latest_stage_name': xpath_wrap(XPATH_LATEST_STAGE_NAME),
            'date_start': xpath_wrap(XPATH_DATE_START),
            'date_end': xpath_wrap(XPATH_DATE_END),
            'status': xpath_wrap(XPATH_STATUS),
            'soft_cap': extract_info_wrap(XPATH_SOFT_CAP),
            'hard_cap': extract_info_wrap(XPATH_HARD_CAP),
            'price': extract_info_wrap(XPATH_PRICE),

            'accepting': extract_info_wrap(XPATH_ACCEPTING),
            'ticker': extract_info_wrap(XPATH_TICKER),
            'token_distribution': extract_info_wrap(XPATH_TOKEN_DISTRIBUTION),
            'country': extract_info_wrap(XPATH_COUNTRY),
            'has_mvp': extract_info_wrap(XPATH_HAS_MVP),
            'platform': extract_info_wrap(XPATH_PLATFORM),
            'restricted_countries': extract_info_wrap(XPATH_RESTRICTED_COUNTRIES),
            'kyc': extract_info_wrap(XPATH_KYC),
            'whitelist': extract_info_wrap(XPATH_WHITELIST),
            'total_supply': extract_info_wrap(XPATH_SUPPLY),

            'about': xpath_wrap(XPATH_ABOUT),

            'twitter_link': parse_social_wrap('twitter.com'),
            'linkedin_link': parse_social_wrap('linkedin.com'),
            'telegram_link': parse_social_wrap('t.me'),
            'reddit_link': parse_social_wrap('reddit.com'),
            'facebook_link': parse_social_wrap('facebook.com'),
            'github_link': parse_social_wrap('github.com'),
            'bitcointalk_link': parse_social_wrap('bitcointalk.org'),
            'slack_link': parse_social_wrap('slack.com'),
            'youtube_link': parse_social_wrap('youtube.com'),
        }

