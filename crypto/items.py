import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Join

from crypto.utils import clear_text, unify_title, unify_website
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
    'youtube_link': 'github.com',
}


def default_field():
    return scrapy.Field(
        input_processor=MapCompose(clear_text),
        output_processor=TakeFirst()
    )


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
    country = scrapy.Field(output_processor=TakeFirst())
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

    # # statistics
    hardcap = default_field()
    rating = default_field()
    number_of_tokens = default_field()
    raised_funds = default_field()
    softcap = default_field()

    # dates
    ico_date_range = default_field()
    pre_ico_date_range = default_field()
    total_ico_date_range = default_field()

    # extra
    accepting = default_field()
    bonus = scrapy.Field(
        input_processor=MapCompose(clear_text),
        ourput_processor=Join(separator='\n')
    )
    know_your_customer = default_field()
    platform = default_field()
    restricted_countries = default_field()
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
    whitelist = default_field()
