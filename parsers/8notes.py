import os

from common import get_page_soup, parse_universal, download_track


EIGHTNOTES_URL = "https://www.8notes.com/"
URL_POSTFIX = "/all/?orderby=4d"


def parse_instruments_list(page_soup):
    raw_instruments_data = page_soup.find_all("li")
    instruments_list = []

    for element in raw_instruments_data:
        if element and element.a:
            element_link = element.a.get("href")

            if not element.a.get("aria-haspopup") and not element.a.get("id"):
                if "instruments" in element_link:
                    return instruments_list

                instruments_list.append(element_link.replace('/', ''))


def get_pages_songs(elements_raw):
    elements = []

    for element in elements_raw:
        try:
            element_link = element.a.get('href')
            if element_link and 'page' in element_link:
                elements.append(element_link)
        except AttributeError:
            continue
    max_page = elements[-2].split('/')[-1] \
        .replace("?page=", '').replace("&orderby=4d", '')
    return int(max_page)


def get_instruments_list():
    return parse_instruments_list(get_page_soup(EIGHTNOTES_URL))


def get_songs_from_instrument(instrument_url):
    return parse_universal(EIGHTNOTES_URL, instrument_url + URL_POSTFIX, "li")


def get_songs_from_page(page_num, instrument_url):
    return parse_universal(EIGHTNOTES_URL,
                           instrument_url + URL_POSTFIX.replace("?", f"?page={page_num}&"),
                           "tr")


def get_songs_links(tr_list):
    links = []

    for element in tr_list:
        if element.get('onclick'):
            element_link = element.get('onclick').replace("document.location='", '')[1:-1]
            links.append(element_link)
    return links


def parse_download_link(song):
    return parse_universal(EIGHTNOTES_URL, song, "a", "class", "midi_list")


def get_file_name(download_link):
    return download_link.split("/")[-1][:-4].replace("_", '').title()


def processing():
    instruments = get_instruments_list()

    for i, instrument in enumerate(instruments):
        if not os.path.isdir(instrument):
            os.mkdir(instrument)

        songs_raw = get_songs_from_instrument(instrument)
        max_page = get_pages_songs(songs_raw)
        print(f"{instrument} songs is downloading... ({(i + 1)} / {len(instruments)})")

        for page in range(1, max_page + 1):
            tr_list = get_songs_from_page(page, instrument)
            songs = get_songs_links(tr_list)
            print(f"{page} page is downloading... ({page} / {max_page})")

            for j, song in enumerate(songs):
                download_link = parse_download_link(song)
                file_name = get_file_name(download_link)
                print(f"{file_name} track is downloading... ({j + 1} / {len(songs)})")

                if not os.path.isfile(f"{instrument}/{file_name}"):
                    download_track(download_link, f"{instrument}/{file_name}", EIGHTNOTES_URL)


def main():
    processing()


if __name__ == "__main__":
    main()
