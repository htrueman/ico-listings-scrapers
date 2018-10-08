import requests

from constants import OrgFields
from utils.post_to_pipedrive import get_base_full_path


class PipedriveIssuesFix:
    base_path = 'https://exrates.pipedrive.com/v1/{item_type_plural}' \
                '?api_token=3b08b823cf50cc5e47baec700b369ba47f202bf0' \
                '{extra_params}'
    base_put_path = 'https://exrates.pipedrive.com/v1/{item_type_plural}/{id}' \
                    '?api_token=3b08b823cf50cc5e47baec700b369ba47f202bf0'
    pipedrive_get_step = 100
    exrates_id = 5079762

    def __init__(self):
        self.orgs_path_gen = get_base_full_path(
            self.base_path,
            self.pipedrive_get_step,
            'organizations'
        )
        self.deal_path_gen = get_base_full_path(
            self.base_path,
            self.pipedrive_get_step,
            'deals'
        )

        self.main()

    def main(self):
        self.move_address_field_to_site_field()
        self.change_deals_owner_to_exrates()
        self.check_if_website_accessible()

    def move_address_field_to_site_field(self):
        # organization
        for org_path in self.orgs_path_gen:
            pipedrive_orgs = requests.get(org_path)
            for org in pipedrive_orgs.json()['data']:
                if org['owner_name'] == 'Vadym Hevlich':
                    org[getattr(OrgFields, 'site')] = org[getattr(OrgFields, 'address')]
                    org[getattr(OrgFields, 'address')] = None
                    requests.put(
                        self.base_put_path.format(
                            item_type_plural='organizations',
                            id=org['id']
                        ),
                        json=org
                    )

    def change_deals_owner_to_exrates(self):
        # deal
        for deal_path in self.deal_path_gen:
            pipedrive_deals = requests.get(deal_path)
            for deal in pipedrive_deals.json()['data']:
                if deal['owner_name'] == 'Vadym Hevlich':
                    deal['owner_id'] = self.exrates_id
                    requests.put(
                        self.base_put_path.format(
                            item_type_plural='deals',
                            id=deal['id']
                        ),
                        json=deal
                    )

    def check_if_website_accessible(self):
        for org_path in self.orgs_path_gen:
            pipedrive_orgs = requests.get(org_path)
            for org in pipedrive_orgs.json()['data']:
                status_code = requests.get(org[getattr(OrgFields, 'site')]).status_code
                if status_code >= 400:
                    org[getattr(OrgFields, 'name')] \
                        = org[getattr(OrgFields, 'name')] + 'NOT ACCESSIBLE'
                    requests.put(
                        self.base_put_path.format(
                            item_type_plural='organizations',
                            id=org['id']
                        ),
                        json=org
                    )


if __name__ == '__main__':
    PipedriveIssuesFix()
