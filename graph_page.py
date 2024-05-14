import tkinter as tk
import csv
import configparser

FLASHCARD_CFG_PATH = "flashcard-config.cfg"
CONFIG_OBJECT = configparser.ConfigParser()
CONFIG_OBJECT.read(FLASHCARD_CFG_PATH)


class GraphPage(tk.Frame):

    # Long __init__. Needs refactor?
    def __init__(self, parent: tk.Frame, controller: tk.Tk):
        tk.Frame.__init__(self, parent)

        self.controller = controller

    @ staticmethod
    def get_words_and_scores_from_csv(file_path: str) -> list:

        # This should be moved to an external utilities function as it will likely be used in many places.

        # Items are stored in the csv as:
        # word, trans, score[/n]word,trans,score[\n]....
        word_list = []

        if not isfile(file_path):
            raise FileNotFoundError("word_scores.csv missing")

        with open(file_path, 'r', encoding="utf8") as f:
            csv_reader = csv.reader(f, delimiter=",")
            for row in csv_reader:

                if len(row) == 0:
                    continue

                if len(row) == 2:  # Make this check more specific
                    row.append(0)

                word, translated_word, score = row
                word_list.append([word, translated_word, float(score)])

        return word_list
