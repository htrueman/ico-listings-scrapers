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


def find_related_members(imported_members_json, name1, name2=None, final_name=None):
    members = []
    for member in imported_members_json:
        if member['Organization'] in [name1, name2]:
            member['Organization'] = final_name or name1
            members.append(member)

    unique_members = []
    while len(members):
        name_key = 'Linkedin link'
        link_key = 'Name'
        current = members.pop()
        rest_links = [m[link_key] for m in members]
        rest_names = [m[name_key] for m in members]
        if current[name_key] and current[name_key] in rest_names or current[link_key] and current[link_key] in rest_links:
            pass
        else:
            unique_members.append(current)

    # if len(members) > 15:
    #     print(len(members))
    #     print('\n'.join(sorted([m['Name'] for m in members])))
    return unique_members


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
                        organization_name = organization['Name']
                        ndo_organisation_name = ndo_organization['Name']
                        organization.update(
                            {k: v for k, v in ndo_organization.items() if len(v) > len(organization[k])}
                        )
                        ndo_content[ndo_index] = organization
                        merged_count += 1

                        final_name = organization['Name']
                        members = find_related_members(imported_members_json, organization_name, ndo_organisation_name, final_name)
                        clear_imported_members_json += members
                        print('merged: ', merged_count)

                        break
                if merge:
                    break

            if not merge:
                ndo_content.append(organization)
                members = find_related_members(imported_members_json, organization['Name'])
                clear_imported_members_json += members

        with open(organizations_file_name, 'w') as f:
            f.write(json.dumps(ndo_content))

        with open(members_file_name, 'w') as f:
            f.write(json.dumps(clear_imported_members_json))


if __name__ == '__main__':
    make_merge()
