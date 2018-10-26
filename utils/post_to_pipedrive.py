import json
import datetime
from math import ceil

import requests

from utils.constants import OrgFields, API_SOURCES
from utils.merge_items import MergeItems
from utils.remove_duplicates import RemoveDuplicateItems


def get_base_full_path(base_path, pipedrive_get_step, item_type_plural):
    base_get_path = base_path.format(
        item_type_plural=item_type_plural,
        extra_params='&start={start}&limit=100&get_summary={get_summary}')
    if item_type_plural == 'notes':
        more_items_in_collection = True
        next_notes_start = 0

        while more_items_in_collection:
            yield base_get_path.format(start=next_notes_start, get_summary=0)

            pipedrive_notes = requests.get(base_get_path.format(start=next_notes_start, get_summary=1))

            more_items_in_collection = pipedrive_notes\
                .json()['additional_data']['pagination']['more_items_in_collection']
            if more_items_in_collection:
                next_notes_start += pipedrive_get_step
    else:
        pipedrive_orgs = requests.get(base_get_path.format(start=0, get_summary=1))

        page_count = ceil(pipedrive_orgs.json()['additional_data']['summary']['total_count'] / 100)
        for i in range(page_count):
            next_start = i * pipedrive_get_step
            yield base_get_path.format(start=next_start, get_summary=0)


class PostToPipedrive:
    base_path = 'https://exrates.pipedrive.com/v1/{item_type_plural}' \
                '?api_token=3b08b823cf50cc5e47baec700b369ba47f202bf0' \
                '{extra_params}'
    pipedrive_orgs_step = 100  # max is 500
    pipedrive_orgs_file_name = 'pipedrive_orgs.json'

    def __init__(self,
                 orgs_file_name=None,
                 members_file_name=None):

        base_get_path = self.base_path.format(
            item_type_plural='organizations',
            extra_params='&start={start}&limit=100&get_summary={get_summary}')
        pipedrive_orgs = requests.get(base_get_path.format(start=0, get_summary=1))

        with open(self.pipedrive_orgs_file_name, 'w+') as f:
            f.write('')

        page_count = ceil(pipedrive_orgs.json()['additional_data']['summary']['total_count'] / 100)
        with open(self.pipedrive_orgs_file_name, 'a') as f:
            for i in range(page_count):
                next_start = i * self.pipedrive_orgs_step
                pipedrive_orgs = requests.get(base_get_path.format(
                    start=next_start, get_summary=0))
                if pipedrive_orgs.json()['data']:
                    for org_index, org in enumerate(pipedrive_orgs.json()['data']):
                        if i == 0 and org_index == 0:
                            item_pattern = '[\n{},\n'
                        elif i + 1 == page_count and org_index + 1 == len(pipedrive_orgs.json()['data']):
                            item_pattern = '{}\n]'
                        else:
                            item_pattern = '{},\n'
                        f.write(item_pattern.format(json.dumps(org)))

        print(orgs_file_name)
        self.orgs_path_gen = get_base_full_path(
            self.base_path,
            self.pipedrive_orgs_step,
            'organizations'
        )
        self.deal_path_gen = get_base_full_path(
            self.base_path,
            self.pipedrive_orgs_step,
            'deals'
        )
        ndo_file_name = MergeItems(orgs_file_name).organizations_file_name
        # ndo_clean_file_name = RemoveDuplicateItems(
        #     self.pipedrive_orgs_file_name, ndo_file_name).ndo_clean_file_name
        self.orgs_json = json.loads(open(ndo_file_name).read())

        self.main()

    @staticmethod
    def get_deal_pipeline(is_parsed):
        # 2-ico - API: id = 5
        # 3-ico - parsing: id = 6
        if is_parsed:
            pipeline_id = 6
        else:
            pipeline_id = 5
        return pipeline_id

    def main(self):
        pipedrive_orgs = []
        for org_path in self.orgs_path_gen:
            pipedrive_orgs.extend(requests.get(org_path).json()['data'])

        for org_dict in self.orgs_json:
            pipedrive_org_dict = OrgFields(**org_dict).get_dict_with_pipedrive_api_field_names()
            is_parsed = json.loads(pipedrive_org_dict.pop('is_parsed'))

            exists = False
            for pipedrive_org in pipedrive_orgs:

                if pipedrive_org.get(getattr(OrgFields, 'name')) \
                        == pipedrive_org_dict.get(getattr(OrgFields, 'name')) \
                        or pipedrive_org.get(getattr(OrgFields, 'site')) \
                        == pipedrive_org_dict.get(getattr(OrgFields, 'site')):
                    if pipedrive_org[getattr(OrgFields, 'source')] in API_SOURCES:
                        pipedrive_org_dict.update(
                            {k: v for k, v in pipedrive_org.items()}
                        )
                        is_parsed = False
                    elif pipedrive_org_dict[getattr(OrgFields, 'source')] in API_SOURCES:
                        pipedrive_org.update(
                            {k: v for k, v in pipedrive_org_dict.items()}
                        )
                        is_parsed = False
                    else:
                        pipedrive_org_dict.update(
                            {k: v for k, v in pipedrive_org_dict.items()
                             if isinstance(pipedrive_org_dict[k], str) and len(v) > len(pipedrive_org_dict[k])}
                        )
                    requests.put(
                        self.base_path.format(
                            item_type_plural='organizations/{}'.format(pipedrive_org['id']),
                            extra_params=''),
                        json=pipedrive_org_dict)
                    exists = True
                    break

            if not exists:
                response = requests.post(
                    self.base_path.format(item_type_plural='organizations', extra_params=''),
                    json=pipedrive_org_dict)

                if response.status_code == 200:
                    org_data = response.json()['data']

                    pipedrive_deal_dict = {
                        'title': org_data['name'] + ' - deal',
                        'org_id': org_data['id'],
                        'pipeline_id': self.get_deal_pipeline(is_parsed)
                    }
                    requests.post(self.base_path.format(item_type_plural='deals', extra_params=''),
                                  json=pipedrive_deal_dict)
        print('Done')


if __name__ == '__main__':
    PostToPipedrive()
