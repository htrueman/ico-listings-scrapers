import json
import sys
import datetime

import dateparser
import tablib


class SpitDeals:
    """
    Get file with non duplicate clean organizations and
    split them between pipelines by ICO status.
    """
    def __init__(self, orgs_file_name):
        self.orgs_file_name = orgs_file_name

        orgs = tablib.Dataset().load(open(self.orgs_file_name).read())
        self.orgs_json = json.loads(orgs.export('json'))

        self.deals_file_name = 'sorted_deals.json'
        with open(self.deals_file_name, 'w+') as f:
            f.write('')

        self.deals_file = open(self.deals_file_name, 'a+')

        self.main()

    def main(self):
        self.deals_file.write('[\n')

        for index, org in enumerate(self.orgs_json):
            if org['Main sale end (date)']:
                end_date = dateparser.parse(org['Main sale end (date)'])
            elif org['Token sale range (str)'] and '-' in org['Token sale range (str)']:
                end_date = dateparser.parse(org['Token sale range (str)'].split('-')[1])
            elif org['Pre-sale end (date)']:
                end_date = dateparser.parse(org['Main sale end (date)'])
            elif org['Pre-sale range (str)'] and '-' in org['Pre-sale range (str)']:
                end_date = dateparser.parse(org['Pre-sale range (str)'].split('-')[1])
            else:
                end_date = None

            deal_dict = {
                'Deal - Title': org['Name'] + ' - deal',
                'Organization - Name': org['Name'],
                'Organization - Address': org['Address'],
            }
            if end_date:
                deal_dict['pipeline'] = '3-ico-finished'
                if end_date >= datetime.datetime.now():
                    # Active ICO
                    deal_dict['pipeline'] = '2-ico-in-progress'
            separator = ',' if index + 1 != len(self.orgs_json) else ''
            self.deals_file.write(json.dumps(deal_dict) + separator + '\n')
        self.deals_file.write(']')


if __name__ == '__main__':
    print(sys.argv[1])
    SpitDeals(sys.argv[1])
