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
        self.delete_old_orgs()
        # self.temp()

    def temp(self):

        l = [
            2,
            4,
            5,
            6,
            7,
            8,
            10
            ,11
            ,12
            ,13
            ,14
            ,15
            ,16
            ,17
            ,18
            ,19
            ,20
            ,23
            ,24
            ,25
            ,26
            ,29
            ,30
            ,31
            ,32
            ,33
            ,34
            ,35
            ,36
            ,37
            ,38
            ,39
            ,41
            ,43
            ,45
            ,46
            ,49
            ,52
            ,53
            ,55
            ,57
            ,58
            ,59
            ,61
            ,62
            ,64
            ,65
            ,66
            ,68
            ,69
            ,70
            ,71
            ,72
            ,73
            ,74
            ,75
            ,76
            ,79
            ,82
            ,83
            ,84
            ,85
            ,87
            ,88
            ,89
            ,91
            ,93
            ,95
            ,96
            ,97
            ,98
            ,101,
            102,
            103,
            105,
            107,
            108,
            110,
            112,
            114,
            115,
            116,
            118,
            119,
            121,
            123,
            124,
            125,
            127,
            131,
            133,
            135,
            137,
            138,
            140,
            142,
            144,
            145,
            146,
            147,
            148,
            149,
            151,
            155,
            156,
            157,
            158,
            162,
            163,
            168,
            171,
            172,
            173,
            174,
            175,
            182,
            183,
            184,
            185,
            186,
            190,
            191,
            192,
            193,
            195,
            197,
            199,
            200,
            201,
            204,
            206,
            207,
            209,
            212,
            213,
            215,
            217,
            218,
            220,
            221,
            222,
            223,
            224,
            225,
            226,
            228,
            229,
            230,
            231,
            232,
            233,
            234,
            235,
            236,
            237,
            238,
            239,
            240,
            244,
            246,
            247,
            248,
            251,
            252,
            253,
            254,
            255,
            257,
            258,
            260,
            261,
            263,
            264,
            266,
            267,
            269,
            270,
            272,
            274,
            276,
            277,
            278,
            279,
            280,
            281,
            282,
            283,
            284,
            285,
            286,
            287,
            288,
            289,
            290,
            292,
            293,
            294,
            295,
            296,
            299,
            300,
            301,
            303,
            306,
            307,
            308,
            310,
            312,
            313,
            314,
            317,
            318,
            319,
            321,
            322,
            324,
            326,
            328,
            329,
            330,
            331,
            334,
            336,
            337,
            338,
            340,
            342,
            343,
            345,
            346,
            347,
            350,
            351,
            352,
            353,
            354,
            355,
            356,
            358,
            359,
            360,
            361,
            364,
            365,
            366,
            368,
            369,
            370,
            371,
            373,
            374,
            376,
            377,
            378,
            379,
            381,
            382,
            383,
            384,
            385,
            387,
            388,
            389,
            390,
            391,
            392,
            393,
            394,
            395,
            396,
            397,
            398,
            401,
            402,
            403,
            404,
            407,
            409,
            410,
            413,
            414,
            416,
            417,
            420,
            421,
            423,
            427,
            429,
            430,
            432,
            433,
            434,
            435,
            437,
            441,
            442,
            443,
            444,
            445,
            446,
            447,
            448,
            449
        ]

        for i in l:
            r = self.session.get(
                self.base_put_path.format(
                    item_type_plural='deals',
                    id=i
                ),
            )

            deal = r.json()['data']
            deal['deleted'] = False
            deal['status'] = 'open'
            deal['creator_user_id'] = deal['creator_user_id']['id']
            deal['user_id'] = deal['user_id']['id']
            deal['org_id'] = deal['org_id']['value']

            print(deal)
            r = self.session.put(
                self.base_put_path.format(
                    item_type_plural='deals',
                    id=i
                ),
                json=deal
            )
            print(r.json())

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
