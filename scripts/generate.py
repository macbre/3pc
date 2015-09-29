#!/usr/bin/env python
import json
import logging
import re

from collections import OrderedDict
from urllib2 import urlopen

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)-20s %(levelname)-8s %(message)s'
)


# 3pc source generic class
class ThirdPCSource(object):
    SOURCE = None
    FILENAME = None

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._data = {}

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
        with open('package.json') as fp:
            package = json.load(fp)
            return package['version']

    def _store(self, name, data):
        self._logger.info('Saving data to {}'.format(name))

        filename = 'db/{}'.format(name)
        with open(filename, 'wt') as fp:
            data.update({
                '_generator': '3pc v{}'.format(self.version),
                '_source': self.SOURCE
            })

            json.dump(data, fp, indent=2, sort_keys=True, separators=(',', ': '))

    def generate(self):
        """
        Run the _generate function that is implemented on per-source basis

        Data stored in self._data will be then saved in self.FILENAME
        """
        self._generate()
        self._store(self.FILENAME, self._data)

    def _generate(self):
        raise Exception("_generate function must be implemented")


# Generate cdn.json using WebPageTest data (issue #6)
class WebPageTestSource(ThirdPCSource):
    SOURCE = 'https://raw.githubusercontent.com/WPO-Foundation/webpagetest/master/agent/wpthook/cdn.h'
    FILENAME = 'cdn.json'

    def _generate(self):
        content = self._fetch_url(self.SOURCE)
        matches = re.findall(r'(\w+)\[\] = \{([^;]+)\};', content, flags=re.MULTILINE)

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
                self._data['by_domain'] = OrderedDict()

                for domain, name in lines:
                    self._data['by_domain'][domain] = name

            elif section == 'cdnHeaderList':
                # {"Via", "CloudFront", "Amazon CloudFront"}
                self._data['by_header'] = OrderedDict()

                for header, value, name in lines:
                    self._data['by_header']['{}: {}'.format(header, value)] = name


# Generate trackers.json using Ghostery data (issue #1)
class GhosterySource(ThirdPCSource):
    SOURCE = 'https://raw.githubusercontent.com/jonpierce/ghostery/master/' + \
             'firefox/ghostery-statusbar/ghostery/chrome/content/ghostery-bugs.js'
    FILENAME = 'trackers.json'

    def _generate(self):
        content = self._fetch_url(self.SOURCE).strip(';')
        rules = json.loads(content)

        self._data['by_regexp'] = {}
        self._data['by_url'] = {}

        self._logger.info('Parsing {} rules'.format(len(rules)))

        for entry in rules:
            pattern = entry['pattern']

            if re.search(r'[\(\|\*\?]', pattern):
                # regexp rule: "/google-analytics\\.com\\/(urchin\\.js|ga\\.js)/i"
                pattern = re.sub(r'^/|/i$', '', pattern)  # remove wrapping /

                self._data['by_regexp'][pattern] = entry['name']
            else:
                # strpos rule: "/\\/piwik\\.js/i"
                pattern = re.sub(r'^/|/i$', '', pattern)
                pattern = re.sub(r'\\', '', pattern)

                self._data['by_url'][pattern] = entry['name']


def main():
    logger = logging.getLogger(__name__)
    logger.info('Started')

    # process all registered sources
    for source in ThirdPCSource.__subclasses__():
        source().generate()

    logger.info('Done')

if __name__ == "__main__":
    main()
