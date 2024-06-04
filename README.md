WORK IN PROGRESS, CURRENTLY NON-FUNCTIONAL. WILL REMOVE THIS HEADER WHEN PROJECT IS IN WORKING STATE.

# arxiv-scraper

The goal of this project is to create a replica of arXiv's database of papers and paper metadata.

## About

This project is a work in progress.

We scrape the arXiv's website and store the paper metadata in a SQLite database, and the PDFs of the papers on disk.

This script can also be run as a cron job on any time interval (daily or above) to keep the database up to date, and to download new papers as they are published.

In addition to this, one of the goals of this project is to create a system that can monitor for discrepencies in the public arXiv database. This was inspired by this nature article: [Millions of research papers at risk of disappearing from the Internet](https://www.nature.com/articles/d41586-024-00616-5). This project was created to ensure no papers ever disappear from the arXiv database without a record of the event, and public attention. As such, the scraper has been programmed to detect anomalies in the arXiv website and notify the user of any discrepancies. For example, in the unlikely event a paper later unexplainably disappears from the arXiv website, an event will be logged and that paper will be flagged in the SQLite database, for further investigation.

## Installation

To install this project, you will need to have Python 3 installed on your system, and the pdm package manager installed.

TODO: Finish readme.
