import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from utils.constants import OrgFields
from utils.post_to_pipedrive import get_base_full_path


class PipedriveIssuesFix:
    base_path = 'https://exrates.pipedrive.com/v1/{item_type_plural}' \
                '?api_token=3b08b823cf50cc5e47baec700b369ba47f202bf0' \
                '{extra_params}'
    base_put_path = 'https://exrates.pipedrive.com/v1/{item_type_plural}/{id}' \
                    '?api_token=3b08b823cf50cc5e47baec700b369ba47f202bf0'
    get_org_deals_path = 'https://exrates.pipedrive.com/v1/organizations/{id}/deals' \
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

        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        self.session = session

        self.main()

    def main(self):
        # self.move_address_field_to_site_field()
        # self.change_deals_owner_to_exrates()
        # self.check_if_website_accessible()
        # self.delete_old_orgs()
        self.delete_duplicate_orgs_and_deals()

    def delete_duplicate_orgs_and_deals(self):
        API_SOURCES = ['icobench', 'icomarks']
        pipedrive_notes = []
        note_path_gen = get_base_full_path(
            self.base_path,
            self.pipedrive_get_step,
            'notes'
        )
        for note_path in note_path_gen:
            pipedrive_notes.extend(requests.get(note_path).json()['data'])
        org_ids_to_not_delete = list(map(lambda n: n['org_id'], pipedrive_notes))
        deal_ids_to_not_delete = list(map(lambda n: n['deal_id'], pipedrive_notes))

        pipedrive_orgs = []
        for org_path in self.orgs_path_gen:
            print(org_path)
            pipedrive_orgs.extend(requests.get(org_path).json()['data'])

        for index, org1 in enumerate(pipedrive_orgs):
            for org2 in pipedrive_orgs:
                if org1['id'] != org2['id'] \
                        and org1['owner_name'] == 'Vadym Hevlich' and org2['owner_name'] == 'Vadym Hevlich' and (
                        org1[getattr(OrgFields, 'name')] == org2[getattr(OrgFields, 'name')]
                        or org1[getattr(OrgFields, 'site')] == org2[getattr(OrgFields, 'site')]):
                    id1 = org1['id']
                    id2 = org2['id']
                    if org2[getattr(OrgFields, 'source')] in API_SOURCES:
                        id1 = org2['id']
                        id2 = org1['id']

                    org1_deals = self.session.get(
                        self.get_org_deals_path.format(
                            id=id1
                        )
                    ).json()['data']

                    org2_deals = self.session.get(
                        self.get_org_deals_path.format(
                            id=id2
                        )
                    ).json()['data']

                    if org1_deals and org2_deals:
                        for deal1, deal2 in zip(org1_deals, org2_deals):
                            # delete duplicate deals, left one parsed from API
                            if deal1['id'] != deal2['id']:
                                deal_to_delete_id = None
                                if deal2['id'] not in deal_ids_to_not_delete:
                                    deal_to_delete_id = deal2['id']
                                elif deal1['id'] not in deal_ids_to_not_delete:
                                    deal_to_delete_id = deal1['id']

                                if deal_to_delete_id:
                                    self.session.delete(
                                        self.base_put_path.format(
                                            item_type_plural='deals',
                                            id=deal_to_delete_id)
                                    )

                    # delete duplicate orgs, left one parsed from API
                    org_to_delete_id = None
                    if id2 not in org_ids_to_not_delete:
                        org_to_delete_id = id2
                    elif id1 not in org_ids_to_not_delete:
                        org_to_delete_id = id1

                    if org_to_delete_id:
                        self.session.delete(
                            self.base_put_path.format(
                                item_type_plural='organizations',
                                id=org_to_delete_id)
                        )
                        print('orgs:', '{}/{}'.format(index, len(pipedrive_orgs)))

    def move_address_field_to_site_field(self):
        # organization
        for org_path in self.orgs_path_gen:
            pipedrive_orgs = requests.get(org_path)
            for org in pipedrive_orgs.json()['data']:
                if org['owner_name'] == 'Vadym Hevlich' and not org[getattr(OrgFields, 'site')]:
                    org[getattr(OrgFields, 'site')] = org[getattr(OrgFields, 'address')]
                    org[getattr(OrgFields, 'address')] = None
                    self.session.put(
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
                    self.session.put(
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
                has_changes = False
                if org[getattr(OrgFields, 'site')] and 'icobench' not in org[getattr(OrgFields, 'site')]:
                    if not ('https' in org[getattr(OrgFields, 'site')] or 'http' in org[getattr(OrgFields, 'site')]):
                        org[getattr(OrgFields, 'site')] = 'https://' + org[getattr(OrgFields, 'site')] + '/'
                        has_changes = True
                    elif 'https' in org[getattr(OrgFields, 'site')] and 'http' in org[getattr(OrgFields, 'site')]:
                        org[getattr(OrgFields, 'site')] = org[getattr(OrgFields, 'site')].replace('http://', '')
                        has_changes = True
                    try:
                        response = requests.get(org[getattr(OrgFields, 'site')])
                        if response.status_code >= 400 and org['owner_name'] == 'Vadym Hevlich':
                            d = self.session.delete(
                                self.base_put_path.format(
                                    item_type_plural='organizations',
                                    id=org['id'])
                            )
                            has_changes = False
                            print('deleted', d.status_code)
                            print(org[getattr(OrgFields, 'site')], org[getattr(OrgFields, 'name')], str(response.status_code))
                    except Exception:
                        if org['owner_name'] == 'Vadym Hevlich':
                            print('connection error ', org[getattr(OrgFields, 'site')])
                            d = self.session.delete(
                                self.base_put_path.format(
                                    item_type_plural='organizations',
                                    id=org['id'])
                            )
                            has_changes = False
                            print('deleted', d.status_code)
                if has_changes:
                    print(org[getattr(OrgFields, 'site')])
                    self.session.put(
                        self.base_put_path.format(
                            item_type_plural='organizations',
                            id=org['id']
                        ),
                        json=org
                    )

    def delete_old_orgs(self):
        pipedrive_notes = []
        note_path_gen = get_base_full_path(
            self.base_path,
            self.pipedrive_get_step,
            'notes'
        )
        for note_path in note_path_gen:
            pipedrive_notes.extend(requests.get(note_path).json()['data'])
        org_ids_to_not_delete = list(map(lambda n: n['org_id'], pipedrive_notes))
        deal_ids_to_not_delete = list(map(lambda n: n['deal_id'], pipedrive_notes))
        print(deal_ids_to_not_delete)
        #
        # for deal_path in self.deal_path_gen:
        #     pipedrive_deals = requests.get(deal_path)
        #     if pipedrive_deals.json()['data']:
        #         for deal in pipedrive_deals.json()['data']:
        #             if deal['creator_user_id']['name'] == 'Vadym Hevlich' and deal['id'] not in deal_ids_to_not_delete:
        #                 deal_r = self.session.delete(
        #                     self.base_put_path.format(
        #                         item_type_plural='deals',
        #                         id=deal['id'])
        #                 )
        #                 print('deal ', deal_r, deal['id'])

        for org_path in self.orgs_path_gen:
            pipedrive_orgs = requests.get(org_path)
            if pipedrive_orgs.json()['data']:
                for org in pipedrive_orgs.json()['data']:
                    if org['owner_id']['name'] == 'Vadym Hevlich' and org['id'] not in org_ids_to_not_delete:
                        org_r = self.session.delete(
                            self.base_put_path.format(
                                item_type_plural='organizations',
                                id=org['id'])
                        )
                        print('org ', org_r, org['id'])


if __name__ == '__main__':
    PipedriveIssuesFix()
