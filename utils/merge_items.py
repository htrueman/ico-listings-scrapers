import json
import os
import sys

import tablib


class MergeItems:
    def __init__(self, imported_orgs_file_name=None, imported_members_file_name=None, *args, **kwargs):
        if not imported_orgs_file_name or not imported_members_file_name:
            imported_orgs_file_name, imported_members_file_name = \
                os.listdir('files_to_import')[0], os.listdir('files_to_import')[1]

        self.imported_organizations = tablib.Dataset(json.loads(open(imported_orgs_file_name).read()))
        self.imported_members = tablib.Dataset(json.loads(open(imported_members_file_name).read()))

        self.organizations_file_name = 'non_duplicate_{}.json'.format(imported_orgs_file_name)
        self.members_file_name = 'non_duplicate_{}.json'.format(imported_members_file_name)

        with open(self.members_file_name, 'w+') as f:
            f.write('')

        self.members_file = open(self.members_file_name, 'r+')
        self.members_file.write('[')

        self.ndo_content = []
        self.make_merge()

    @staticmethod
    def find_related_members(imported_members_json, name1, name2=None, final_name=None):
        members = []
        for member in imported_members_json:
            if member['Organization'] in [name1, name2]:
                member['Organization'] = final_name or name1
                members.append(member)
                imported_members_json.remove(member)

        unique_members = []
        while len(members):
            name_key = 'linkedin_link'
            link_key = 'name'
            current = members.pop()
            rest_links = [m[link_key] for m in members]
            rest_names = [m[name_key] for m in members]
            if current[name_key] \
                    and current[name_key] in rest_names \
                    or current[link_key] \
                    and current[link_key] in rest_links:
                pass
            else:
                unique_members.append(current)

        return unique_members, imported_members_json

    @staticmethod
    def write_members(members, members_file):
        if members:
            members_file.write(json.dumps(members)[1:-1] + ',')

    def merge_main(self, organization, mergeable_link_keys,
                   merged_count, imported_members_json):
        merge = False
        for ndo_index, ndo_organization in enumerate(self.ndo_content):
            for content_key, content_value in ndo_organization.items():
                if content_key == 'site':
                    if organization[content_key] and organization[content_key] == content_value:
                        merge = True
                elif content_key in mergeable_link_keys:
                    if organization[content_key] \
                            and content_value \
                            and organization[content_key].lower() == content_value.lower():
                        merge = True

                if merge:
                    organization_name = organization['name']
                    ndo_organisation_name = ndo_organization['name']
                    organization.update(
                        {k: v for k, v in ndo_organization.items()
                         if len(v) > len(organization[k])}
                    )
                    self.ndo_content[ndo_index] = organization
                    merged_count += 1

                    final_name = organization['name']
                    members, imported_members_json = self.find_related_members(
                        imported_members_json,
                        organization_name,
                        ndo_organisation_name,
                        final_name)
                    self.write_members(members, self.members_file)
                    print('merged: ', merged_count)

                    break
            if merge:
                break

        if not merge:
            self.ndo_content.append(organization)
            members, imported_members_json = self.find_related_members(
                imported_members_json, organization['name'])
            self.write_members(members, self.members_file)

    def make_merge(self):
        imported_members_json = json.loads(self.imported_members.export('json'))
        imported_organizations_json = json.loads(self.imported_organizations.export('json'))
        merged_count = 0

        imported_total = len(imported_organizations_json)

        mergeable_link_keys = [h for h in self.imported_organizations.headers
                               if 'link' in h and 'medium' not in h]

        for index, organization in enumerate(imported_organizations_json):
            print('{} of {}'.format(index, imported_total))

            if index == 0:
                self.ndo_content.append(organization)
            else:
                self.merge_main(organization, mergeable_link_keys,
                                merged_count, imported_members_json)

        with open(self.organizations_file_name, 'w') as f:
            f.write(json.dumps(self.ndo_content))

        self.members_file.write(']')
        self.members_file.close()


if __name__ == '__main__':
    print(sys.argv[1:3])
    MergeItems(*sys.argv[1:3])
