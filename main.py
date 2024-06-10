import os
import sys

# from config import scrape, sql
# from models.models import Category


# from scrape import Category


def main():
    print(os.environ.get("PYTHONPATH"))


# categories = Category.objects.all()
# for category in categories:
#     print(category.name)
# Get the categories we want to scrape and their
# oldest years they have papers for.
# categories = map(
#     lambda x: Category(x["category"], x["end_year"]), sql.get_categories()
# )

# Create the skip list. We don't want to try and download this
# metadata because it's already been finished.


# skip_list = sql.get_finished_archive_urls()

# Start scraping, one unfinished category at a time,
# by looping through their month urls.
# i = 0
# for c in categories:
#     i += len(c.month_urls)
#     for mu in c.month_urls:
#         # if mu is in skip_list, skip it
#         if mu in skip_list:
#             continue

#         print(f"Scraping {mu}")
#         total_entries = scrape.total_entries(mu)
#         # scrape.paper_metadata(mu, )

#         # call scrape archive page in loop, relative to total entries offset
#         # scrape archive page will return a ArchivePage and

# print(i)
# # Find the pages we haven't scraped yet.

# # Close sqlite database at end of program
# sql.close()


if __name__ == "__main__":
    main()
