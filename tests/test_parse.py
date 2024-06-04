def test_parse(parser):
    assert parser.get_total_entries("https://arxiv.org/list/cs/1805") == 5649
