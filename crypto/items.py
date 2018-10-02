import scrapy


class Organization(scrapy.Item):
    # general
    country = scrapy.Field()
    name = scrapy.Field()
    site = scrapy.Field()

    # social links
    bitcointalk_link = scrapy.Field()
    linkedIn_link = scrapy.Field()
    medium_link = scrapy.Field()
    reddit_link = scrapy.Field()
    telegram_Link = scrapy.Field()
    youtube_link = scrapy.Field()

    # statistics
    hardcap = scrapy.Field()
    rating = scrapy.Field()
    number_of_tokens = scrapy.Field()
    raised_funds = scrapy.Field()
    softcap = scrapy.Field()

    # dates
    ico_date_range = scrapy.Field()
    pre_ico_date_range = scrapy.Field()
    total_ico_date_range = scrapy.Field()

    # extra
    team_description = scrapy.Field()
    team_rating = scrapy.Field()
    token_bonus_available = scrapy.Field()
    token_distribution = scrapy.Field()
    token_name = scrapy.Field()
    token_price = scrapy.Field()
    tokens_for_sale = scrapy.Field()
