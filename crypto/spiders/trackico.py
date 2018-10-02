from functools import partial

import scrapy

from ..utils import xpath_tolerant, xpath_exract_first_text, parse_social_link, unify_title, unify_website

XPATH_SOCIAL_LINK = '//*[@class="main-container"]//a[@href[contains(., "{href_contains}")]]/@href'

XPATH_TITLE = '//*[@class="main-container"]//h1[@class="h2"]'
XPATH_RATING = '//*[@class="main-container"]//div[footer[contains(., "rating")]]//strong'
XPATH_WEBSITE = '//*[@class="main-container"]//a[text()[contains(., "Website")]]/@href'
XPATH_WHITEPAPER = '//*[@class="main-container"]//a[text()[contains(., "Whitepaper")]]/@href'
XPATH_PRE_SALE = '//*[@class="main-container"]//table/tbody/tr[./th[contains(., "Pre-Sale")]]/child::td[1]'
XPATH_TOKEN_SALE = '//*[@class="main-container"]//table/tbody/tr[./th[contains(., "Token Sale")]]/child::td[1]'
XPATH_COUNTRY = '//*[@class="main-container"]//table/tbody/tr[./th[contains(., "Country")]]/child::td[1]/a'
XPATH_PLATFORM = '//*[@id="tab-financial"]//table/tbody/tr[./th[contains(., "Platform")]]/child::td[1]/a'
XPATH_TOKEN_PRICE = '//*[@id="tab-financial"]//table/tbody/tr[./th[contains(., "Token Price")]]/child::td[1]'
XPATH_TOKEN_FOR_SALE = '//*[@id="tab-financial"]//table/tbody/tr[./th[contains(., "Token for sale")]]/child::td[1]'
XPATH_TOKEN_SUPPLY = '//*[@id="tab-financial"]//table/tbody/tr[./th[contains(., "Token supply")]]/child::td[1]'
XPATH_SOFT_CAP = '//*[@id="tab-financial"]//table/tbody/tr[./th[contains(., "Soft cap")]]/child::td[1]'
XPATH_HARD_CAP = '//*[@id="tab-financial"]//table/tbody/tr[./th[contains(., "Hard cap")]]/child::td[1]'
XPATH_ACCEPTING = '//*[@id="tab-financial"]//table/tbody/tr[./th[contains(., "Accepting")]]/child::td[1]'
XPATH_RESTRICTED_COUNTRIES = '//*[@id="tab-financial"]//table/tbody/tr[./th[contains(., "Restricted countries")]]/child::td[1]'
XPATH_KYC = '//*[@id="tab-financial"]//table/tbody/tr[./th[contains(., "Know Your Customer")]]/child::td[1]'
XPATH_WHITELIST = '//*[@id="tab-financial"]//table/tbody/tr[./th[contains(., "Whitelist")]]/child::td[1]'
XPATH_BONUS = '//*[@id="tab-financial"]//table/tbody/tr[./th[contains(., "Bonus")]]/child::td[1]/p/text()'

MAX_PAGE = 163


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

        try:
            bounty_link = response.xpath(XPATH_SOCIAL_LINK.format(href_contains="bitcointalk.org")).extract()[1]
        except Exception:
            bounty_link = None

        parse_social_wrap = partial(parse_social_link, response, XPATH_SOCIAL_LINK)

        yield {
            'title': unify_title(xpath_exract_first_text(response, XPATH_TITLE)),
            'rating': xpath_exract_first_text(response, XPATH_RATING),

            'website': unify_website(xpath_tolerant(response, XPATH_WEBSITE)),
            'whitepaper': xpath_tolerant(response, XPATH_WHITEPAPER),

            'bitcointalk_link': parse_social_wrap("bitcointalk.org"),
            'telegram_link': parse_social_wrap("t.me"),
            'twitter_link': parse_social_wrap("twitter.com"),
            'medium_link': parse_social_wrap("medium.com"),
            'facebook_link': parse_social_wrap("facebook.com"),
            'linkedin_link': parse_social_wrap("linkedin.com"),
            'reddit_link': parse_social_wrap("reddit.com"),
            'github_link': parse_social_wrap("github.com"),
            'instagram_link': parse_social_wrap("instagram.com"),

            'bounty_link': bounty_link,

            'pre_sale': xpath_exract_first_text(response, XPATH_PRE_SALE),
            'token_sale': xpath_exract_first_text(response, XPATH_TOKEN_SALE),
            'country': xpath_exract_first_text(response, XPATH_COUNTRY),

            'platform': xpath_exract_first_text(response, XPATH_PLATFORM),
            'token_price': xpath_exract_first_text(response, XPATH_TOKEN_PRICE),

            'token_for_sale': xpath_exract_first_text(response, XPATH_TOKEN_FOR_SALE),
            'token_supply': xpath_exract_first_text(response, XPATH_TOKEN_SUPPLY),

            'soft_cap': xpath_exract_first_text(response, XPATH_SOFT_CAP),
            'hard_cap': xpath_exract_first_text(response, XPATH_HARD_CAP),

            'accepting': xpath_exract_first_text(response, XPATH_ACCEPTING),
            'restricted_countries': xpath_exract_first_text(response, XPATH_RESTRICTED_COUNTRIES),
            'kyc': xpath_exract_first_text(response, XPATH_KYC),
            'whitelist': xpath_exract_first_text(response, XPATH_WHITELIST),
            'bonus': ' '.join(text for text in response.xpath(XPATH_BONUS).extract())
        }
