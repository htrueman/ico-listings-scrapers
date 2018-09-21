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
    return title.split('(')[0].strip().lower().title()


def unify_website(website):
    return website.split('?')[0]
