# generate list of websites to scrape
# scrape text -> assign count to keep track of number of appearances
# go over data -> clean it up. Ensure only valid LT words.
# package words with english translation

from words_from_wiki import get_words_from_articles
from translate import translate_word_list
from utils import write_scores_to_csv
import configparser
from os.path import join


def grab_sorted_words(seed_link: str, search_depth: int):
    """_summary_ Given a seed link an search depth, grab a list of words from an lt.wikipedia link 

    Args:
        seed_link (_type_):str _description_ First link which is searched for words and links
        search_depth (_type_):int _description_ How many links deep do you need to go i.e 0:Don't follow any links, 1:Follow links from first page, 2:Follow links from 1 etc..
    """
    word_dict = get_words_from_articles(SEED_LINK, SEARCH_DEPTH)

    # Sort words based on occurance in the links searched
    sorted_words = sorted(word_dict, key=word_dict.get)

    lt_alphabet = set("ertyuiopasdfghjklzxcvbnmąčęėįšųūž".upper()
                      )  # missing key letters
    # filters out russian, greek alphabets etc.
    sorted_words = [i.capitalize()
                    for i in sorted_words if set(i).issubset(lt_alphabet)]

    return sorted_words


root = "https://lt.wikipedia.org"
SEED_LINK = "https://lt.wikipedia.org/wiki/Taryb%C5%B3_S%C4%85junga"
SEARCH_DEPTH = 0
FLASHCARD_NAME = "TarybJungaSD0_Wiki"

word_list = grab_sorted_words(SEED_LINK, SEARCH_DEPTH)
word_trans_score_list = translate_word_list(word_list)

CONFIG_OBJECT = configparser.ConfigParser()
CONFIG_PATH = "flashcard-config.cfg"
CONFIG_OBJECT.read(CONFIG_PATH)

new_flashcard_path = join(
    CONFIG_OBJECT["Variables"]["flashcard-folder"], FLASHCARD_NAME+".flashcards")

write_scores_to_csv(new_flashcard_path, word_trans_score_list, edit_mode=1)
