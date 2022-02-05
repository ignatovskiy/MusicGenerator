from common import get_page_soup


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


def get_instruments_list():
    return parse_instruments_list(get_page_soup(EIGHTNOTES_URL))


def processing():
    instruments_list = get_instruments_list()
    print(instruments_list)


def main():
    processing()


if __name__ == "__main__":
    main()
