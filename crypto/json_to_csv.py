import tablib


imported_data = tablib.Dataset().load(open('non_duplicate_members.json').read())

with open('non_duplicate_members.csv', 'w+') as f:
    f.write(imported_data.export('csv'))

print('Done')
