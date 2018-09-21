import scrapy

from crypto.utils import unify_title, unify_website


class CoinscheduleSpider(scrapy.Spider):
    name = 'coinschedule'
    start_urls = [
        'https://www.coinschedule.com/?live_view=2',
    ]

    def parse(self, response):
        next_pages = response.xpath(
            '//div[contains(@class, "divTableRow")]//div[1]//a/@href').extract()

        for page in next_pages:
            yield response.follow(page, callback=self.parse_pages)

    @staticmethod
    def get_date(date_selector, parameter, date_type):
        date = date_selector\
            .xpath('//div[contains(@class, "tab-pane") and {}(contains(@class, "active"))]'
                   '//h6[contains(., "{}")]/following::*/text()'.format(parameter, date_type))\
            .extract_first()
        return date

    def parse_pages(self, response):
        date_selector = response.xpath('//div[contains(@class, "event-tabs")]')
        has_tabs = bool(
            date_selector.xpath('//ul/li/a[contains(., "Pre-Sale")]/text()').extract_first())

        start_pre_sale_date = None
        end_pre_sale_date = None
        if has_tabs:
            start_pre_sale_date = self.get_date(date_selector, '', 'Start')
            end_pre_sale_date = self.get_date(date_selector, '', 'End')

            start_ico_date = self.get_date(date_selector, 'not', 'Start')
            end_ico_date = self.get_date(date_selector, 'not', 'End')
        else:
            start_ico_date = self.get_date(date_selector, '', 'Start')
            end_ico_date = self.get_date(date_selector, '', 'End')

        website_names = (
            'Github',
            'Twitter',
            'Reddit',
            'Youtube',
            'Facebook',
            'LinkedIn',
            'Telegram',
            'Instagram',
            'Steemit',
            'Discord',
            'Slack',
        )
        platform = response.xpath(
            '//ul/li/span[contains(., "Platform")]/following::span[1]/text()').extract_first()
        result = {
            'title': unify_title(response.xpath(
                '//div[contains(@class, "company-info")]'
                '//h1/text()').extract_first().replace('\n', '')),
            'description': ''.join(
                response.xpath(
                    '//div[contains(@class, "project-description")]//text()').extract()),
            'category': response.xpath(
                '//ul/li/span[contains(., "Category")]'
                '/following::span[1]/text()').extract_first().replace('\n', ''),
            'website': unify_website(response.xpath(
                '//ul/li/span[contains(., "Website")]/following::span[1]/a/@href').extract_first()),
            'project_type': response.xpath(
                '//ul/li/span[contains(., "Project Type")]'
                '/following::span[1]/text()').extract_first().replace('\n', ''),
            'white_paper': response.xpath(
                '//ul/li/span[contains(., "White Paper")]/following::span[1]/a/@href').extract_first(),
            'platform': platform.replace('\n', '') if platform else None,
            'bitcoin_talk': response.xpath(
                '//ul/li/span[contains(., "Bitcoin")]/following::span[1]/a/@href').extract_first(),
            'jurisdiction': response.xpath(
                '//ul/li/span[contains(., "Jurisdiction")]'
                '/following::span[1]/text()').extract_first().replace('\n', ''),
            'start_pre_sale_date': start_pre_sale_date,
            'end_pre_sale_date': end_pre_sale_date,
            'start_ico_date': start_ico_date,
            'end_ico_date': end_ico_date
        }
        for link in self.get_social_links(response, website_names):
            result.update(link)
        yield result


    @staticmethod
    def get_social_links(response, website_names):
        soc_links = []
        for website_name in website_names:
            soc_link = response.xpath(
                '//ul[contains(@class, "socials-list")]'
                '/li/a[span[contains(., "{}")]]/@href'.format(website_name)).extract_first()
            soc_links.append({website_name: soc_link})
        return soc_links
