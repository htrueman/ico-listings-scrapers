from functools import partial

import scrapy

from ..utils import xpath_exract_first_text, parse_social_link, xpath_tolerant

XPATH_TITLE = '//*[@id="ico-profile"]/div[1]/div[1]/div/div[2]/h1'
XPATH_UPDATED = '//*[@id="ico-profile"]/div[1]/div[1]/div/div[2]/div/span'
XPATH_DESCRIPTION = '//*[@id="ico-profile"]/div[1]/div[1]/div/div[2]/p'
XPATH_WHITEPAPER = '//*[@id="ico-profile"]/div[1]/div[1]/div/div[2]/ul/li/a[text()[contains(., "Whitepaper")]]/@href'
XPATH_WEBSITE = '//*[@id="ico-profile"]/div[1]/div[1]/div/div[2]/ul/li/a[text()[contains(., "Website")]]/@href'
XPATH_RATING = '/html/body/div[1]/main/div/div/div[2]/div[1]/div/div[2]/div[1]'
XPATH_STATUS = '/html/body/div[1]/main/div/div/div[2]/div[1]/div/div/div[span[contains(., "Status")]]/child::span[2]/span'
XPATH_PUBLIC_SALE = '/html/body/div[1]/main/div/div/div[2]/div[1]/div/div/div[span[contains(., "Public sale")]]/child::span[2]'
XPATH_CAP = '/html/body/div[1]/main/div/div/div[2]/div[1]/div/div/div[span[contains(., "Cap")]]/child::span[2]'
XPATH_GOAL = '/html/body/div[1]/main/div/div/div[2]/div[1]/div/div/div[span[contains(., "Goal")]]/child::span[2]'
XPATH_PRICE = '/html/body/div[1]/main/div/div/div[2]/div[1]/div/div/div[span[contains(., "Price")]]/child::span[2]'
XPATH_SOCIAL_LINK = '/html/body/div[1]/main/div/div/div[2]/div[1]/div/div/div/div/a/@href[contains(., "{href_contains}")]'

MAX_PAGE = 32


class IcobazaarSpider(scrapy.Spider):
    name = "icobazaar"

    def start_requests(self):
        urls = ('https://icobazaar.com/v2/ico-list?page={}'.format(i) for i in range(1, MAX_PAGE + 1))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        next_pages = response.xpath('//*[@id="PjaxForm"]/div[4]/div/a/@href').extract()

        for next_page in next_pages:
            yield response.follow(next_page, callback=self.parse_ico)

    def parse_ico(self, response):
        xpath_wrap = partial(xpath_exract_first_text, response)
        parse_social_wrap = partial(parse_social_link, response, XPATH_SOCIAL_LINK)
        yield {
            'title': xpath_wrap(XPATH_TITLE).split('(')[0].strip(),
            'last_updated': xpath_wrap(XPATH_UPDATED),
            'description': xpath_wrap(XPATH_DESCRIPTION),
            'whitepaper': xpath_tolerant(response, XPATH_WHITEPAPER),
            'website': xpath_tolerant(response, XPATH_WEBSITE),
            'rating': xpath_wrap(XPATH_RATING),
            'status': xpath_wrap(XPATH_STATUS),
            'public_sale': xpath_wrap(XPATH_PUBLIC_SALE),
            'cap': xpath_wrap(XPATH_CAP),
            'goal': xpath_wrap(XPATH_GOAL),
            'price': xpath_wrap(XPATH_PRICE),
            'twitter_link': parse_social_wrap('twitter.com'),
            'linkedin_link': parse_social_wrap('linkedin.com'),
            'telegram_link': parse_social_wrap('t.me'),
            'reddit_link': parse_social_wrap('reddit.com'),
            'facebook_link': parse_social_wrap('facebook.com'),
            'github_link': parse_social_wrap('github.com'),
            'bitcointalk_link': parse_social_wrap('bitcointalk.org'),
            'slack_link': parse_social_wrap('slack.com'),
        }
        # 'team': [
        #     {'name': '', 'position': '', 'linkedin_link': ''},
        # ]  # ???

