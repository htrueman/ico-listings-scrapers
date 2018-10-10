import base64
import hmac
from urllib.parse import urlencode, quote_plus

PRIVATE_KEY = b'qEAKaFgIyMrFc1kcShDbP13QGst49w9XZ0dWE3E4fqP7dYeVkbou2OgbSC20u'
PUBLIC_KEY = 'ahzTVzVTsQyVWKzs49QBc93nCmmPIIINFyau5nnSHPOn0YRWTREKgqgTEylXExG9'


def generate_signature(path, params):
    path = path.replace('/', '')
    _hash = hmac.new(PRIVATE_KEY, (path + '?' + urlencode(params)).encode())
    base = base64.b64encode(_hash.digest())
    return quote_plus(base)


def generate_url(path, params=None):
    if not params:
        params = {}
    params["public_key"] = PUBLIC_KEY
    params["signature"] = generate_signature(path, params)
    return 'https://icomarks.com/api/v1/' + path + '?' + urlencode(params)


print(generate_url('icos'))
