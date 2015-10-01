import json
import logging

from urllib2 import urlopen


# 3pc source generic class
class ThirdPCSource(object):
    SOURCE = None
    FILENAME = None

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)

        self._data = {}
        self._count = 0

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
                '_count': self._count,
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
