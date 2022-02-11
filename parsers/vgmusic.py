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

    return consoles_list


def get_consoles_list():
    return parse_consoles_list(get_page_soup(VGMUSIC_URL))


def get_songs_from_console(console_url):
    return parse_universal(VGMUSIC_URL, console_url, "td")


def parse_songs_from_console(links):
    songs_list = []

    for link in links:
        if link.a and not link.get("align") and not link.get("class"):
            songs_list.append(link.a.get("href"))

    return songs_list


def get_file_name(download_link):
    return download_link[:-4]


def processing():
    consoles = get_consoles_list()

    for i, console in enumerate(consoles):
        console_name = console.split("/")[-2].title()
        if not os.path.isdir(console_name):
            os.mkdir(console_name)

        raw_songs_links = get_songs_from_console(console)
        print(f"{console_name} songs is downloading... ({(i + 1)} / {len(consoles)})")

        songs = parse_songs_from_console(raw_songs_links)

        for j, song in enumerate(songs):
            try:
                file_name = get_file_name(song)
                print(f"{file_name} track is downloading... ({j + 1} / {len(songs)})")

                if not os.path.isfile(f"{console_name}/{file_name}.mid"):
                    download_track(console + song,
                                   f"{console_name}/{file_name}",
                                   VGMUSIC_URL)
            except IndexError:
                continue


def main():
    processing()


if __name__ == "__main__":
    main()
