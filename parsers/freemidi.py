import os

import requests
from bs4 import BeautifulSoup


FREEMIDI_URL = "https://freemidi.org/"


def _get_page_data(url, stream=None, allow_redirects=False):
    return requests.get(url, stream=stream, allow_redirects=allow_redirects)


def _get_content_page(page_data):
    return page_data.content


def _get_page_soup(page_content):
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


def get_page_soup(url):
    return _get_page_soup(_get_content_page(_get_page_data(url)))


def get_genres_list():
    return parse_genres_list(get_page_soup(FREEMIDI_URL))


def parse_universal(url, postfix, main_element, att, value):
    page_soup = get_page_soup(url + postfix)
    elements = page_soup.find_all(main_element, {att: value})

    if main_element == "a":
        return elements[0].get("href")
    elif main_element == "ul":
        return int(elements[0].text.split('\n')[2].strip().replace('»', '').strip()[-1])
    else:
        return [element.a.get("href") for element in elements]


def get_artists_from_genre(genre_url):
    return parse_universal(FREEMIDI_URL, genre_url, "div", "class", "genre-link-text")


def get_tracks_from_artists(artist_url):
    return parse_universal(FREEMIDI_URL, artist_url, "div", "class", "artist-song-cell")


def get_track_download_link(track_url):
    return parse_universal(FREEMIDI_URL, track_url, "a", "id", "downloadmidi")


def get_pages_tracks(artist_url):
    return parse_universal(FREEMIDI_URL, artist_url, "ul", "class", "pagination")


def get_genre_name(genre):
    return " ".join(genre.split('-')[1:]).title()


def get_artist_name(artist_url):
    return " ".join(artist_url.split('-')[2:]).title()


def get_track_name(track_url):
    return " ".join(track_url.split('-')[2:-1]).title()


def download_track(download_link, path):
    track_raw = _get_content_page(_get_page_data(FREEMIDI_URL + download_link, allow_redirects=False))
    with open(path + ".mid", "wb") as f:
        f.write(track_raw)


def processing():
    genres = get_genres_list()

    for i, genre in enumerate(genres):
        genre_name = get_genre_name(genre)
        print(f"{genre_name} genre is downloading... ({(i + 1)} / {len(genres)})")
        os.mkdir(genre_name)

        artists = get_artists_from_genre(genre)
        for j, artist in enumerate(artists):
            artist_name = get_artist_name(artist)
            print(f"{artist_name} artist is downloading... ({(j + 1)} / {len(artists)})")
            os.mkdir(f"{genre_name}/{artist_name}")

            pages = get_pages_tracks(artist)
            for page in range(pages):
                print(f"{page + 1} page is downloading... ({page + 1} / {pages})")
                tracks = get_tracks_from_artists(f"{artist}-P-{page}")
                artist_name_part = " ".join(artist_name.split()[:-1])

                for k, track in enumerate(tracks):
                    track_name = get_track_name(track)
                    if track_name.endswith(artist_name_part):
                        track_name = track_name.replace(artist_name_part, '').strip()
                    print(f"{track_name} track is downloading... ({(k + 1)} / {len(tracks)})")

                    track_link = get_track_download_link(track)
                    download_track(track_link, f"{genre_name}/{artist_name}/{track_name}")


def main():
    processing()


if __name__ == "__main__":
    main()
