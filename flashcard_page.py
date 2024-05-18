import tkinter as tk
from functools import partial
from os.path import join
import configparser
from random import choices
import numpy as np
from utils import get_words_and_scores_from_csv, write_scores_to_csv

FONTSIZE = 30
FONT = ("Helvetica", FONTSIZE)


class FlashcardPage(tk.Frame):

    # Long __init__. Needs refactor?
    def __init__(self, parent: tk.Frame, controller: tk.Tk):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.FLASHCARD_CFG_PATH = "flashcard-config.cfg"
        self.CONFIG_OBJECT = configparser.ConfigParser()
        self.CONFIG_OBJECT.read(self.FLASHCARD_CFG_PATH)

        flashcard_folder = self.CONFIG_OBJECT["Variables"]["flashcard-folder"]
        flashcard_csv_name = self.CONFIG_OBJECT["Variables"]["selected-flashcard-file"]

        self.WORD_CSV_PATH = join(flashcard_folder, flashcard_csv_name)

        temp_word_trans_score_list = get_words_and_scores_from_csv(
            self.WORD_CSV_PATH)

        _abs_lower_score_limit = abs(float(
            self.CONFIG_OBJECT["FlashCard-Preferences"]["lower_score_limit"]))

        _k = k = int(
            self.CONFIG_OBJECT["FlashCard-Preferences"]["words_per_session"])

        if len(temp_word_trans_score_list) < _k:
            _k = len(temp_word_trans_score_list)

        _list = []

        while len(_list) < _k:
            # Weighted such that scores approaching the lower score limit are significantly more likely to appear,
            # the +1 mitigates any divide by zero errors as scores lower than the negative shouldn't be possible.
            _weights = [1/(score+1+_abs_lower_score_limit) for _,
                        _, score in temp_word_trans_score_list]

            _word_list = choices(temp_word_trans_score_list,
                                 weights=_weights, k=2*_k)

            temp_word_trans_score_list = [
                i for i in temp_word_trans_score_list if i not in _list]

            # Used np.unique as set() doesn't work on lists
            _unique_words = np.unique(_word_list, axis=0)

            _unique_words = [
                [word, trans, float(score)] for word, trans, score in _unique_words]  # np arrays have to have homogenous type, so they convert score to string. This reverses that.

            _list.extend(_unique_words)

        # The while loop can introduce extra words, this cuts it off at the maximum defined in config
        self.word_trans_score_list = _list[:_k]
        self.word_index = 0

        self.waiting_for_answer = False
        self.word_list_complete = False

        go_home_button = tk.Button(
            self, text="Return Home", command=self.go_home_button_clicked)
        go_home_button.pack(anchor='ne')

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

    def go_home_button_clicked(self):
        self.controller.show_frame("HomePage")

    def reset_all_scores(self, *_):

        # rewrite this to redo all scores from csv instead of only selected x scores
        self.word_trans_score_list = [[word, trans, 0]
                                      for word, trans, score in self.word_trans_score_list]
        write_scores_to_csv(
            self.WORD_CSV_PATH, self.word_trans_score_list)
        print("Word scores reset")

    def kill_program(self, *_):

        print("Ending Program...")

        self.controller.destroy()
        quit()

    def display_next_word(self):
        self.word_index += 1

        write_scores_to_csv(
            self.WORD_CSV_PATH, self.word_trans_score_list)

        if self.word_index >= len(self.word_trans_score_list):

            # Here switch to the graph page.
            self.word_list_complete = True
            self.displayed_word.config(text="Complete")
            self.show_word_button.pack_forget()

            self.controller.show_frame("GraphPage")

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

        LOWER_LIMIT = float(
            self.CONFIG_OBJECT["FlashCard-Preferences"]["lower_score_limit"])
        UPPER_LIMIT = float(
            self.CONFIG_OBJECT["FlashCard-Preferences"]["upper_score_limit"])

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
