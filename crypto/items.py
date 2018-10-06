import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join

from crypto.utils import clear_text, unify_title, unify_website, strip
from w3lib.html import remove_tags


SOCIAL_LINK_BASES = {
    'bitcointalk_link': 'bitcointalk.org',
    'facebook_link': 'facebook.com',
    'github_link': 'github.com',
    'instagram_link': 'instagram.com',
    'linkedin_link': 'linkedin.com',
    'medium_link': 'medium.com',
    'reddit_link': 'reddit.com',
    'slack_link': 'slack.com',
    'telegram_link': 't.me',
    'twitter_link': 'twitter.com',
    'youtube_link': 'youtube.com',
}


def default_field():
    return scrapy.Field(
        input_processor=MapCompose(clear_text, strip),
        output_processor=TakeFirst()
    )


def load_organization(response, xpaths, context=None):
        loader = ItemLoader(item=Organization(), response=response)

        for field in Organization.fields:
            if 'link' not in field:
                loader.add_xpath(field, xpaths.get(field.upper()))

        if type(context) == dict:
            for key, value in context.items():
                loader.add_value(key, value)

        # social links
        if 'SOCIAL_LINK' in xpaths:
            for key, value in SOCIAL_LINK_BASES.items():
                loader.add_xpath(key, xpaths['SOCIAL_LINK'].format(href_contains=value))

        return loader.load_item()


class Organization(scrapy.Item):
    # general
    name = scrapy.Field(
        input_processor=MapCompose(clear_text, unify_title),
        output_processor=TakeFirst()
    )
    site = scrapy.Field(
        input_processor=MapCompose(unify_website),
        output_processor=TakeFirst()
    )
    country = default_field()
    whitepaper = scrapy.Field(output_processor=TakeFirst())

    # social links
    bitcointalk_link = scrapy.Field(output_processor=TakeFirst())
    facebook_link = scrapy.Field(output_processor=TakeFirst())
    github_link = scrapy.Field(output_processor=TakeFirst())
    instagram_link = scrapy.Field(output_processor=TakeFirst())
    linkedin_link = scrapy.Field(output_processor=TakeFirst())
    medium_link = scrapy.Field(output_processor=TakeFirst())
    reddit_link = scrapy.Field(output_processor=TakeFirst())
    slack_link = scrapy.Field(output_processor=TakeFirst())
    telegram_link = scrapy.Field(output_processor=TakeFirst())
    twitter_link = scrapy.Field(output_processor=TakeFirst())
    youtube_link = scrapy.Field(output_processor=TakeFirst())

    # statistics
    hardcap = default_field()
    rating = default_field()
    number_of_tokens = default_field()
    raised_funds = default_field()
    softcap = default_field()

    # dates
    ico_date_range = default_field()
    pre_ico_date_range = default_field()
    total_ico_date_range = default_field()

    # extra_dates (icoholder has different structure and can display variety of stages)
    last_stage_date_start = default_field()
    last_stage_date_end = default_field()
    last_stage_name = default_field()
    last_stage_status = default_field()

    # extra
    accepting = default_field()
    bonus = scrapy.Field(
        input_processor=MapCompose(clear_text),
        output_processor=Join(separator='\n')
    )
    description = scrapy.Field(
        input_processor=MapCompose(clear_text),
        output_processor=Join()
    )
    goal = default_field()
    has_mvp = default_field()
    know_your_customer = default_field()
    latest_stage_name = default_field()
    platform = default_field()
    restricted_countries = default_field()
    status = default_field()
    team_description = default_field()
    team_rating = default_field()
    token_bonus_available = default_field()
    token_distribution = default_field()
    token_name = default_field()
    token_price = scrapy.Field(
        input_processor=MapCompose(clear_text, remove_tags),
        output_processor=Join()
    )
    tokens_for_sale = default_field()
    updated = default_field()
    whitelist = default_field()
