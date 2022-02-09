import os

from common import get_page_soup, parse_universal, download_track


VGMUSIC_URL = "http://vgmusic.com/"


def parse_consoles_list(page_soup):
    raw_consoles_data = page_soup.find_all("p", {"class": "menu"})
    consoles_list = []

    for element in raw_consoles_data:
        links = element.find_all("a")
        for link in links:
            element_link = link.get("href")

            if "music/console/" in element_link:
                consoles_list.append(element_link[2:])

    print(consoles_list)
    return consoles_list


def get_consoles_list():
    return parse_consoles_list(get_page_soup(VGMUSIC_URL))


def get_songs_from_instrument(console_url):
    return parse_universal(VGMUSIC_URL, console_url, "li")


def processing():
    get_consoles_list()


def main():
    processing()


if __name__ == "__main__":
    main()
