import base64
import collections
import hmac
from urllib.parse import urlencode, quote_plus


import json
import requests
import time

from scrapy.loader import ItemLoader

from crypto.items import Organization, SOCIAL_LINK_BASES
from crypto.utils import unify_title, unify_website

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
        url = generate_url(path, params)
        try:
            time.sleep(0.5)
            res = requests.get(url)
            res_json = json.loads(res.content.decode())
        except Exception:
            continue

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
    total = len(lst)
    for ind, i in enumerate(lst):
        print('Icomarks: {} of {}'.format(ind, total))
        item = make_request(PATH1 + i['id'], {})

        loader = ItemLoader(item=Organization())
        loader.add_value('name', unify_title(item['name']))
        loader.add_value('site', unify_website(item['website']))
        loader.add_value('country', item['country'])
        loader.add_value('whitepaper', item['whitepaper'])

        for key, value in SOCIAL_LINK_BASES.items():
            if item['social']:
                k = [k for k in item['social'].keys() if item['social'][k] and value in item['social'][k]]
                if len(k) == 1:
                    loader.add_value(key, item['social'][k[0]])

        loader.add_value('hardcap', item['hard.cap'])
        loader.add_value('icomarks_rating', item['rating'])
        loader.add_value('number_of_tokens', item['total.tokens'])
        loader.add_value('raised_funds_usd_value', item['raised'])
        loader.add_value('softcap', item['soft.cap'])

        loader.add_value('pre_ico_date_range_from', item['presale.start'])
        loader.add_value('pre_ico_date_range_to', item['presale.end'])
        loader.add_value('ico_date_range_from', item['main.start'])
        loader.add_value('ico_date_range_to', item['main.end'])
        loader.add_value('total_ico_date_range_from', item['presale.start'] or item['main.start'])
        loader.add_value('total_ico_date_range_to', item['main.end'] or item['presale.end'])

        loader.add_value('accepting', item['accepting'])
        loader.add_value('bonus', item['bonus'])
        loader.add_value('description', item['description'])
        loader.add_value('token_name', item['ticker'])
        loader.add_value('tokens_for_sale', item['available.for.sale'])
        loader.add_value('token_price', item['main.price'] or item['presale.price'])

        loader.add_value('source', 'icomarks')
        loader.add_value('is_parsed', 'false')

        output.append(loader.load_item())
    return output


if __name__ == '__main__':
    main()
