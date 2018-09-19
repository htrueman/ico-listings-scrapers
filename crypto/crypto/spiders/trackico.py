import scrapy


XPATH_SOCIAL_LINK = '/html/body/main/div/div[1]/div[1]/div/div[2]/div/div/div[1]/div[2]/div[2]/a[@href[contains(., "{}")]]/@href'
XPATH_BOUNTY_LINK = '/html/body/main/div/div[1]/div[1]/div/div[2]/div/div/div[1]/div[2]/div[2]/a[@href[contains(., "bitcointalk.org")]]/@href'
XPATH_TITLE = '/html/body/main/div/div[1]/div[1]/div/div[2]/div/div/div[1]/div[2]/div[1]/h1'
XPATH_RATING = '/html/body/main/div/div[1]/div[2]/div/div[2]/div/div/div/strong'
XPATH_WEBSITE = '/html/body/main/div/div[1]/div[1]/div/div[2]/div/div/div[1]/div[2]/div[2]/a[text()[contains(., "Website")]]/@href'
XPATH_WHITEPAPER = '/html/body/main/div/div[1]/div[1]/div/div[2]/div/div/div[1]/div[2]/div[2]/a[text()[contains(., "Whitepaper")]]/@href'
XPATH_PRE_SALE = '/html/body/main/div/div[1]/div[2]/div/div[3]/div/table/tbody/tr[./th[contains(., "Pre-Sale")]]/child::td[1]'
XPATH_TOKEN_SALE = '/html/body/main/div/div[1]/div[2]/div/div[3]/div/table/tbody/tr[./th[contains(., "Token Sale")]]/child::td[1]'
XPATH_COUNTRY = '/html/body/main/div/div[1]/div[2]/div/div[3]/div/table/tbody/tr[./th[contains(., "Country")]]/child::td[1]/a'
XPATH_PLATFORM = '//*[@id="tab-financial"]/div/div[1]/div/div/div/table/tbody/tr[./th[contains(., "Platform")]]/child::td[1]/a'
XPATH_TOKEN_PRICE = '//*[@id="tab-financial"]/div/div[1]/div/div/div/table/tbody/tr[./th[contains(., "Token Price")]]/child::td[1]'
XPATH_TOKEN_FOR_SALE = '//*[@id="tab-financial"]/div/div[1]/div/div/div/table/tbody/tr[./th[contains(., "Token for sale")]]/child::td[1]'
XPATH_TOKEN_SUPPLY = '//*[@id="tab-financial"]/div/div[1]/div/div/div/table/tbody/tr[./th[contains(., "Token supply")]]/child::td[1]'
XPATH_SOFT_CAP = '//*[@id="tab-financial"]/div/div[2]/div/div/div/table/tbody/tr[./th[contains(., "Soft cap")]]/child::td[1]'
XPATH_HARD_CAP = '//*[@id="tab-financial"]/div/div[2]/div/div/div/table/tbody/tr[./th[contains(., "Hard cap")]]/child::td[1]'
XPATH_ACCEPTING = '//*[@id="tab-financial"]/div/div[2]/div/div/div/table/tbody/tr[./th[contains(., "Accepting")]]/child::td[1]'
XPATH_RESTRICTED_COUNTRIES = '//*[@id="tab-financial"]/div/div[2]/div/div/div/table/tbody/tr[./th[contains(., "Restricted countries")]]/child::td[1]'
XPATH_KYC = '//*[@id="tab-financial"]/div/div[2]/div/div/div/table/tbody/tr[./th[contains(., "Know Your Customer")]]/child::td[1]'
XPATH_WHITELIST = '//*[@id="tab-financial"]/div/div[2]/div/div/div/table/tbody/tr[./th[contains(., "Whitelist")]]/child::td[1]'
XPATH_BONUS = '//*[@id="tab-financial"]/div/div[2]/div/div/div/table/tbody/tr[./th[contains(., "Bonus")]]/child::td[1]/p/text()'

MAX_PAGE = 163


def xpath_tolerant(response, xpath_selector):
    try:
        return response.xpath(xpath_selector).extract_first()
    except AttributeError:
        return None


def xpath_exract_first_text(response, xpath_selector):
    try:
        return response.xpath(xpath_selector + '/text()').extract_first().replace('\n', '')
    except AttributeError:
        return None


def parse_social_link(response, href_contains):
    try:
        return response.xpath(XPATH_SOCIAL_LINK.format(href_contains)).extract_first()
    except AttributeError:
        return None


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
            bounty_link = response.xpath(XPATH_BOUNTY_LINK).extract()[1]
        except Exception:
            bounty_link = None

        yield {
            'title': xpath_exract_first_text(response, XPATH_TITLE),
            'rating': xpath_exract_first_text(response, XPATH_RATING),

            'website': xpath_tolerant(response, XPATH_WEBSITE),
            'whitepaper': xpath_tolerant(response, XPATH_WHITEPAPER),

            'bitcointalk_link': parse_social_link(response, "bitcointalk.org"),
            'telegram_link': parse_social_link(response, "t.me"),
            'twitter_link': parse_social_link(response, "twitter.com"),
            'medium_link': parse_social_link(response, "medium.com"),
            'facebook_link': parse_social_link(response, "facebook.com"),
            'linkedin_link': parse_social_link(response, "linkedin.com"),
            'reddit_link': parse_social_link(response, "reddit.com"),
            'github_link': parse_social_link(response, "github.com"),
            'instagram_link': parse_social_link(response, "instagram.com"),

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
