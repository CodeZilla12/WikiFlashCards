import googletrans
import time
from tqdm import tqdm


# Notes on translate api
# The maximum character limit on a single text is 15k https://py-googletrans.readthedocs.io/en/latest/
# Google Translate API also has a default limit of 2 million characters per day and 100,000 characters per 100 second https://help.stackby.com/article/71-google-translate
# Can use googletrans.models to perhaps get confidence of translation


TRANSLATE_CHAR_LIMIT = 15_000
DELTA_CHAR = TRANSLATE_CHAR_LIMIT*0.1
CHARS_PER_100_SECONDS = 100_000


def translate_word_list(word_list: list):

    total_chars = sum([len(i) for i in word_list])

    translator = googletrans.Translator()

    chunked_words = []
    previous = 0
    current_n_chars = 0
    for i, word in enumerate(word_list):
        current_n_chars += len(word)

        if current_n_chars >= CHARS_PER_100_SECONDS:
            # Indicate that this chunk should have a 100 second wait
            chunked_words.append(["P"])

        coefficient = len(chunked_words) if len(chunked_words) > 0 else 1
        if current_n_chars >= (coefficient*TRANSLATE_CHAR_LIMIT) - DELTA_CHAR:
            current_n_chars -= len(word)
            chunked_words.append(word_list[previous:i-1])

            previous = i

    print(len(word_list))
    # print(total_chars)
    print(chunked_words)

    print("Translating Words...")
    time.sleep(1)
    translated_words = []

    for chunk in tqdm(chunked_words):
        if not chunk:
            continue
        if chunk[0] == "P":
            time.sleep(101)
        # API is very slow. Multiple minutes.
        translated_words.extend(
            translator.translate(chunk, dest='en', src='lt'))

    with open("Words.txt", "w+", encoding='utf-8') as f:
        for lt, en in tqdm(zip(word_list, translated_words)):
            f.write(f"{lt}:{en.text}\n")
