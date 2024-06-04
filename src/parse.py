from requests import Session
from bs4 import BeautifulSoup
import re
import logging


class Parse:
    def __init__(self, session: Session, logger: logging.Logger):
        self.session = session
        self.logger = logger

    # Get the total number of entries on a particular archive url page:
    # Example: https://arxiv.org/list/cs/1805 -> returns int(4158)
    # The archives do not show duplicates (i.e. anything past v1),
    # so we can be sure if counts don't match up there's a problem in their data (deleted papers).
    def get_total_entries(self, url: str) -> int:
        r = self.session.get(url)
        if r.status_code != 200:
            self.logger.error(
                "Could not get total entries", url, r.status_code
            )
            exit(1)

        soup = BeautifulSoup(r.text, "html.parser")
        rgx = re.compile("Total of ([0-9]+) entries")
        total_entries = soup.find(string=rgx)

        try:
            total_entries = rgx.search(str(total_entries)).group(1)
            total_entries = int(total_entries)
        except ValueError:
            self.logger.error(
                "Could not parse total entries. Has the websites HTML changed?",
                url,
                r.status_code,
            )
            exit(1)

        return total_entries
