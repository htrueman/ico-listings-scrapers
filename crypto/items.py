import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose

from crypto.utils import clear_text, unify_title, unify_website


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
    hardcap = scrapy.Field(
        input_processor=MapCompose(clear_text),
        output_processor=TakeFirst()
    )
    rating = scrapy.Field(
        input_processor=MapCompose(clear_text),
        output_processor=TakeFirst()
    )
    number_of_tokens = scrapy.Field(
        input_processor=MapCompose(clear_text),
        output_processor=TakeFirst()
    )
    raised_funds = scrapy.Field(
        input_processor=MapCompose(clear_text),
        output_processor=TakeFirst()
    )
    softcap = scrapy.Field(
        input_processor=MapCompose(clear_text),
        output_processor=TakeFirst()
    )

    # dates
    ico_date_range = scrapy.Field(
        input_processor=MapCompose(clear_text),
        output_processor=TakeFirst()
    )
    pre_ico_date_range = scrapy.Field(
        input_processor=MapCompose(clear_text),
        output_processor=TakeFirst()
    )
    total_ico_date_range = scrapy.Field(
        input_processor=MapCompose(clear_text),
        output_processor=TakeFirst()
    )

    # extra
    accepting = scrapy.Field(
        input_processor=MapCompose(clear_text),
        output_processor=TakeFirst()
    )
    know_your_customer = scrapy.Field(
        input_processor=MapCompose(clear_text),
        output_processor=TakeFirst()
    )
    platform = scrapy.Field(
        input_processor=MapCompose(clear_text),
        output_processor=TakeFirst()
    )
    restricted_countries = scrapy.Field()
    team_description = scrapy.Field()
    team_rating = scrapy.Field()
    token_bonus_available = scrapy.Field()
    token_distribution = scrapy.Field()
    token_name = scrapy.Field()
    token_price = scrapy.Field()
    tokens_for_sale = scrapy.Field()
    whitelist = scrapy.Field()
