import json
import sys
import datetime
from collections import OrderedDict

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

        self.main()

    def main(self):
        for org in self.orgs_json:
            dates_dict = OrderedDict()
            dates_dict.update({'Main sale end (date)': org['Main sale end (date)']})
            # for key, value in org.items():
            #     date_marks = ['sale', 'date', 'ico']
            #     not_wanted_date_marks = ['update', 'activity', 'for']
            #     if any(x in key.lower() for x in date_marks) \
            #             and not any(x in key.lower() for x in not_wanted_date_marks):
            #         dates_dict.update({key: value})
            # ordered_dates_dict = OrderedDict(
            #     sorted(dates_dict.items(), key=lambda x: print(x))
            # )

            # print(ordered_dates_dict)

            break


if __name__ == '__main__':
    print(sys.argv[1])
    SpitDeals(sys.argv[1])
