import requests
from bs4 import BeautifulSoup


def _get_page_data(url, stream=None, allow_redirects=False):
    return requests.get(url, stream=stream, allow_redirects=allow_redirects)


def _get_content_page(page_data):
    return page_data.content


def _get_page_soup(page_content):
    return BeautifulSoup(page_content, features="lxml")


def get_page_soup(url):
    return _get_page_soup(_get_content_page(_get_page_data(url)))


def parse_universal(url, postfix, main_element, att=None, value=None):
    page_soup = get_page_soup(url + postfix)

    if att and value:
        elements = page_soup.find_all(main_element, {att: value})
    else:
        elements_raw = page_soup.find_all(main_element)
        return elements_raw

    if main_element == "a":
        return elements[0].get("href")
    if main_element == "ul":
        return int(elements[0].text.split('\n')[2].strip().replace('»', '').strip()[-1])
    return [element.a.get("href") for element in elements]


def download_track(download_link, path, url):
    track_raw = _get_content_page(_get_page_data
                                  (url + download_link, allow_redirects=False))
    with open(path + ".mid", "wb") as file:
        file.write(track_raw)
