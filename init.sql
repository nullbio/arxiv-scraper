CREATE TABLE IF NOT EXISTS categories (
    category TEXT NOT NULL,
    end_year INTEGER NOT NULL,
    UNIQUE(category)
);

/* the category ids and their monthly archive urls, for example:
https://arxiv.org/year/cs -> /<yymm>
each yymm archive page has a total number of entries that we can scrape
by paginating through the pages. */
CREATE TABLE IF NOT EXISTS categories_monthly_archives (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    /* year is the full year, mm is 01-12 */
    year TEXT NOT NULL,
    mm TEXT NOT NULL,
    archive_url TEXT NOT NULL,
    total_entries INTEGER NOT NULL,
    /* number of entries that have had their paper metadata scraped
    (but NOT pdf downloaded, and NOT extra_metadata scraped) */
    collected_entries INTEGER,
    last_updated_date datetime,

    UNIQUE(archive_url),
    FOREIGN KEY (category) REFERENCES categories (category)
);

/* during an integrity check scrape, if we notice that the total entries
have changed over time, we record that invent here so it can be further investigated.
The values stored in this table represent the values at the time of date_of_mismatch,
which will be out of sync with categories_monthly_archive.total_entries
 */
CREATE TABLE IF NOT EXISTS total_entries_mismatch (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categories_monthly_archive_id INTEGER NOT NULL,
    date_of_mismatch datetime NOT NULL,
    total_entries INTEGER NOT NULL,
    counted_entries INTEGER NOT NULL,

    FOREIGN KEY (categories_monthly_archive_id) REFERENCES categories_monthly_archive (id)
);

/* this is the data scraped from the individual monthly archive urls, for example:
https://arxiv.org/list/cs/2402 */
CREATE TABLE IF NOT EXISTS papers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    papers_extra_metadata_id INTEGER,
    arxiv_id INTEGER,
    title TEXT,
    authors TEXT,
    comment TEXT DEFAULT NULL,
    journal_ref TEXT DEFAULT NULL,
    withdrawn BOOLEAN DEFAULT(FALSE),
    /* null = no download attempt. 't' = download success. 'f' = download failed. */
    failed_to_download TEXT DEFAULT NULL,
    fetched_date datetime,

    UNIQUE(arxiv_id),
    FOREIGN KEY (papers_extra_metadata_id) REFERENCES papers_extra_metadata (id)
);

/* This table is used to store the mapping between papers and categories - many_to_many join table */
CREATE TABLE IF NOT EXISTS papers_categories (
    paper_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,

    PRIMARY KEY (paper_id, category_id)
);

CREATE TABLE IF NOT EXISTS papers_pdfs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_md5_hash TEXT NOT NULL,
    file_name TEXT NOT NULL,
    paper_id INTEGER NOT NULL,
    papers_extra_metadata_id INTEGER,

    UNIQUE(file_md5_hash, file_name),
    FOREIGN KEY (paper_id) REFERENCES papers (id),
    FOREIGN KEY (papers_extra_metadata_id) REFERENCES papers_extra_metadata (id)
);

/* we don't get this information by scraping
the archive urls, but we get it if we manually visit an arxiv paper page
or request the metadata via the api for that particular arxiv id.
the issue with using the regular api for scraping papers is that they don't
include withdrawn papers, and may have hidden papers. */
CREATE TABLE IF NOT EXISTS papers_extra_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    oid TEXT DEFAULT NULL,
    journal_ref TEXT DEFAULT NULL,
    pdf_link TEXT NOT NULL,
    page_link TEXT NOT NULL,
    collected_date datetime,
    published_date datetime,
    updated_date datetime DEFAULT NULL,
    summary TEXT,

    UNIQUE(pdf_link, page_link)
);

/* insert the categories we want to scrape and the oldest year they have papers for */
INSERT OR IGNORE INTO categories (category, end_year) VALUES ('cond-mat', 1992);
INSERT OR IGNORE INTO categories (category, end_year) VALUES ('math-ph', 1996);
INSERT OR IGNORE INTO categories (category, end_year) VALUES ('nlin', 1993);
INSERT OR IGNORE INTO categories (category, end_year) VALUES ('physics', 1996);
INSERT OR IGNORE INTO categories (category, end_year) VALUES ('math', 1992);
INSERT OR IGNORE INTO categories (category, end_year) VALUES ('cs', 1993);
INSERT OR IGNORE INTO categories (category, end_year) VALUES ('q-bio', 2003);
INSERT OR IGNORE INTO categories (category, end_year) VALUES ('q-fin', 2008);
INSERT OR IGNORE INTO categories (category, end_year) VALUES ('stat', 2017);
INSERT OR IGNORE INTO categories (category, end_year) VALUES ('eess', 2017);
INSERT OR IGNORE INTO categories (category, end_year) VALUES ('econ', 2017);
