class SQL:
    def __init__(self, cursor):
        self.cursor = cursor
        pass

    # return a list of Category objects, filled from the database
    def get_categories(self) -> list[dict]:
        categories = []
        self.cursor.execute("SELECT category, end_year FROM categories")
        for row in self.cursor:
            categories.append(
                {"category": row["category"], "end_year": row["end_year"]}
            )
        return categories

    # return a list of archive urls that have been fully scraped
    def get_finished_archive_urls(self):
        self.cursor.execute(
            """SELECT archive_url FROM categories_monthly_archives
            WHERE collected_entries >= total_entries AND total_entries > 0"""
        )

        return [row["archive_url"] for row in self.cursor]
