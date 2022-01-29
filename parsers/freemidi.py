import requests
from bs4 import BeautifulSoup


FREEMIDI_URL = "https://freemidi.org/"


def get_page_data(url):
    return requests.get(url)


def get_content_page(page_data):
    return page_data.content


def get_page_soup(page_content):
    return BeautifulSoup(page_content, features="lxml")


def parse_genres_list(page_soup):
    raw_genres_data = page_soup.find_all("li")
    genres_list = []

    for element in raw_genres_data:
        if element and element.a:
            element_link = element.a.get("href")

            if "genre" in element_link:
                genres_list.append(element_link)
    return genres_list


def get_genres_list():
    return parse_genres_list(get_page_soup(get_content_page(get_page_data(FREEMIDI_URL))))


def get_artists_from_genre(genre):
    page_soup = get_page_soup(get_content_page(get_page_data(FREEMIDI_URL + genre)))
    artists = page_soup.find_all("div", {"class": "genre-link-text"})
    return [artist.a.get("href") for artist in artists]


def main():
    genres = get_genres_list()
    test_artist = get_artists_from_genre(genres[0])
    print(test_artist)


if __name__ == "__main__":
    main()
