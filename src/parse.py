from bs4 import BeautifulSoup
import re
import logging
from requester import Requester


class Parse:
    def __init__(self, requester: Requester, logger: logging.Logger):
        self.logger = logger
        self.requester = requester

    # Get the total number of entries on a particular archive url page:
    # Example: https://arxiv.org/list/cs/1805 -> returns int(4158)
    # The archives do not show duplicates (i.e. anything past v1),
    # so we can be sure if counts don't match up there's a problem in their data (deleted papers).
    def get_total_entries(self, url: str) -> int:
        r = self.requester.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        rgx = re.compile("Total of ([0-9]+) entries")
        total_entries = soup.find(string=rgx)

        try:
            total_entries = rgx.search(str(total_entries)).group(1)
            total_entries = int(total_entries)
        except ValueError:
            self.logger.error(
                "Could not parse total entries. Has the websites HTML changed? url: %s, status: %s",
                url,
                r.status_code,
            )
            exit(1)

        self.logger.debug(
            "Total entries retrieved (%d) for url: %s", total_entries, url
        )
        return total_entries
