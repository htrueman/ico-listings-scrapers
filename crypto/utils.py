from datetime import datetime

import tldextract


def xpath_tolerant(response, xpath_selector):
    try:
        return response.xpath(xpath_selector).extract_first()
    except AttributeError:
        return None


def xpath_exract_first_text(response, xpath_selector):
    try:
        return response.xpath(xpath_selector + '/text()').extract_first().replace('\n', '')
    except AttributeError:
        return None


def parse_social_link(response, xpath_social_link, href_contains):
    try:
        return response.xpath(xpath_social_link.format(href_contains=href_contains)).extract_first()
    except AttributeError:
        return None


def unify_title(title):
    return title.split('(')[0]\
                .strip()\
                .lower()\
                .replace('network', '')\
                .replace('ico', '')\
                .replace('pre-ico', '')\
                .replace('platform', '')\
                .strip()\
                .title()


def unify_website(website):
    try:
        extracted = tldextract.extract(website)
        # return '{}.{}'.format(extracted.domain, extracted.suffix)
        return 'https://{}.{}/'.format(extracted.domain, extracted.suffix)
    except TypeError:
        return ''


def clear_text(value):
    return str(value).replace('\n', '').replace('\t', '')


def strip(string):
    return string.strip()


def clear_date(date):
    return date.replace('th', '').replace('st', '').replace('nd', '').replace('rd', '').replace('Augu ', 'August ')


def skip_date(date):
    return None if date == '0000-00-00 00:00:00' else date


def to_common_format(date, original_formats):
    for original_format in original_formats:
        try:
            return datetime.strptime(date, original_format).strftime('%Y-%m-%d')
        except ValueError:
            continue
    return ''
