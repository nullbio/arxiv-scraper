/* We use migrations instead of this file, this is just kept here for reference. */
/* There are no gaurantees it is up to date. */
CREATE TABLE IF NOT EXISTS category (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    end_year INTEGER NOT NULL
);

/* the category ids and their monthly archive urls, for example:
https://arxiv.org/year/cs -> /<yymm>
each yymm archive page has a total number of entries that we can scrape
by paginating through the pages. */
CREATE TABLE IF NOT EXISTS monthly_archive (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL REFERENCES category (id),
    /* year is the full year, mm is 01-12 */
    year TEXT NOT NULL,
    mm TEXT NOT NULL,
    archive_url TEXT UNIQUE NOT NULL,
    total_entries INTEGER NOT NULL,
    /* number of entries that have had their paper metadata scraped
    (but NOT pdf downloaded, and NOT extra_metadata scraped) */
    scraped_entries INTEGER NOT NULL,

    created_at datetime NOT NULL,
    updated_at datetime DEFAULT NULL
);

/* during an integrity check scrape, if we notice that the total entries
have changed over time, we record that invent here so it can be further investigated.
The values stored in this table represent the values at the time of date_of_mismatch,
which will be out of sync with categories_monthly_archive.total_entries
 */
CREATE TABLE IF NOT EXISTS total_entries_mismatch (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    monthly_archive_id INTEGER NOT NULL REFERENCES monthly_archive (id),
    total_entries INTEGER NOT NULL,
    counted_entries INTEGER NOT NULL,

    created_at datetime NOT NULL,
    updated_at datetime DEFAULT NULL
);

/* this is the data scraped from the individual monthly archive urls, for example:
https://arxiv.org/list/cs/2402 */
CREATE TABLE IF NOT EXISTS paper (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    arxiv_id TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    authors TEXT NOT NULL,
    comment TEXT DEFAULT NULL,
    journal_ref TEXT DEFAULT NULL,
    pdf_link TEXT NOT NULL UNIQUE,
    page_link TEXT NOT NULL UNIQUE,
    withdrawn BOOLEAN DEFAULT(FALSE),

    /* additional metadata fields that aren't visible on the archive page. */
    summary TEXT DEFAULT NULL,
    doi TEXT DEFAULT NULL,
    related_doi TEXT DEFAULT NULL,
    report_no TEXT DEFAULT NULL,
    published_date datetime DEFAULT NULL,
    updated_date datetime DEFAULT NULL,
    
    /* pdf download */
    download_failed BOOLEAN DEFAULT(FALSE),
    pdf_id INTEGER REFERENCES pdf (id),

    created_at datetime NOT NULL,
    updated_at datetime DEFAULT NULL
);

/* This table is used to store the mapping between papers and categories - many_to_many join table */
CREATE TABLE IF NOT EXISTS paper_category (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    paper_id INTEGER NOT NULL REFERENCES paper (id),
    category_id INTEGER NOT NULL REFERENCES category (id)
);

CREATE TABLE IF NOT EXISTS pdf (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    file_md5_hash TEXT NOT NULL UNIQUE,
    file_name TEXT NOT NULL UNIQUE,

    created_at datetime NOT NULL,
    updated_at datetime DEFAULT NULL
);

/* insert the categories we want to scrape and the oldest year they have papers for */
INSERT OR IGNORE INTO category (name, end_year) VALUES ('cond-mat', 1992);
INSERT OR IGNORE INTO category (name, end_year) VALUES ('math-ph', 1996);
INSERT OR IGNORE INTO category (name, end_year) VALUES ('nlin', 1993);
INSERT OR IGNORE INTO category (name, end_year) VALUES ('physics', 1996);
INSERT OR IGNORE INTO category (name, end_year) VALUES ('math', 1992);
INSERT OR IGNORE INTO category (name, end_year) VALUES ('cs', 1993);
INSERT OR IGNORE INTO category (name, end_year) VALUES ('q-bio', 2003);
INSERT OR IGNORE INTO category (name, end_year) VALUES ('q-fin', 2008);
INSERT OR IGNORE INTO category (name, end_year) VALUES ('stat', 2017);
INSERT OR IGNORE INTO category (name, end_year) VALUES ('eess', 2017);
INSERT OR IGNORE INTO category (name, end_year) VALUES ('econ', 2017);
