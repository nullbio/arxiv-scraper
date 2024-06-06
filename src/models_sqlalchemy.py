# from typing import List, Optional
import databases
import ormar
import sqlalchemy

# Initialize database and metadata
DATABASE_URL = "sqlite:///arxiv.db"

# base_ormar_config
boc = ormar.OrmarConfig(
    database=databases.Database(DATABASE_URL),
    metadata=sqlalchemy.MetaData(),
    engine=sqlalchemy.create_engine(DATABASE_URL),
)


class Category(ormar.Model):
    ormar_config = boc.copy(tablename="category")

    id = ormar.Integer(primary_key=True, autoincrement=True)
    name = ormar.Text(nullable=False, unique=True)
    end_year = ormar.Integer(nullable=False)


class MonthlyArchive(ormar.Model):
    ormar_config = boc.copy(tablename="monthly_archive")

    id = ormar.Integer(primary_key=True, autoincrement=True)
    category_id = ormar.ForeignKey(Category, nullable=False)
    year = ormar.Text(max_length=4, nullable=False)
    mm = ormar.Text(max_length=2, nullable=False)
    archive_url = ormar.Text(unique=True, nullable=False)
    total_entries = ormar.Integer(nullable=False)
    scraped_entries = ormar.Integer(nullable=False)
    created_at = ormar.DateTime()
    updated_at = ormar.DateTime(nullable=True)


class TotalEntriesMismatch(ormar.Model):
    ormar_config = boc.copy(tablename="total_entries_mismatch")

    id = ormar.Integer(primary_key=True, autoincrement=True)
    monthly_archive_id = ormar.ForeignKey(MonthlyArchive, nullable=False)
    total_entries = ormar.Integer(nullable=False)
    counted_entries = ormar.Integer(nullable=False)
    created_at = ormar.DateTime(nullable=False)
    updated_at = ormar.DateTime(nullable=True)


class PDF(ormar.Model):
    ormar_config = boc.copy(tablename="pdf")

    id = ormar.Integer(primary_key=True, autoincrement=True)
    file_md5_hash = ormar.Text(
        max_length=32, min_length=32, unique=True, nullable=False
    )
    file_name = ormar.Text(unique=True, nullable=False)
    created_at = ormar.DateTime(nullable=False)
    updated_at = ormar.DateTime(nullable=True)


class Paper(ormar.Model):
    ormar_config = boc.copy(tablename="paper")

    id = ormar.Integer(primary_key=True, autoincrement=True)
    arxiv_id = ormar.Text(unique=True, nullable=False)
    title = ormar.Text(nullable=False)
    authors = ormar.Text(nullable=False)
    comment = ormar.Text(nullable=True)
    journal_ref = ormar.Text(nullable=True)
    pdf_link = ormar.Text(unique=True, nullable=False)
    page_link = ormar.Text(unique=True, nullable=False)
    withdrawn = ormar.Boolean(default=False)
    summary = ormar.Text(nullable=True)
    doi = ormar.Text(nullable=True)
    related_doi = ormar.Text(nullable=True)
    report_no = ormar.Text(nullable=True)
    published_date = ormar.DateTime(nullable=True)
    updated_date = ormar.DateTime(nullable=True)
    download_failed = ormar.Boolean(default=False)
    pdf_id = ormar.ForeignKey(PDF, nullable=True)
    created_at = ormar.DateTime(nullable=False)
    updated_at = ormar.DateTime(nullable=True)


class PaperCategory(ormar.Model):
    ormar_config = boc.copy(tablename="paper_category")

    id = ormar.Integer(primary_key=True, autoincrement=True)
    paper_id = ormar.ForeignKey(Paper, nullable=False)
    category_id = ormar.ForeignKey(Category, nullable=False)
    # paper_id: List[Paper] = ormar.ManyToMany(Paper)
    # category_id: List[Category] = ormar.ManyToMany(Category)
