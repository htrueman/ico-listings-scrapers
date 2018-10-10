import base64
import collections
import hmac
from pprint import pprint
from urllib.parse import urlencode, quote_plus


import json
import requests
import time

from scrapy.loader import ItemLoader

from crypto.items import Organization


PRIVATE_KEY = b'qEAKaFgIyMrFc1kcShDbP13QGst49w9XZ0dWE3E4fqP7dYeVkbou2OgbSC20u'
PUBLIC_KEY = 'ahzTVzVTsQyVWKzs49QBc93nCmmPIIINFyau5nnSHPOn0YRWTREKgqgTEylXExG9'
PATH = 'icos'
PATH1 = 'ico/'


def generate_signature(path, params):
    # path = path.replace('/', '')
    _hash = hmac.new(PRIVATE_KEY, (path + '?' + urlencode(params)).encode(), 'sha384')
    base = base64.b64encode(_hash.digest())
    return quote_plus(base)


def generate_url(path=PATH, params=None):
    if not params:
        params = {}

    params = collections.OrderedDict(sorted(params.items()))
    params["public_key"] = PUBLIC_KEY
    params["signature"] = generate_signature(path, params)
    return 'https://icomarks.com/api/v1/' + path + '?' + urlencode(params)


def make_request(path, params):
    retries = 10
    for _ in range(retries):
        print('Retrying: ', _)
        url = generate_url(path, params)
        res = requests.get(url)
        res_json = json.loads(res.content.decode())

        if 'error' in res_json and res_json['error'] and res_json['error']['code'] != '485':
            time.sleep(1)
            continue
        else:
            return res_json


def get_data():
    res = make_request(PATH, params={'page': 1})
    max_page = int(res['total_pages'])
    data = res['icos']

    for page in range(2, max_page + 1):
        new = make_request(PATH, params={'page': page})
        data.extend(new['icos'])

    return data


def main():
    output = []
    lst = get_data()
    for i in lst[:10]:
        item = make_request(PATH1 + i['id'], {})
        loader = ItemLoader(item=Organization())
        loader.add_value('name', item['name'])
        loader.add_value('site', item['website'])
        loader.add_value('country', item['country'])
        output.append(loader.load_item())



main()

# for item in data:
#     loader = ItemLoader(item=Organization())
#     loader.add_value('name', item['name'])
#     output.append(loader.load_item())
#     count += 1
#     print(count)
#
# print(output)
#
