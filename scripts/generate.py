#!/usr/bin/env python
import logging

from sources import ThirdPCSource

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)-25s %(levelname)-8s %(message)s'
)


def main():
    logger = logging.getLogger(__name__)
    logger.info('Started')

    # process all registered sources
    for source in ThirdPCSource.__subclasses__():
        source().generate()

    logger.info('Done')

if __name__ == "__main__":
    main()
