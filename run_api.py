import json

from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from crypto.api_loaders.icomarks import main as icomarks_main
from crypto.api_loaders.icobench import main as icobench_main
from utils.post_to_pipedrive import PostToPipedrive


configure_logging()
settings = get_project_settings()

OUTPUT_FILE = settings['FEED_API_URI']
open(OUTPUT_FILE, 'w').close()


def load_api(main_func, output_file=OUTPUT_FILE):
    orgs = main_func()
    with open(output_file, 'a') as f:
        f.write('[\n')
        for i, org in enumerate(orgs):
            f.write(json.dumps(dict(org)))
            f.write("\n]" if i == len(orgs) - 1 else ",\n")


def repaire_file(output_file=OUTPUT_FILE):
    with open(output_file, 'r') as f:
        content = f.read()
    with open(output_file, 'w') as f:
        f.write(content.replace('\n][\n', ',\n'))


if __name__ == '__main__':
    while True:
        load_api(icomarks_main)
        load_api(icobench_main)
        repaire_file()
        PostToPipedrive(orgs_file_name=OUTPUT_FILE)
        open(OUTPUT_FILE, 'w').close()
