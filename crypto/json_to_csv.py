import tablib


imported_data = tablib.Dataset().load(open('icoholder.json').read())

with open('icoholder.csv', 'w+') as f:
    f.write(imported_data.export('csv'))

print(type(imported_data.export('csv')))
