import base64
import hmac
from urllib.parse import urlencode, quote_plus


import json
import requests

from scrapy.loader import ItemLoader

from crypto.items import Organization


PRIVATE_KEY = b'qEAKaFgIyMrFc1kcShDbP13QGst49w9XZ0dWE3E4fqP7dYeVkbou2OgbSC20u'
PUBLIC_KEY = 'ahzTVzVTsQyVWKzs49QBc93nCmmPIIINFyau5nnSHPOn0YRWTREKgqgTEylXExG9'
PATH = 'ico'

def generate_signature(path, params):
    path = path.replace('/', '')
    _hash = hmac.new(PRIVATE_KEY, (path + '?' + urlencode(params)).encode(), 'sha384')
    base = base64.b64encode(_hash.digest())
    return quote_plus(base)


def generate_url(path=PATH, params=None):
    if not params:
        params = {}
    params["public_key"] = PUBLIC_KEY
    params["signature"] = generate_signature(path, params)
    return 'https://icomarks.com/api/v1/' + path + '?' + urlencode(params)


print(generate_url('icos'))


def get_data():
    res = requests.get(
        generate_url()
    )
    res_json = json.loads(res.text)
    max_page = int(res_json['total_pages'])
    data = res_json['icos']

    for page in range(1, max_page + 1):
        res = requests.get(generate_url(params={'page': page}))
        data.append(json.loads(res.text)['icos'])
    return data


def main():
    print(len(get_data()))

# for item in data:
#     loader = ItemLoader(item=Organization())
#     loader.add_value('name', item['name'])
#     output.append(loader.load_item())
#     count += 1
#     print(count)
#
# print(output)
#
