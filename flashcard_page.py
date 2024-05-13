import tkinter as tk
from functools import partial
import csv
from os.path import isfile
import configparser

FONTSIZE = 30
FONT = ("Helvetica", FONTSIZE)

# Initialises the config and reads "flashcard-config.cfg" file contents into memory.
FLASHCARD_CFG_PATH = "flashcard-config.cfg"
CONFIG_OBJECT = configparser.ConfigParser()
CONFIG_OBJECT.read(FLASHCARD_CFG_PATH)


class FlashcardPage(tk.Frame):
    def __init__(self, parent: tk.Frame, controller: tk.Tk):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.WORD_CSV_PATH = "word_scores.csv"
        self.word_trans_score_list = self.get_words_and_scores_from_csv(
            self.WORD_CSV_PATH)
        self.word_index = 0
        self.waiting_for_answer = False
        self.word_list_complete = False

        # Initialising Initial display widgets
        self.displayed_word = tk.Label(
            self, text=self.word_trans_score_list[self.word_index][0], font=FONT)
        self.displayed_word.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        self.show_word_button = tk.Button(
            self, text="Show Word (space)", command=self.show_word_button_clicked)
        self.show_word_button.pack(side=tk.BOTTOM, pady=20)

        # Initialising answering widgets
        self.button_frame = tk.Frame()

        self.SCORE_VALUE_DICT = {
            "easy": 1,
            "okay": 0.5,
            "hard": 0.25,
            "fail": -1
        }

        # Instead of generating these every time - have them show and hide accordingly
        self.easy_button = tk.Button(self.button_frame, text="Easy (v)", command=partial(
            self.answer_button_clicked, "easy"))
        self.hard_button = tk.Button(self.button_frame, text="Hard (x)", command=partial(
            self.answer_button_clicked, "hard"))
        self.okay_button = tk.Button(self.button_frame, text="Okay (c)", command=partial(
            self.answer_button_clicked, "okay"))
        self.fail_button = tk.Button(self.button_frame, text="Fail (z)", command=partial(
            self.answer_button_clicked, "fail"))

        # Packs buttons into button_frame side-by-side
        self.fail_button.grid(row=0, column=0)
        self.hard_button.grid(row=0, column=1)
        self.okay_button.grid(row=0, column=2)
        self.easy_button.grid(row=0, column=3)

        # Initialising Hotkeys
        self.bind("<Escape>", self.kill_program)
        self.bind("<Control-r>", self.reset_all_scores)
        self.bind("<space>", self.show_word_button_clicked)
        self.bind("z", partial(self.answer_button_clicked, "fail"))
        self.bind("x", partial(self.answer_button_clicked, "hard"))
        self.bind("c", partial(self.answer_button_clicked, "okay"))
        self.bind("v", partial(self.answer_button_clicked, "easy"))
        self.focus_set()  # Focuses current frame so that it can take keypresses

    def reset_all_scores(self, *_):
        self.word_trans_score_list = [[word, trans, 0]
                                      for word, trans, score in self.word_trans_score_list]
        self.write_scores_to_csv(
            self.WORD_CSV_PATH, self.word_trans_score_list)
        print("Word scores reset")

    @staticmethod
    def get_words_and_scores_from_csv(file_path: str) -> list:

        # Items are stored in the csv as:
        # word,score[/n]word,score[\n]....
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

    @staticmethod
    def write_scores_to_csv(file_path: str, word_trans_score_list: list) -> None:
        with open(file_path, 'w', encoding="utf-8") as f:
            csv_writer = csv.writer(f, delimiter=",", lineterminator="\n")

            csv_writer.writerows(word_trans_score_list)

    def kill_program(self, *_):

        print("Ending Program...")

        self.controller.destroy()

    def display_next_word(self):
        self.word_index += 1

        self.write_scores_to_csv(
            self.WORD_CSV_PATH, self.word_trans_score_list)

        # print("Saved Score")

        if self.word_index >= len(self.word_trans_score_list):
            self.word_list_complete = True
            self.displayed_word.config(text="Complete")
            self.show_word_button.pack_forget()
            return

        self.displayed_word.config(
            text=self.word_trans_score_list[self.word_index][0])

    def show_word_button_clicked(self, *_):

        # *_ is to capture keyboard event input.

        # In case of function called from hotkey
        if self.word_list_complete:
            return

        if self.waiting_for_answer:

            self.displayed_word.configure(
                text=self.word_trans_score_list[self.word_index][0])

            self.button_frame.pack_forget()
            self.show_word_button.pack(side=tk.BOTTOM, pady=20)
            self.waiting_for_answer = False
            return

        self.waiting_for_answer = True
        self.displayed_word.configure(
            text=self.word_trans_score_list[self.word_index][1])
        self.show_word_button.pack_forget()

        self.button_frame.pack(side=tk.BOTTOM, pady="10px")

    def answer_button_clicked(self, answer: str, *_):

        # *_ is to capture keyboard event input.

        # In case of function called from hotkey
        if not self.waiting_for_answer or self.word_list_complete:
            return

        current_score = self.word_trans_score_list[self.word_index][2]

        LOWER_LIMIT = -5
        UPPER_LIMIT = +5

        current_score = self.word_trans_score_list[self.word_index][2]
        bonus_score = self.SCORE_VALUE_DICT[answer]
        new_score = current_score + bonus_score

        if new_score < LOWER_LIMIT:
            new_score = LOWER_LIMIT
        elif new_score > UPPER_LIMIT:
            new_score = UPPER_LIMIT

        self.word_trans_score_list[self.word_index][2] = new_score

        self.button_frame.pack_forget()
        self.show_word_button.pack(side=tk.BOTTOM, pady=20)
        self.display_next_word()
        self.waiting_for_answer = False
