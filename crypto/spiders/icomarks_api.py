import json
import requests

from scrapy.loader import ItemLoader

from crypto.items import Organization


# URL = 'https://icomarks.com/api/v1/icos' \
#       '?public_key=ahzTVzVTsQyVWKzs49QBc93nCmmPIIINFyau5nnSHPOn0YRWTREKgqgTEylXExG9' \
#       '&signature=jrOTHzNk9IGhxdSKqOP8b9OIWWYG69I%252BTEmdMds5d1hDwE30HfJc4P0r1syQEi2M'

URL = 'https://icomarks.com/api/v1/icos' \
      '?public_key=ahzTVzVTsQyVWKzs49QBc93nCmmPIIINFyau5nnSHPOn0YRWTREKgqgTEylXExG9' \
      '&page=2' \
      '&signature=nfTGEP8u0qVy8YsSiBi2z5CJKXbMwY5Dnyt%252BrnAa3%252BY9V5WCvncw8gqzJgvSS9SL'


def get_data():
    res = requests.get(URL)
    print(json.loads(res.text))
    return json.loads(res.text)['icos']


output = []

count = 0
data = get_data()
for item in data:
    loader = ItemLoader(item=Organization())
    loader.add_value('name', item['name'])
    loader.add_value('description', item['description'])
    loader.add_value('pre_ico_date_range_from', item['presale.start'])
    loader.add_value('pre_ico_date_range_to', item['presale.end'])
    loader.add_value('ico_date_range_from', item['main.start'])
    loader.add_value('ico_date_range_to', item['main.end'])
    loader.add_value('rating', item['rating'])
    output.append(loader.load_item())
    count += 1
    print(count)

print(output)

