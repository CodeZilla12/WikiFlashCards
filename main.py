# generate list of websites to scrape
# scrape text -> assign count to keep track of number of appearances
# go over data -> clean it up. Ensure only valid LT words.
# package words with english translation

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import googletrans
import time

def grab_links_in_article(url: str) -> list:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        all_links = [link.get('href') for link in soup.find(id="bodyContent").find_all("a") if link.get('href')]
        all_links = [i for i in all_links if '/wiki/' in i and '://' not in i]
    except AttributeError:
        print(f"No links found at {url}!")
        return []


    return all_links


def get_article_text(url: str) -> str:
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    #maybe check if successful connection here. Example of bad connection: https://lt.wikipedia.org/commons.wikimedia.org/wiki/File:Flag_of_Mongolia_(construction_sheet).svg

    try:
        article_text = "".join([x.text for x in soup.find(id="bodyContent").find_all('p')]).upper() #improve this to be more selective
        article_text = "".join([i for i in article_text if i.isalpha() or i == " "]).replace("  ", " ").replace("  ", " ")
    except AttributeError:
        print(f"No text found at {url}!")
        return ""


    return article_text


def parse_and_store_article(collection: dict, article_text: str) -> dict:
    for word in article_text.split(" "):
        if collection.get(word):
            collection[word] += 1  # counts number of occurrences of any given word to track most common
        else:
            collection[word] = 1
    return collection


word_collection = {}
link_lst = []

root = "https://lt.wikipedia.org"
SEED_LINK = "https://lt.wikipedia.org/wiki/Taryb%C5%B3_S%C4%85junga"

word_collection = parse_and_store_article(word_collection, get_article_text(SEED_LINK))

SEARCH_DEPTH = 50
MAX_LINKS_PER_ARTICLE = 10
link_lst.extend(grab_links_in_article(SEED_LINK)) #do first pass of link grabbing from zeroth link
link_lst = list(set(link_lst))  # remove any duplicate links

#need a more recursive/async approach to list searching so that it's less prone to crashing due to bad links.

for _ in range(SEARCH_DEPTH):
    new_links = []
    for c,path_ext in enumerate( tqdm(link_lst, leave=False) ): #doesn't check if links have been seen before
        current_url = root + path_ext
        word_collection = parse_and_store_article(word_collection, get_article_text(current_url))
        new_links.extend(grab_links_in_article(current_url))

        if (c == MAX_LINKS_PER_ARTICLE):
            break

    link_lst = list(set(new_links)) #???
    link_lst = new_links

sorted_words = sorted(word_collection, key=word_collection.get) #https://stackoverflow.com/questions/12987178/sort-a-list-based-on-dictionary-values-in-python

lt_alphabet = set("ertyuiopasdfghjklzxcvbnmąčęėįšųūž".upper())
sorted_words = [i for i in sorted_words if set(i).issubset(lt_alphabet)] #filters out russian, greek alphabets etc.

#Notes on translate api
#The maximum character limit on a single text is 15k https://py-googletrans.readthedocs.io/en/latest/
#Google Translate API also has a default limit of 2 million characters per day and 100,000 characters per 100 second https://help.stackby.com/article/71-google-translate
#Can use googletrans.models to perhaps get confidence of translation

TRANSLATE_CHAR_LIMIT = 15_000
DELTA_CHAR = TRANSLATE_CHAR_LIMIT*0.1

CHARS_PER_100_SECONDS = 100_000

total_chars = sum( [len(i) for i in sorted_words] )

translator = googletrans.Translator()

chunked_words = []
previous = 0
current_n_chars = 0
for i,word in enumerate(sorted_words):
    current_n_chars += len(word)

    if current_n_chars >= CHARS_PER_100_SECONDS:
        chunked_words.append(["P"]) #Indicate that this chunk should have a 100 second wait

    coefficient = len(chunked_words) if len(chunked_words) > 0 else 1
    if current_n_chars >= (coefficient*TRANSLATE_CHAR_LIMIT) - DELTA_CHAR:
        current_n_chars -= len(word)
        chunked_words.append(sorted_words[previous:i-1])

        previous = i

print(len(sorted_words))
# print(total_chars)
print(chunked_words)

print("Translating Words...")
time.sleep(1)
translated_words = []

for chunk in tqdm(chunked_words):
    if not chunk:
        continue
    if chunk[0] == "p":
        time.sleep(101)
    translated_words.extend( translator.translate(chunk, dest = 'en', src = 'lt'))  #API is very slow. Multiple minutes.

with open("Words.txt", "w+", encoding='utf-8') as f:
    for lt,en in tqdm(zip(sorted_words,translated_words)):
        f.write(f"{lt}:{en.text}\n")
