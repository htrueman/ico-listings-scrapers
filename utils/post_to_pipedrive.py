import json
import datetime
from math import ceil

import tablib
import requests

from constants import OrgFields
from utils.merge_items import MergeItems
from utils.remove_duplicates import RemoveDuplicateItems
from utils.split_between_pipelines import SpitDeals


def get_base_full_path(base_path, pipedrive_get_step, item_type_plural):
    base_get_path = base_path.format(
        item_type_plural=item_type_plural,
        extra_params='&start={start}&limit=100&get_summary={get_summary}')
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
                for org_index, org in enumerate(pipedrive_orgs.json()['data']):
                    if i == 0 and org_index == 0:
                        item_pattern = '[\n{},\n'
                    elif i + 1 == page_count and org_index + 1 == len(pipedrive_orgs.json()['data']):
                        item_pattern = '{}\n]'
                    else:
                        item_pattern = '{},\n'
                    f.write(item_pattern.format(json.dumps(org)))

        print(orgs_file_name)
        ndo_file_name = MergeItems(orgs_file_name).organizations_file_name
        ndo_clean_file_name = RemoveDuplicateItems(
            self.pipedrive_orgs_file_name, ndo_file_name).ndo_clean_file_name
        orgs = tablib.Dataset().load(open(ndo_clean_file_name).read())
        self.orgs_json = json.loads(orgs.export('json'))

        # deals_file_name = SpitDeals(ndo_clean_file_name).deals_file_name
        # deals = tablib.Dataset().load(open(deals_file_name).read())
        # self.deals_json = json.loads(deals.export('json'))

        # members = tablib.Dataset().load(open(members_file_name).read())
        # self.deals_json = json.loads(members.export('json'))

        self.main()

    @staticmethod
    def get_deal_pipeline(org):
        """
        Get deal pipeline by organization ICO date.
        All deals are splitted between '2-ico-in-progress' and '3-ico-finished' pipelines.
        """
        # 3-ico-finished : id = 3
        # 2-ico-in-progress : id = 1

        ico_date_range_to = org.get(getattr(OrgFields, 'ico_date_range_to'))
        total_ico_date_range_to = org.get(getattr(OrgFields, 'total_ico_date_range_to'))
        pre_ico_date_range_to = org.get(getattr(OrgFields, 'pre_ico_date_range_to'))

        pipeline_id = 3
        for date_str in [ico_date_range_to, total_ico_date_range_to, pre_ico_date_range_to]:
            if datetime.datetime.strptime(date_str, '%Y-%m-%d') <= datetime.datetime.now():
                pipeline_id = 1
        return pipeline_id

    def main(self):
        for org_dict in self.orgs_json:
            # print(org_dict)
            pipedrive_org_dict = OrgFields(**org_dict).get_dict_with_pipedrive_api_field_names()
            response = requests.post(
                self.base_path.format(item_type_plural='organizations', extra_params=''),
                json=pipedrive_org_dict)

            org_data = response.json()['data']

            pipedrive_deal_dict = {
                'title': org_data['name'] + ' - deal',
                'org_id': org_data['id'],
                'pipeline_id': self.get_deal_pipeline(org_data)
            }
            requests.post(self.base_path.format(item_type_plural='deals', extra_params=''),
                          json=pipedrive_deal_dict)
        print('Done')


if __name__ == '__main__':
    PostToPipedrive()
