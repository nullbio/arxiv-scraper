from pprint import pprint
from datetime import datetime
import os
from typing import Tuple
from config import *


class Category:
    def __init__(self, name: str, end_year: int):
        self.name = name
        self.end_year = end_year
        self.month_urls = self.get_month_urls()

    def get_month_urls(self):
        month_urls = []
        curr_yr = datetime.now().year
        # start at -1 from current month, because archives dont happen til end of month
        curr_mnth = datetime.now().month - 1
        yr = curr_yr
        while yr >= self.end_year:
            for mnth in range(12, 0, -1):
                if yr == curr_yr and mnth > curr_mnth:
                    continue

                # get last two digits of year
                setyr = int(str(yr)[-2:])
                month_urls.append(
                    f"https://arxiv.org/list/{self.name}/{setyr:02d}{mnth:02d}"
                )
            yr -= 1
        return month_urls


class Scraper:
    def __init__(self, **kwargs):
        # Create the download directory if it doesn't exist
        os.makedirs(DOWNLOAD_DIRECTORY, exist_ok=True)


class ArchivePage:
    def __init__(self, **kwargs):
        self.category = kwargs.get("category")
        self.archive_url = kwargs.get("url")
        self.total_entries = kwargs.get("total_entries")
        self.mm = kwargs.get("month")
        self.year = kwargs.get("year")
        self.collected_entries = 0
        self.last_updated_date = datetime.now()


class ArchivePapers:
    def __init__(self, **kwargs):
        return


# By appending ?skip=0&show=2000 we can get 2000 results per page at a time, where skip is the offset (exclusive)
# If we see <dl id="articles"><p>No updates for this time period.</p></dl> we know we've reached the end of the archive.
def scrape_archive_page(skip: int) -> Tuple[ArchivePage, ArchivePapers]:
    return ArchivePage(), ArchivePapers()


# Get the categories we want to scrape and their oldest years they have papers for.
categories = map(
    lambda x: Category(x["category"], x["end_year"]), sql.get_categories()
)

# Create the skip list. We don't want to try and download this
# metadata because it's already been finished.
skip_list = sql.get_finished_archive_urls()

# Start scraping, one category at a time, by looping through their month urls.
i = 0
for c in categories:
    i += len(c.month_urls)
    for mu in c.month_urls:
        # if mu is in skip_list, skip it
        if mu in skip_list:
            continue

        print(f"Scraping {mu}")
        total_entries = parser.get_total_entries(mu)

        # call scrape archive page in loop, relative to total entries offset
        # scrape archive page will return a ArchivePage and


print(i)
# Find the pages we haven't scraped yet.

# Close sqlite database at end of program
sql.close()
