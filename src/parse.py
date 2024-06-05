from bs4 import BeautifulSoup
import re
import logging


class Parse:
    def __init__(self, log: logging.Logger):
        self.log = log

    def total_entries(self, html: str, url: str) -> int:
        soup = BeautifulSoup(html, "html.parser")
        rgx = re.compile("Total of ([0-9]+) entries")
        total_entries = soup.find(string=rgx)

        try:
            total_entries = rgx.search(str(total_entries)).group(1)
            total_entries = int(total_entries)
        except ValueError:
            self.log.error(
                "Could not parse total entries. Has the websites "
                "HTML changed? url: %s, status: %s",
                url,
            )
            exit(1)

        self.log.debug(
            "Total entries retrieved (%d) for url: %s", total_entries, url
        )
        return total_entries
