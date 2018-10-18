import base64
import hmac
import json
import requests

from scrapy.loader import ItemLoader

from crypto.items import SOCIAL_LINK_BASES, IcobenchOrganization
from crypto.utils import unify_title, unify_website


PRIVATE_KEY = b'd205be90-9907-4cb5-91ec-26cb5fa733a9'
PUBLIC_KEY = 'b6b629a3-56c2-48a0-861a-a03c11aed501'
PATH = 'icos/all'
PATH_PROFILE = 'ico/'
BASE_URL = 'https://icobench.com/api/v1/'
DEFAULT_DATE = '0000-00-00 00:00:00'


def generate_signature(params=''):
    _hash = hmac.new(PRIVATE_KEY, params.encode(), 'sha384')
    base = base64.b64encode(_hash.digest())
    return base


def make_request(path, params=None):
    if params is None:
        params = {}
    params = json.dumps(params)
    return json.loads(requests.post(
        BASE_URL + path,
        data=params,
        headers={
            'Content-Type': 'application/json',
            'Content-Length': str(len(params)),
            'X-ICObench-Key': PUBLIC_KEY,
            'X-ICObench-Sig': generate_signature(params)
        }
    ).text)


def main():
    res = make_request(PATH, {'page': 0})
    max_page = res['pages']
    output = res['results']
    for page in range(1, max_page + 1):
        output.extend(make_request(PATH, {'page': page})['results'])
        print('Icobench page{}/{}'.format(page, max_page))
    total = len(output)
    data = []
    for i, item in enumerate(output):
        print('Icobench {}/{}'.format(i, total))
        ico = make_request(PATH_PROFILE + str(item['id']))

        loader = ItemLoader(item=IcobenchOrganization())
        loader.add_value('name', unify_title(ico['name']))
        loader.add_value('site', unify_website(ico['links']['www']))
        loader.add_value('country', ico['country'])
        loader.add_value('whitepaper', ico['links']['whitepaper'])

        for key, value in SOCIAL_LINK_BASES.items():
            if ico['links']:
                k = [k for k in ico['links'].keys() if ico['links'][k] and value in ico['links'][k]]
                if len(k) == 1:
                    loader.add_value(key, ico['links'][k[0]])

        finance = ico['finance']
        loader.add_value('hardcap', finance['hardcap'])
        loader.add_value('softcap', finance['softcap'])
        loader.add_value('rating', ico['rating'])
        loader.add_value('number_of_tokens', finance['tokens'])
        loader.add_value('raised_funds_usd_value', finance['raised'])

        dates = ico['dates']
        loader.add_value('pre_ico_date_range_from', dates['preIcoStart'])
        loader.add_value('pre_ico_date_range_to', dates['preIcoEnd'])
        loader.add_value('ico_date_range_from', dates['icoStart'])
        loader.add_value('ico_date_range_to', dates['icoEnd'])
        loader.add_value(
            'total_ico_date_range_from',
            dates['preIcoStart'] if dates['preIcoStart'] != DEFAULT_DATE else dates['icoStart']
        )
        loader.add_value(
            'total_ico_date_range_to',
            dates['icoEnd'] if dates['icoEnd'] != DEFAULT_DATE else dates['preIcoEnd']
        )

        loader.add_value('accepting', finance['accepting'])
        loader.add_value('bonus', finance['bonus'])
        loader.add_value('description', ico['tagline'] + '. ' + ico['intro'])
        loader.add_value('team_description', ico['teamIntro'])
        loader.add_value('team_rating', ico['ratingTeam'])
        loader.add_value('product_rating', ico['ratingProduct'])
        loader.add_value('profile_rating', ico['ratingProfile'])
        loader.add_value('vision_rating', ico['ratingVision'])
        loader.add_value('token_name', finance['token'])
        loader.add_value('token_price', finance['price'])

        data.append(loader.load_item())

    return data


if __name__ == '__main__':
    main()
