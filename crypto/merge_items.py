import json

import os
import tablib

parts_count = 100


def init():
    imported_organizations = tablib.Dataset().load(open('organizations.csv').read())
    imported_members = tablib.Dataset().load(open('people.csv').read())
    organizations_file_name = 'non_duplicate_organizations.json'
    members_file_name = 'non_duplicate_members.json'

    return imported_members, imported_organizations, organizations_file_name, members_file_name


def find_related_member(imported_members_json, name1, name2=None):
    member = {}
    for member in imported_members_json:
        if member['Organization'] in [name1, name2]:
            member['Organization'] = name1
    return member


def make_merge():
    imported_members, imported_organizations, organizations_file_name, members_file_name = init()
    imported_members_json = json.loads(imported_members.export('json'))
    imported_organizations_json = json.loads(imported_organizations.export('json'))
    merged_count = 0

    ndo_content = []
    clear_imported_members_json = []
    imported_total = len(imported_organizations_json)

    mergable_link_keys = [h for h in imported_organizations.headers if 'link' in h and 'Medium' not in 'h']

    for index, organization in enumerate(imported_organizations_json):
        print('{} of {}'.format(index, imported_total))

        if index == 0:
            member = find_related_member(imported_members_json, organization['Name'])
            imported_members_json.remove(member)
            clear_imported_members_json.append(member)

            ndo_content.append(organization)
        else:
            merge = False
            for ndo_index, ndo_organization in enumerate(ndo_content):
                for content_key, content_value in ndo_organization.items():
                    if content_key == 'Address':
                        if organization[content_key] and organization[content_key] == content_value:
                            merge = True
                    elif content_key in mergable_link_keys:
                        if organization[content_key] and content_value and organization[content_key].lower() == content_value.lower():
                            merge = True

                    if merge:
                        organization.update(
                            {k: v for k, v in ndo_organization.items() if len(v) > len(organization[k])}
                        )
                        ndo_content[ndo_index] = organization
                        merged_count += 1
                        print('merged: ', merged_count)
                        break
                if merge:
                    break

            if not merge:
                ndo_content.append(organization)

        with open(organizations_file_name, 'w+') as f:
            f.write(json.dumps(ndo_content))


if __name__ == '__main__':
    make_merge()
