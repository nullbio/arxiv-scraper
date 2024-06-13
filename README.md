# scrapii

WORK IN PROGRESS, CURRENTLY NON-FUNCTIONAL. WILL REMOVE THIS HEADER WHEN PROJECT IS IN WORKING STATE. STAY TUNED, ACTIVE DEV UNDERWAY.

Scrapii is a research documents scraper web app, written in Django, that allows you to scrape research papers, documents, and web pages from various sources and store them on disk, and in a SQLite database.

If there is an additional resource you want to scrape that is not currently supported, it is easy to create a new plugin for scrapii. Scrapii ships with an arXiv plugin, and we're looking for community members to contribute additional plugins.

## About

Depending on which plugins you have activated through the Scrapii web app, we scrape that resource and store their relevant research documents and document metadata in a SQLite database and on disk. For example, you can use Scrapii to download all research papers on arXiv, selecting which categories you would like to keep. Scrapii will then store all of the abstracts, titles, and other relevant metadata about the research papers for those categories in the database, and save the relevant paper PDFs to disk. Scrapii will continue to monitor arXiv for any new papers and download them as they become available.

The arXiv plugin also has the ability to scan the local database to highlight discrepencies in the arXiv website. In other words, it can detect whether papers are removed from the arXiv archives, and notify you of the relevant paper. This is useful to ensure arXiv's data archives remain up to date and accurate, and data integrity is maintained. I'm not aware of any other service or software that explicitly allows you to monitor for discrepancies such as this, and given this article: [Millions of research papers at risk of disappearing from the Internet](https://www.nature.com/articles/d41586-024-00616-5) - I feel it is prudent functionality.

## Plugins

Plugins are shipped as Django apps, and once installed, can be dynamically enabled and disabled through the Scrapii web app. Scrapii ships with an arXiv plugin, and we're looking for community members to contribute additional plugins.

## Installation

TODO: Finish installation instructions.
