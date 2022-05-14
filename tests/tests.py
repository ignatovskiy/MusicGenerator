import bs4


from parsers.common import _get_page_data, get_page_soup, parse_universal


GITHUB_URL = "https://github.com/"


def test_get_page_data():
    test_req = _get_page_data(GITHUB_URL)
    assert test_req.status_code == 200


def test_get_content_page():
    test_req = _get_page_data(GITHUB_URL)
    assert test_req.content is not None


def test_get_page_soup():
    test_soup = get_page_soup(GITHUB_URL)
    assert isinstance(test_soup, bs4.BeautifulSoup)


def test_parse_universal():
    test_list = parse_universal(GITHUB_URL, "", "a")
    assert isinstance(test_list, list)



