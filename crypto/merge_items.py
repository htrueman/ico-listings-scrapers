import json
import tablib

imported_organizations = tablib.Dataset().load(open('organizations.csv').read())
imported_members = tablib.Dataset().load(open('people.csv').read())

organizations_file_name = 'non_duplicate_organizations.json'
members_file_name = 'non_duplicate_members.json'

parts_count = 100
json_orgs = json.loads(imported_organizations.export('json'))

for i in range(parts_count):
    range_start = i * len(json_orgs) // parts_count
    range_end = ((i + 1) * len(json_orgs)) // parts_count
    with open('imported_organizations_splitted_{}.json'.format(i), 'w+') as f:
        f.write(json.dumps(json_orgs[range_start:range_end]))


with open(members_file_name, 'w+') as ndm_file:
    ndo_content = []

    for i in range(parts_count):
        part_file_name = 'imported_organizations_splitted_{}.json'.format(i)
        with open(part_file_name, 'r') as f1:
            content = f1.read()
            imported_organizations = json.loads(content)
            imported_members_json = json.loads(imported_members.export('json'))
            for index, organization in enumerate(imported_organizations):

                if index == 0:
                    ndo_content.append(organization)
                else:
                    print(ndo_content)
                    to_write = True
                    for ndo_organization in ndo_content:
                        for content_key, content_value in ndo_organization.items():
                            if 'link' in content_key.lower():
                                if organization[content_key] and \
                                        organization[content_key].lower() in content_value.lower():

                                    for member in imported_members_json:
                                        if member['Organization'] in [organization['Name'], ndo_organization['Name']]:
                                            member['Organization'] = organization['Name']
                                    to_write = False
                            if not to_write:
                                organization.update({k: v for k, v in ndo_organization.items()
                                                     if len(v) > len(organization[k])})
                                ndo_content.append(organization)
                    if to_write:
                        ndo_content.append(organization)
    ndm_file.write(imported_members)
    with open(organizations_file_name, 'w+') as f:
        f.write(json.dumps(ndo_content))
