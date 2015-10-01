import re
from collections import OrderedDict

from . import ThirdPCSource


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
                    # filter out "END_MARKER"
                    if '.' in domain:
                        self._data['by_domain'][domain] = name
                        self._count += 1

            elif section == 'cdnHeaderList':
                # {"Via", "CloudFront", "Amazon CloudFront"}
                self._data['by_header'] = OrderedDict()

                for header, value, name in lines:
                    self._data['by_header']['{}: {}'.format(header, value)] = name
                    self._count += 1
