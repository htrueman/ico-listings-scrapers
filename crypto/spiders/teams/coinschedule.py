from crypto.spiders.coinschedule import CoinscheduleBaseSpider
from crypto.utils import unify_title, unify_website


class CoinscheduleMembersSpider(CoinscheduleBaseSpider):
    name = 'coinschedule_members'

    def parse_pages(self, response):
        member_pages = response.xpath(
            '//div[contains(@class, "widget")]'
            '//a[contains(@class, "ui") and contains(@class, "card")]/@href').extract()

        ico_title = unify_title(response.xpath(
                '//div[contains(@class, "company-info")]'
                '//h1/text()').extract_first().replace('\n', ''))
        ico_website = unify_website(response.xpath(
                '//ul/li/span[contains(., "Website")]/following::span[1]/a/@href').extract_first())

        for page in member_pages:
            yield response.follow(page,
                                  callback=self.parse_members,
                                  meta={'ico_title': ico_title, 'ico_website': ico_website})

    def parse_members(self, response):
        ico_title = response.meta['ico_title']
        ico_website = response.meta['ico_website']

        full_name = response.xpath('//h1[contains(@class, "title")]/child::span[1]/text()').extract_first()
        linkedin_link = response.xpath(
            '//div[contains(@class, "widget") and h3[contains(., "Social")]]'
            '/div[contains(@class, "meta")]/a/@href').extract_first()
        country = response.xpath(
            '//h1[contains(@class, "title")]/following::div/span/text()').extract_first()
        yield {
            'ico_title': ico_title,
            'ico_website': ico_website,
            'full_name': full_name,
            'linkedin_link': linkedin_link,
            'country': country,
        }
