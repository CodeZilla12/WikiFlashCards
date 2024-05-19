# generate list of websites to scrape
# scrape text -> assign count to keep track of number of appearances
# go over data -> clean it up. Ensure only valid LT words.
# package words with english translation

from words_from_wiki import get_words_from_articles

from tqdm import tqdm
import googletrans
import time

root = "https://lt.wikipedia.org"
SEED_LINK = "https://lt.wikipedia.org/wiki/Taryb%C5%B3_S%C4%85junga"
SEARCH_DEPTH = 1

word_dict = get_words_from_articles(SEED_LINK, SEARCH_DEPTH)

# https://stackoverflow.com/questions/12987178/sort-a-list-based-on-dictionary-values-in-python
sorted_words = sorted(word_dict, key=word_dict.get)

lt_alphabet = set("ertyuiopasdfghjklzxcvbnmąčęėįšųūž".upper()
                  )  # missing key letters
# filters out russian, greek alphabets etc.
sorted_words = [i for i in sorted_words if set(i).issubset(lt_alphabet)]

print(sorted_words)

quit()

# Notes on translate api
# The maximum character limit on a single text is 15k https://py-googletrans.readthedocs.io/en/latest/
# Google Translate API also has a default limit of 2 million characters per day and 100,000 characters per 100 second https://help.stackby.com/article/71-google-translate
# Can use googletrans.models to perhaps get confidence of translation

TRANSLATE_CHAR_LIMIT = 15_000
DELTA_CHAR = TRANSLATE_CHAR_LIMIT*0.1

CHARS_PER_100_SECONDS = 100_000

total_chars = sum([len(i) for i in sorted_words])

translator = googletrans.Translator()

chunked_words = []
previous = 0
current_n_chars = 0
for i, word in enumerate(sorted_words):
    current_n_chars += len(word)

    if current_n_chars >= CHARS_PER_100_SECONDS:
        # Indicate that this chunk should have a 100 second wait
        chunked_words.append(["P"])

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
    # API is very slow. Multiple minutes.
    translated_words.extend(translator.translate(chunk, dest='en', src='lt'))

with open("Words.txt", "w+", encoding='utf-8') as f:
    for lt, en in tqdm(zip(sorted_words, translated_words)):
        f.write(f"{lt}:{en.text}\n")
