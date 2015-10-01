import json
import re

from . import ThirdPCSource


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
                self._count += 1
            else:
                # strpos rule: "/\\/piwik\\.js/i"
                pattern = re.sub(r'^/|/i$', '', pattern)
                pattern = re.sub(r'\\', '', pattern)

                self._data['by_url'][pattern] = entry['name']
                self._count += 1
