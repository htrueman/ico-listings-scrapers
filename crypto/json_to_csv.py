import tablib


imported_data = tablib.Dataset().load(open('icomarks_teams.json').read())

with open('icomarks_members.csv', 'w+') as f:
    f.write(imported_data.export('csv'))

print('Done')
