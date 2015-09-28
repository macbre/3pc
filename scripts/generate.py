#!/usr/bin/env python
import json
import logging
import re

from collections import OrderedDict
from urllib2 import urlopen

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-20s %(levelname)-8s %(message)s'
)


# 3pc source generic class
class ThirdPCSource(object):
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.info('Started')

    def _fetch_url(self, url):
        self._logger.info('Fetching <{}>'.format(url))

        response = urlopen(url)
        ret = response.read()

        self._logger.info('HTTP {}'.format(response.code))
        return ret

    @property
    def version(self):
        """
        Get version entry from package.json
        """
        with open('../package.json') as fp:
            package = json.load(fp)
            return package['version']

    def _store(self, name, data):
        self._logger.info('Saving data to {}.json'.format(name))

        filename = '../db/{}.json'.format(name)
        with open(filename, 'wt') as fp:
            data.update({
                '_generator': '3pc v{}'.format(self.version)
            })

            json.dump(data, fp, indent=2, sort_keys=True, separators=(',', ': '))

    def generate(self):
        raise Exception("generate function must be implemented")


# Generate cdn.json using WebPageTest data (issue #6)
class WebPageTestSource(ThirdPCSource):
    SOURCE = 'https://raw.githubusercontent.com/WPO-Foundation/webpagetest/master/agent/wpthook/cdn.h'

    def generate(self):
        content = self._fetch_url(self.SOURCE)
        matches = re.findall(r'(\w+)\[\] = \{([^;]+)\};', content, flags=re.MULTILINE)

        cdn = {}

        for section, lines in matches:
            # parse lines
            # e.g. {"server", "cloudflare", "Cloudflare"}
            lines = re.findall(r'\{([^}]+)\}', lines.strip())

            # parse each line items
            lines = [line.strip('"').split('", "') for line in lines]

            self._logger.info('Parsing {} section with {} entries'.format(section, len(lines)))
            self._logger.debug((section, lines))

            if section == 'cdnList':
                # {".nocookie.net", "Fastly"}
                cdn['by_domain'] = OrderedDict()

                for domain, name in lines:
                    cdn['by_domain'][domain] = name

            elif section == 'cdnHeaderList':
                # {"Via", "CloudFront", "Amazon CloudFront"}
                cdn['by_header'] = OrderedDict()

                for header, value, name in lines:
                    cdn['by_header']['{}: {}'.format(header, value)] = name

        self._store('cdn', cdn)


def main():
    logger = logging.getLogger(__name__)
    logger.info('Started')

    # process all registered sources
    for source in ThirdPCSource.__subclasses__():
        source().generate()

    logger.info('Done')

if __name__ == "__main__":
    main()
