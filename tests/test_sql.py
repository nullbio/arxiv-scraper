from datetime import datetime, timezone


class TestClassSQL:
    # make sure the init script worked properly and initialized the db
    def test_init(self, sql):
        # check if database was created, and tables
        assert sql.db_file == "arxiv.test.db"

        # count number of tables in database
        assert (
            sql.cursor.execute("SELECT * FROM categories").fetchone()
            is not None
        )
        assert sql.cursor.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table'"
        ).fetchone()[0] > 0  # fmt: skip

    def test_get_categories(self, sql):
        # check if database was created, and tables
        c = sql.get_categories()

        assert len(c) > 0

        c1, c2 = [], []
        for row in c:
            c1.append(row["category"])
            c2.append(row["end_year"])

        assert "cs" in c1
        assert 1993 in c2

    def test_get_finished_archive_urls(self, sql):
        assert len(sql.get_finished_archive_urls()) == 0

        sql.cursor.execute(
            """INSERT INTO categories_monthly_archives
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                1,
                "cs",
                "2015",
                "01",
                "https://arxiv.org/list/cs/1501",
                5,
                0,
                datetime.now(timezone.utc),
            ),
        )
        assert len(sql.get_finished_archive_urls()) == 0

        sql.cursor.execute(
            """UPDATE categories_monthly_archives
            SET collected_entries = 2 WHERE id = 1"""
        )
        assert len(sql.get_finished_archive_urls()) == 0

        sql.cursor.execute(
            """UPDATE categories_monthly_archives SET
            collected_entries = 5 WHERE id = 1"""
        )
        assert len(sql.get_finished_archive_urls()) == 1
        return
