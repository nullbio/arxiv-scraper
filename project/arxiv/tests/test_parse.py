class TestParse:
    def test_parse(self, parse):
        url = "https://arxiv.org/list/cs/1805"
        fpath = "tests/html/total_entries.html"
        with open(fpath, "r") as file:
            html_content = file.read()
            assert parse.total_entries(html_content, url) == 5648
