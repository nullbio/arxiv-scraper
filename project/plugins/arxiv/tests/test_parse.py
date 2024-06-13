from pathlib import Path

import pytest

testspath = BASE_DIR = Path(__file__).resolve().parent


class TestParse:
    def test_parse(self, parse):
        url = "https://arxiv.org/list/cs/1805"
        fpath = f"{testspath}/html/total_entries.html"
        with open(fpath, "r") as file:
            html_content = file.read()
            assert parse.total_entries(html_content, url) == 5648
