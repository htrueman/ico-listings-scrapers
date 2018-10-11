import json

from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from crypto.api_loaders.icomarks import main as icomarks_main
from utils.post_to_pipedrive import PostToPipedrive


configure_logging()
settings = get_project_settings()

OUTPUT_FILE = settings['FEED_URI']
open(OUTPUT_FILE, 'w').close()

runner = CrawlerRunner(settings)


@defer.inlineCallbacks
def crawl():
    yield runner.crawl('trackico')
    yield runner.crawl('icobazaar')
    yield runner.crawl('icoholder')
    yield runner.crawl('baseinfo')
    yield runner.crawl('foundico')
    yield runner.crawl('coinschedule')
    reactor.stop()


def load_icomarks(output_file=OUTPUT_FILE):
    icomarks_orgs = icomarks_main()
    with open(output_file, 'a') as f:
        f.write('[\n')
        for i, icomarks_org in enumerate(icomarks_orgs):
            f.write(json.dumps(dict(icomarks_org)))
            f.write("\n]" if i == len(icomarks_orgs) - 1 else ",\n")


def repaire_file(output_file=OUTPUT_FILE):
    with open(output_file, 'r') as f:
        content = f.read()
    with open(output_file, 'w') as f:
        f.write(content.replace('\n][\n', ',\n'))


if __name__ == '__main__':
    crawl()
    reactor.run()

    load_icomarks()

    repaire_file()

    print('crawled')

    # PostToPipedrive(orgs_file_name=OUTPUT_FILE)
