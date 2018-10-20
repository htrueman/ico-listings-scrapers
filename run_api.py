from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from run import load_api, repaire_file
from crypto.api_loaders.icomarks import main as icomarks_main
from crypto.api_loaders.icobench import main as icobench_main
from utils.post_to_pipedrive import PostToPipedrive


configure_logging()
settings = get_project_settings()

OUTPUT_FILE = settings['FEED_API_URI']
open(OUTPUT_FILE, 'w').close()

if __name__ == '__main__':
    load_api(icomarks_main)
    load_api(icobench_main)

    repaire_file()
    PostToPipedrive(orgs_file_name=OUTPUT_FILE)
