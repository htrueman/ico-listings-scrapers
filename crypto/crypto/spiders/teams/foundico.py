from ...utils import unify_title
from ..foundico import FoundicoBaseSpider


class FoundicoSpider(FoundicoBaseSpider):
    name = 'foundico_members'

    def parse_company_page(self, response):
        base_path = '//div[contains(., "row")]//div[contains(@class, "ico-team-unit")]'

        full_names = response.xpath('{}//h4//a/text()'.format(base_path)).extract()
        positions = response.xpath('{}//p/text()'.format(base_path)).extract()
        links = response.xpath('{}//p/following::span[1]/a/@href'.format(base_path)).extract()

        for name, position, link in zip(full_names, positions, links):
            yield {
                'ico_title': unify_title(response.xpath('//h1/text()').extract_first()),
                'full_name': name,
                'position': position,
                'linkedin': link
            }
