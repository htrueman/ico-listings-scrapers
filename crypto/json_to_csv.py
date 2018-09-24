import tablib


imported_data = tablib.Dataset().load(open('non_duplicate_organizations.json').read())

with open('non_duplicate_organizations.csv', 'w+') as f:
    f.write(imported_data.export('csv'))

print('Done')
