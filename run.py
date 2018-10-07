from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging


configure_logging()
settings = get_project_settings()
runner = CrawlerRunner(settings)


@defer.inlineCallbacks
def crawl():
    yield runner.crawl('trackico')
    yield runner.crawl('icobazaar')
    yield runner.crawl('icoholder')
    reactor.stop()


crawl()
reactor.run()

with open(settings['FEED_URI'], 'r') as f:
    content = f.read()
with open(settings['FEED_URI'], 'w') as f:
    f.write(content.replace('\n][\n', ',\n'))
