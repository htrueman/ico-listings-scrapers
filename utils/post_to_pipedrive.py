import json
from math import ceil

import tablib
import requests

from constants import OrgFields
from utils.remove_duplicates import RemoveDuplicateItems


class PostToPipedrive:
    base_path = 'https://relevant-dessert.pipedrive.com/v1/{item_type_plural}' \
                '?api_token=3b08b823cf50cc5e47baec700b369ba47f202bf0' \
                '&start={start}&limit=100&get_summary={get_summary}'
    pipedrive_orgs_step = 100  # max is 500
    pipedrive_orgs_file_name = 'pipedrive_orgs.json'

    def __init__(self,
         orgs_file_name=None,
         deals_file_name=None,
         members_file_name=None):

        orgs_file_name = 'non_duplicate_organizations.csv'

        pipedrive_orgs = requests.get(self.base_path.format(
            item_type_plural='organizations', start=0, get_summary=1))

        with open(self.pipedrive_orgs_file_name, 'w+') as f:
            f.write('')

        page_count = ceil(pipedrive_orgs.json()['additional_data']['summary']['total_count'] / 100)
        with open(self.pipedrive_orgs_file_name, 'a') as f:
            for i in range(page_count):
                next_start = i * self.pipedrive_orgs_step
                pipedrive_orgs = requests.get(self.base_path.format(
                    item_type_plural='organizations', start=next_start, get_summary=0))
                for org_index, org in enumerate(pipedrive_orgs.json()['data']):
                    if i == 0 and org_index == 0:
                        item_pattern = '[\n{},\n'
                    elif i + 1 == page_count and org_index + 1 == len(pipedrive_orgs.json()['data']):
                        item_pattern = '{}\n]'
                    else:
                        item_pattern = '{},\n'
                    f.write(item_pattern.format(json.dumps(org)))

        ndo_clean_file_name = RemoveDuplicateItems(
            self.pipedrive_orgs_file_name, orgs_file_name).ndo_clean_file_name

        orgs = tablib.Dataset().load(open(ndo_clean_file_name).read())
        self.orgs_json = json.loads(orgs.export('json'))

        # deals = tablib.Dataset().load(open(deals_file_name).read())
        # self.deals_json = json.loads(deals.export('json'))

        # members = tablib.Dataset().load(open(members_file_name).read())
        # self.deals_json = json.loads(members.export('json'))

        self.main()

    def main(self):
        # print('here')
        # existing_orgs = requests.get(self.base_path.format(item_type_plural='organizations'))
        # for d in existing_orgs.json()['data']:
        #     print(d)
        #     break

        org_dict = {
            'name': '',
            'open_deals_count': '',
            'related_open_deals_count': '',
            'closed_deals_count': '',
            'related_closed_deals_count': '',
            'email_messages_count': '',
            'people_count': '',
            'activities_count': '',
            'done_activities_count': '',
            'undone_activities_count': '',
            'reference_activities_count': '',
            'files_count': '',
            'notes_count': '',
            'followers_count': '',
            'won_deals_count': '',
            'related_won_deals_count': '',
            'lost_deals_count': '',
            'related_lost_deals_count': '',
            'active_flag': '',
            'category_id': '',
            'picture_id': '',
            'country_code': '',
            'first_char': '',
            'update_time': '',
            'add_time': '',
            'visible_to': '',
            'next_activity_date': '',
            'next_activity_time': '',
            'next_activity_id': '',
            'last_activity_id': '',
            'last_activity_date': '',
            'label': '',
            'address': '',
            'address_subpremise': '',
            'address_street_number': '',
            'address_route': '',
            'address_sublocality': '',
            'address_locality': '',
            'address_admin_area_level_1': '',
            'address_admin_area_level_2': '',
            'address_country': '',
            'address_postal_code': '',
            'address_formatted_address': '',

            'site': '',
            'country': '',
            'pre_ico_date_range_from': '',
            'pre_ico_date_range_to': '',
            'ico_date_range_from': '',
            'ico_date_range_to': '',
            'total_ico_date_range_from': '',
            'total_ico_date_range_to': '',
            'ico_total_rating': '',
            'team_rating': '',
            'vision_rating': '',
            'product_rating': '',
            'profile_ration': '',
            'description': '',
            'team_description': '',
            'token_price': '',
            'token_bonus_available': '',
            'number_of_tokens': '',
            'hardcap': '',
            'softcap': '',
            'raised_funds_usd_value': '',
            'raised_funds_usd_currency': '',
            'deals_value_value': '',
            'deals_value_currency': '',
            'token_name': '',
            'jurisdiction': '',
            'bitcointalk_link': '',
            'whitepaper': '',
            'youtube_link': '',
            'twitter_link': '',
            'about': '',
            'bonus': '',
            'reddit_link': '',
            'medium_link': '',
            'linkedin_link': '',
            'instagram_link': '',
            'facebook_link': '',
            'telegram_link': '',
            'pre_ico_date_start': '',
            'pre_ico_date_end': '',
            'start_date_of_ico_date_range': '',
            'tokens_for_sale': '',
            'token_distribution': '',
        }
        pipedrive_org_dict = OrgFields(**org_dict).get_dict_with_pipedrive_api_field_names()
        # print(pipedrive_org_dict)

        # response = requests.post(self.base_path.format(item_type_plural='organizations'), json={
        #     'name': 'AAAAAA'
        # })
        # print(response)


if __name__ == '__main__':
    PostToPipedrive()
