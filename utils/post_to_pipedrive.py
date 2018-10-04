import json
import tablib
import requests


class PostToPipedrive:
    base_path = 'https://relevant-dessert.pipedrive.com/v1/{item_type_plural}' \
                '?api_token=3b08b823cf50cc5e47baec700b369ba47f202bf0'
    
    def __init__(self,
                 orgs_file_name=None,
                 deals_file_name=None,
                 members_file_name=None):

        # orgs = tablib.Dataset().load(open(orgs_file_name).read())
        # self.orgs_json = json.loads(orgs.export('json'))
        #
        # deals = tablib.Dataset().load(open(deals_file_name).read())
        # self.deals_json = json.loads(deals.export('json'))
        #
        # members = tablib.Dataset().load(open(members_file_name).read())
        # self.deals_json = json.loads(members.export('json'))

        self.main()

    def main(self):
        print('here')
        existing_orgs = requests.get(self.base_path.format(item_type_plural='organizations'))
        for d in existing_orgs.json()['data']:
            print(d)
            break

        org_dict = {
            'name': 'Datablockchain',
            'open_deals_count': 1,
            'related_open_deals_count': 0,
            'closed_deals_count': 0,
            'related_closed_deals_count': 0,
            'email_messages_count': 0,
            'people_count': 17,
            'activities_count': 0,
            'done_activities_count': 0,
            'undone_activities_count': 0,
            'reference_activities_count': 0,
            'files_count': 0,
            'notes_count': 2,
            'followers_count': 1,
            'won_deals_count': 0,
            'related_won_deals_count': 0,
            'lost_deals_count': 0,
            'related_lost_deals_count': 0,
            'active_flag': True,
            'category_id': None,
            'picture_id': None,
            'country_code': None,
            'first_char': 'd',
            'update_time': '2018-09-27 21:15:06',
            'add_time': '2018-05-15 07:58:34',
            'visible_to': '3',
            'next_activity_date': None,
            'next_activity_time': None,
            'next_activity_id': None,
            'last_activity_id': None,
            'last_activity_date': None,
            'label': None,
            'address': None,
            'address_subpremise': None,
            'address_street_number': None,
            'address_route': None,
            'address_sublocality': None,
            'address_locality': None,
            'address_admin_area_level_1': None,
            'address_admin_area_level_2': None,
            'address_country': None,
            'address_postal_code': None,
            'address_formatted_address': None,
            '3a7ab4c4f128f0b4b3224cb9dbf1ac892fb04ff5': 'https://icobench.com/ico/datablockchain',
            '0597db537f5942f12c5972b8b3c7eccc1257f021': 'Cayman Islands',
            '181de81c6261329bdceed27ed2efe448db432846': '2018-05-27',
            '181de81c6261329bdceed27ed2efe448db432846_until': '2018-06-27',
            '41427adbb8512d496082c36587c0c1eec4b71a69': '2018-09-10',
            '41427adbb8512d496082c36587c0c1eec4b71a69_until': '2018-10-31',
            'b34181f68cae0ef102bd759f7f6f521574421009': '2018-05-27',
            'b34181f68cae0ef102bd759f7f6f521574421009_until': '2018-10-31',
            'd76d4c336cfbab7370427abba02d4a34f10adaac': 4.7,
            'bd01c4bf0f2f1d6656d6ea6249a8f744a9332a14': 4.8,
            'bad5c31cbbcdc27b5cb26303107d98a726f0400c': 4.7,
            'ca80f495655efecb18bb631888702778b424dd8a': 4.6,
            '28a057442cb6c909834fee143db4f41cd572d88f': 4.8,
            'badfa76adf047269cf99ffa1df094c7516a32268': 'DataBlockChain.io is a revolutionary data platform that stands to disrupt the way that companies and individuals gather premium data. Our product will democratize data, making it more readily available and less expensive than the current methods of data gathering and vetting. The result is that clients can access specific data sets in a cost-effective and transparent way, collecting exactly what they need without paying for extraneous data. MVP is LIVE! \r\n\r\nWe will merge our own proprietary data with many of the world’s largest databases ranging from government data, industry-specific data, voting records, business to business data, property data, credit bureau data, etc. to create a comprehensive variety of data sets valuable to individuals and businesses looking to both attract and retain clients.\r\n\r\nAs a result of our platform, all participants will be able to obtain the exact, nuanced data they are seeking. Because DataBlockChain.io removes the middlemen in the data industry.',
            '43196c4b7b933bd1dbf4c8cacd19c524732cec85': '',
            '537f17eda9623f072d35c72d43a9cf2af8aa6929': '1 DBCCoin = 0.12 USD',
            '0b95724a1b593fc7f81c54b5dfe6892b06a4f057': 0,
            'c6604ebd9b26c3570017a8d51155f8f9c14270aa': 591600000,
            '7a3202db617a359559ddf0b446dd760aaeac80b5': 50000000,
            'cf76b6d8b2c3649bb625621282aa823427ba2d56': 10000000,
            '9c058bb74a6aaf958f74197803ad3cf3c943959c': 0,
            '9c058bb74a6aaf958f74197803ad3cf3c943959c_currency': 'IDR',
            '161b1434f0b0a1470df39b1f4a366b9be0f94221': None,
            '161b1434f0b0a1470df39b1f4a366b9be0f94221_currency': None,
            '05d96d97afafd744f2058189cd8322f2b411631c': None,
            '3eae70451093702d73bc673392140d1dd148990d': None,
            '37bb04143de69ea2b30559aae8972a5b0fad5c3b': None,
            '855163173f2039b38ad71a560628b2492520bc30': None,
            'd57dc05b4b0d4f0c2ba73ee1211750282318d2fc': None,
            'b4871a3edf8ae6f4215f0f38a3cf330010755c3f': None,
            '5ac527b83d6ceeeec798a9cda9cee3030aa11712': None,
            '0017179018085f6d627d6fe4443347635b3c278b': None,
            'fb488cfcadf7c0f0fbfcaafbc8ff4db590296a27': None,
            '932cb10494275ba4ff495df0a75ebcca1dc0ec8f': None,
            '850f3be6cc1b2b79961a716609488939f9b03496': None,
            '3db40cff6214eb767ab8b3f866de0bdb59a5644a': None,
            'ca38eeb0c869b640ae2aa4679a63ea407c3874d3': None,
            '304903240d588419beeb7f88b1599056c5cc29be': None,
            '52714484f8a7222562c26213d66871eac010d103': None,
            '9b0d043091ecd2819de131bc77c44a70c3b6091e': None,
            '2a333a658c44c0c1662bf602587c8348d40c21c5': None,
            '7624affb4afec7c8566c446009d699ca3858349f': None,
            'ef3fb9aabf598fd926241757d2a85cc552ba019d': None
        }

        # response = requests.post(self.base_path.format(item_type_plural='organizations'), json={
        #     'name': 'AAAAAA'
        # })
        # print(response)


if __name__ == '__main__':
    PostToPipedrive()
