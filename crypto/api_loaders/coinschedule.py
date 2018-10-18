# NOT USED, NOT FINISHED, HAVE PARSER INSTEAD

import json

import requests
from scrapy.loader import ItemLoader

from crypto.items import Organization
from crypto.utils import unify_title, unify_website

urls = [
    "https://api.coinschedule.com/v2/crowdfunds/ended",
    "https://api.coinschedule.com/v2/crowdfunds/live",
    "https://api.coinschedule.com/v2/crowdfunds/upcoming"
]
headers = {
    'Authentication-Info': "Basic 2C7C1F77E1AEC74C",
    'Cache-Control': "no-cache",
}

output = []
for url in urls:
    response = requests.request("GET", url, headers=headers)
    data = json.loads(response.text)
    for item in data:
        loader = ItemLoader(item=Organization())
        loader.add_value('name', unify_title(item['ProjName']))
        loader.add_value('site', unify_website(item['website']))
        loader.add_value('country', item['country'])
        loader.add_value('whitepaper', item['country'])
