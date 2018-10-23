import json
import sys

import tablib

from utils.constants import OrgFields


class MergeItems:
    def __init__(self, imported_orgs_file_name=None, *args, **kwargs):

        self.imported_organizations = tablib.Dataset(json.loads(open(imported_orgs_file_name).read()))
        self.organizations_file_name = 'non_duplicate_{}'.format(imported_orgs_file_name)

        self.ndo_content = []
        self.make_merge()

    def merge_main(self, organization, mergeable_link_keys, merged_count):
        merge = False
        for ndo_index, ndo_organization in enumerate(self.ndo_content):
            for content_key, content_value in ndo_organization.items():
                content_key = getattr(OrgFields, content_key)
                if content_key == 'site':
                    if organization[content_key] and organization[content_key] == content_value:
                        merge = True
                elif content_key in mergeable_link_keys:
                    if organization[content_key] \
                            and content_value \
                            and organization[content_key].lower() == content_value.lower():
                        merge = True

                if merge:
                    organization.update(
                        {k: v for k, v in ndo_organization.items()
                         if len(v) > len(organization[k])}
                    )
                    self.ndo_content[ndo_index] = organization
                    merged_count += 1

                    print('merged: ', merged_count)

                    break
            if merge:
                break

        if not merge:
            self.ndo_content.append(organization)

    def make_merge(self):
        imported_organizations_json = json.loads(self.imported_organizations.export('json'))[0]
        merged_count = 0

        imported_total = len(imported_organizations_json)

        mergeable_link_keys = [h for h in imported_organizations_json[0].keys()
                               if 'link' in h and 'medium' not in h]

        for index, organization in enumerate(imported_organizations_json):
            print('{} of {}'.format(index, imported_total))

            if index == 0:
                self.ndo_content.append(organization)
            else:
                self.merge_main(organization, mergeable_link_keys, merged_count)

        with open(self.organizations_file_name, 'w') as f:
            f.write(json.dumps(self.ndo_content))


if __name__ == '__main__':
    print(sys.argv[1])
    MergeItems(*sys.argv[1])
