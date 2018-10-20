from functools import partial

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Compose

from crypto.utils import clear_text, unify_title, unify_website, strip, to_common_format, clear_date, skip_date
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


def default_field(extra=None):
    if not extra:
        extra = []
    return scrapy.Field(
        input_processor=MapCompose(clear_text, strip, *extra),
        output_processor=TakeFirst()
    )


def default_field_join(extra=None):
    if not extra:
        extra = []
    return scrapy.Field(
        input_processor=MapCompose(clear_text, strip),
        output_processor=Compose(Join(separator=''), *extra)
    )


def take_first_field():
    return scrapy.Field(output_processor=TakeFirst())


def load_organization(response, xpaths, context=None, item_cls=None):

        if not item_cls:
            item_cls = Organization
        loader = ItemLoader(item=item_cls(), response=response)

        for field in item_cls.fields:
            if 'link' not in field:
                loader.add_xpath(field, xpaths.get(field.upper()))

        if type(context) == dict:
            for key, value in context.items():
                loader.add_value(key, value)

        # social links
        if 'SOCIAL_LINK' in xpaths:
            for key, value in SOCIAL_LINK_BASES.items():
                loader.add_xpath(key, xpaths['SOCIAL_LINK'].format(href_contains=value))
        loader.add_value('raised_funds_usd_currency', 'USD')
        loader.add_value('is_parsed', 'true')

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
    whitepaper = take_first_field()

    # social links
    bitcointalk_link = take_first_field()
    facebook_link = take_first_field()
    github_link = take_first_field()
    instagram_link = take_first_field()
    linkedin_link = take_first_field()
    medium_link = take_first_field()
    reddit_link = take_first_field()
    slack_link = take_first_field()
    telegram_link = take_first_field()
    twitter_link = take_first_field()
    youtube_link = take_first_field()

    # statistics
    hardcap = default_field()
    number_of_tokens = default_field()
    raised_funds_usd_value = default_field()
    raised_funds_usd_currency = default_field()
    softcap = default_field()

    # dates yyyy-mm-dd
    pre_ico_date_range_from = default_field()
    pre_ico_date_range_to = default_field()

    ico_date_range_from = default_field()
    ico_date_range_to = default_field()

    total_ico_date_range_from = default_field()
    total_ico_date_range_to = default_field()

    # (icoholder has different structure and can display variety of stages)
    # last_stage_name = default_field()
    # last_stage_status = default_field()

    # extra
    accepting = default_field()
    # airdrop_program = default_field()
    # bounty_program = default_field()
    bonus = scrapy.Field(
        input_processor=MapCompose(clear_text),
        output_processor=Join(separator='\n')
    )
    description = scrapy.Field(
        input_processor=MapCompose(clear_text),
        output_processor=Join()
    )
    # goal = default_field()
    # has_mvp = default_field()
    # know_your_customer = default_field()
    # platform = default_field()
    # restricted_countries = default_field()
    # status = default_field()

    team_description = default_field()
    token_bonus_available = default_field()
    token_distribution = default_field()
    token_name = default_field()
    token_price = scrapy.Field(
        input_processor=MapCompose(clear_text, remove_tags),
        output_processor=Join()
    )
    tokens_for_sale = default_field()
    # updated = default_field()
    # whitelist = default_field()

    source = take_first_field()
    is_parsed = default_field()

    # rating

    # icobench
    rating = default_field()
    product_rating = default_field()
    profile_rating = default_field()
    team_rating = default_field()
    vision_rating = default_field()

    # other
    baseinfo_rating = default_field()
    trackico_rating = default_field()
    icomarks_rating = default_field()

    # icobazaar
    icobazaar_rating = default_field()
    icobazaar_site_rating = default_field()
    icobazaar_team_rating = default_field()
    icobazaar_idea_rating = default_field()
    icobazaar_tech_rating = default_field()
    icobazaar_media_rating = default_field()
    icobazaar_users_rating = default_field()

    # foundico
    foundico_rating = default_field()
    foundico_info_rating = default_field()
    foundico_finance_rating = default_field()
    foundico_product_rating = default_field()
    foundico_team_rating = default_field()
    foundico_marketing_rating = default_field()

    # icoholder
    icoholder_rating = default_field()
    icoholder_profile_rating = default_field()
    icoholder_team_rating = default_field()
    icoholder_vision_rating = default_field()
    icoholder_product_rating = default_field()
    icoholder_potential_rating = default_field()
    icoholder_activity_rating = default_field()


class BaseInfoOrganization(Organization):
    original_formats = ['%d.%m.%Y']

    date_processor = partial(to_common_format, original_formats=original_formats)

    pre_ico_date_range_from = default_field(extra=[date_processor])
    pre_ico_date_range_to = default_field(extra=[date_processor])

    ico_date_range_from = default_field(extra=[date_processor])
    ico_date_range_to = default_field(extra=[date_processor])

    total_ico_date_range_from = default_field(extra=[date_processor])
    total_ico_date_range_to = default_field(extra=[date_processor])


class IcoholderOrganization(Organization):
    original_formats = ['%b %d, %Y', '%b, %Y']

    date_processor = partial(to_common_format, original_formats=original_formats)

    pre_ico_date_range_from = default_field(extra=[date_processor])
    pre_ico_date_range_to = default_field(extra=[date_processor])

    ico_date_range_from = default_field(extra=[date_processor])
    ico_date_range_to = default_field(extra=[date_processor])

    total_ico_date_range_from = default_field(extra=[date_processor])
    total_ico_date_range_to = default_field(extra=[date_processor])


class CoinscheduleOrganization(Organization):
    original_formats = ['%B %-d %Y %H:%M UTC', '%B %d %Y %H:%M UTC', '%B %-d %Y', '%B %d %Y']

    date_processor = partial(to_common_format, original_formats=original_formats)

    pre_ico_date_range_from = default_field(extra=[clear_date, date_processor])
    pre_ico_date_range_to = default_field(extra=[clear_date, date_processor])

    ico_date_range_from = default_field(extra=[clear_date, date_processor])
    ico_date_range_to = default_field(extra=[clear_date, date_processor])

    total_ico_date_range_from = default_field(extra=[clear_date, date_processor])
    total_ico_date_range_to = default_field(extra=[clear_date, date_processor])


class FoundicoOrganization(Organization):
    original_formats = ['%Y%b %dth']

    date_processor = partial(to_common_format, original_formats=original_formats)

    pre_ico_date_range_from = default_field_join(extra=[date_processor])
    pre_ico_date_range_to = default_field_join(extra=[date_processor])

    ico_date_range_from = default_field_join(extra=[date_processor])
    ico_date_range_to = default_field_join(extra=[date_processor])

    total_ico_date_range_from = default_field_join(extra=[date_processor])
    total_ico_date_range_to = default_field_join(extra=[date_processor])


class IcobenchOrganization(Organization):
    original_formats = ['%Y-%m-%d %H:%M:%S']

    date_processor = partial(to_common_format, original_formats=original_formats)

    pre_ico_date_range_from = default_field_join(extra=[skip_date, date_processor])
    pre_ico_date_range_to = default_field_join(extra=[skip_date, date_processor])

    ico_date_range_from = default_field_join(extra=[skip_date, date_processor])
    ico_date_range_to = default_field_join(extra=[skip_date, date_processor])

    total_ico_date_range_from = default_field_join(extra=[skip_date, date_processor])
    total_ico_date_range_to = default_field_join(extra=[skip_date, date_processor])
