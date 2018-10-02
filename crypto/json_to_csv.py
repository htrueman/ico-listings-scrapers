import sys

import tablib


class JsonToCsv:
    def __init__(self, *args):
        self.file_names = args

        self.main()

    def main(self):
        for file in self.file_names:
            imported_data = tablib.Dataset().load(open(file).read())

            with open('{}.csv'.format(file.split('.')[0]), 'w+') as f:
                f.write(imported_data.export('csv'))

        print('Done')


if __name__ == '__main__':
    JsonToCsv(*sys.argv[1:])
