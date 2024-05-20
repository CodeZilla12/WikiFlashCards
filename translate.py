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

    word_string = ".".join(word_list)

    total_chars = sum([len(i) for i in word_string])

    translator = googletrans.Translator()

    assert total_chars <= TRANSLATE_CHAR_LIMIT, "Too many words, in future update will implement chunking. Choose a different article or lower chunk depth."

    translated_words = translator.translate(
        word_string, dest='en', src='lt').text.split(".")

    word_trans_score_list = [[word, trans, 0]
                             for word, trans in zip(word_list, translated_words)]

    return word_trans_score_list
