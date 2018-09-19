import tablib


imported_data = tablib.Dataset().load(open('wiserico.json').read())

with open('f.csv', 'w+') as f:
    f.write(imported_data.export('csv'))

print(type(imported_data.export('csv')))
