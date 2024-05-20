import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_words_from_articles(seed_url: str, search_depth=1) -> dict:

    links = list(set(_grab_links_recursively(seed_url, search_depth)))

    links = list(set(links))

    word_dict = {}

    # Below yields about 60k links for a search depth of 2. Investigate.
    for url in tqdm(links):
        text = _get_article_text(url)
        word_dict = _store_words_in_dict(word_dict, text)

    return word_dict


def filter_links(link_list: list) -> list:
    pass


def _grab_links_in_article(url: str) -> list:

    page = requests.get(url)

    ROOT_URL = "https://lt.wikipedia.org"

    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        all_links = [link.get('href') for link in soup.find(
            "div", {"class": "mw-content-ltr mw-parser-output"}).find_all("a") if link.get('href')]
        all_links = [ROOT_URL +
                     i for i in all_links if '/wiki/' in i and '://' not in i]

        # Each link is always listed twice. Bandaid fix.
        all_links = list(set(all_links))

    except AttributeError:
        print(f"No links found at {url}!")
        return []

    return list(set(all_links))


def _grab_links_recursively(seed_url: str, search_depth=1):

    links = [seed_url]
    searched_links = []

    for _ in tqdm(range(search_depth)):

        _new_links = []  # Done this way to avoid changing the iterable mid-iteration

        for url in tqdm(links):

            if url in searched_links:  # Do not search the same url twice for links
                continue

            _new_links.extend(_grab_links_in_article(url))
            searched_links.append(url)

        links.extend(_new_links)

    return links


def _get_article_text(url: str) -> str:

    try:
        page = requests.get(url)

    except requests.exceptions.InvalidSchema:
        # Connection Failed
        return ""

    soup = BeautifulSoup(page.content, 'html.parser')

    # Maybe check if successful connection here. Example of bad connection: https://lt.wikipedia.org/commons.wikimedia.org/wiki/File:Flag_of_Mongolia_(construction_sheet).svg

    try:
        text_div = soup.find(
            "div", {"class": "mw-content-ltr mw-parser-output"})

        article_text = text_div.findAll('p')

        article_text = "".join([i.text for i in article_text]).upper()

    except AttributeError as e:
        print(e)
        print(f"No text found at {url}!")
        return ""

    return article_text


def _store_words_in_dict(collection: dict, article_text: str) -> dict:
    # Adds words/number of occurances of words into a supplied dictionary.

    # Filter out words here

    for word in article_text.split(" "):
        if collection.get(word):
            # counts number of occurrences of any given word to track most common
            collection[word] += 1
        else:
            collection[word] = 1
    return collection
