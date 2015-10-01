import re

from . import ThirdPCSource


# Generate ads.json using someonewhocares.org data (issue #11)
class SomeoneWhoCaresSource(ThirdPCSource):
    SOURCE = 'http://someonewhocares.org/hosts/hosts'
    FILENAME = 'ads.json'

    SECTION_NAME = 'ad-sites'  # ads
    # SECTION_NAME = 'spyware-sites'  # Spyware and user tracking -> trackers.json

    @staticmethod
    def extract_hosts_section(content, section):
        """
        #<section>
        127.0.0.1 domain.to.extract.com
        #</section>
        """
        start_marker = '#<{}>'.format(section)
        end_marker = '#</{}>'.format(section)
        in_section = False

        hosts = []

        for line in content.split('\n'):
            line = line.lstrip()

            if line == start_marker:
                in_section = True
            elif line == end_marker:
                in_section = False

            if in_section:
                if not line.startswith('#'):
                    # 127.0.0.1 cdn.krxd.net
                    # 127.0.0.1 media.fastclick.net	# Likewise, this may interfere with some
                    matches = re.search(r'^127.0.0.1 ([^ \t]+)', line)

                    if matches:
                        hosts.append(matches.group(1))

        return hosts

    def _generate(self):
        content = self._fetch_url(self.SOURCE)
        hosts = self.extract_hosts_section(content, self.SECTION_NAME)

        self._logger.info('Got {} hosts'.format(len(hosts)))

        self._data['hosts'] = []

        for host in hosts:
            self._data['hosts'].append(host)
            self._count += 1
