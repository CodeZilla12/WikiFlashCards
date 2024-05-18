import tkinter as tk
from utils import get_words_and_scores_from_csv, write_scores_to_csv
import configparser
from os.path import join


class FlashcardViewer(tk.Toplevel):
    def __init__(self):

        tk.Toplevel.__init__(self)

        # Lot of repeated code across project
        self.FLASHCARD_CFG_PATH = "flashcard-config.cfg"
        self.CONFIG_OBJECT = configparser.ConfigParser()
        self.CONFIG_OBJECT.read(self.FLASHCARD_CFG_PATH)

        self.FLASHCARD_FOLDER = self.CONFIG_OBJECT["Variables"]["flashcard-folder"]
        self.SELECTED_FLASHCARD_FILE = self.CONFIG_OBJECT["Variables"]["selected-flashcard-file"]
        self.FLASHCARD_PATH = join(
            self.FLASHCARD_FOLDER, self.SELECTED_FLASHCARD_FILE)

        self.word_trans_score_list = get_words_and_scores_from_csv(
            self.FLASHCARD_PATH)
        self.word_index = 0

        self.geometry("600x200")
        self.title(f"Editing {self.SELECTED_FLASHCARD_FILE.split('.')[0]}")

        # Iterate through each entry in selected config.
        entry_frame = tk.Frame(self)

        # Using width to specify widget width means character length - not pixel length. Find a way for pixel width instead.
        self.word_text_field = tk.Text(entry_frame, height=2, width=74)

        # 1.0 refers to line 1 character 0
        self.word_text_field.insert(
            "1.0", self.word_trans_score_list[self.word_index][0])

        self.trans_text_field = tk.Text(entry_frame, height=2, width=74)

        self.trans_text_field.insert(
            "1.0", self.word_trans_score_list[self.word_index][1])

        self.word_text_field.grid(row=0, column=0)
        self.trans_text_field.grid(row=1, column=0)
        entry_frame.grid(row=0, column=0)

        button_frame = tk.Frame(self)

        next_button = tk.Button(
            button_frame, text="->", command=self.on_next_button_clicked)

        previous_button = tk.Button(button_frame,
                                    text="<-", command=self.on_previous_button_clicked)

        add_new_flashcard_button = tk.Button(
            button_frame, text="+", command=self.on_add_new_flashcard_button_clicked)

        save_button = tk.Button(button_frame,
                                text="save all", command=self.on_save_button_clicked)

        delete_flashcard_button = tk.Button(
            button_frame, text="Delete", command=self.on_delete_flashcard_button_clicked)

        # Packing buttons into frame
        previous_button.grid(row=2, column=0)
        next_button.grid(row=2, column=1)
        add_new_flashcard_button.grid(row=2, column=2)
        save_button.grid(row=2, column=3)

        delete_flashcard_button.grid(row=2, column=4, padx=20)
        button_frame.grid(row=2, column=0, sticky="w")

        # Keybinds not working for some reason
        self.bind_all("<<Modified>>", self.text_modified)
        # self.bind("Right", self.on_next_button_clicked)
        # self.bind("Left", self.on_previous_button_clicked)
        self.focus_set()  # Focuses current frame so that it can take keypress

    def text_modified(self, event):
        pass

    def on_delete_flashcard_button_clicked(self):
        self.word_trans_score_list.pop(self.word_index)
        self.word_index -= 1
        self.on_next_button_clicked()

    def on_next_button_clicked(self, *_):

        self.word_index += 1

        if self.word_index >= len(self.word_trans_score_list):
            self.word_index -= 1
            return

        self.word_text_field.delete('1.0', tk.END)
        self.word_text_field.insert(
            '1.0', self.word_trans_score_list[self.word_index][0])

        self.trans_text_field.delete('1.0', tk.END)
        self.trans_text_field.insert(
            '1.0', self.word_trans_score_list[self.word_index][1])

    def on_previous_button_clicked(self, *_):
        self.word_index -= 1

        if self.word_index < 0:
            self.word_index += 1
            return

        self.word_text_field.delete('1.0', tk.END)
        self.word_text_field.insert(
            '1.0', self.word_trans_score_list[self.word_index][0])

        self.trans_text_field.delete('1.0', tk.END)
        self.trans_text_field.insert(
            '1.0', self.word_trans_score_list[self.word_index][1])

    def on_save_button_clicked(self):
        new_word = self.word_text_field.get("1.0", tk.END).strip("\n")
        new_trans = self.trans_text_field.get("1.0", tk.END).strip("\n")

        # When word is edited, reset the score to zero
        self.word_trans_score_list[self.word_index] = [new_word, new_trans, 0]
        write_scores_to_csv(self.FLASHCARD_PATH,
                            self.word_trans_score_list, edit_mode=True)

    def on_add_new_flashcard_button_clicked(self):
        self.word_trans_score_list.insert(self.word_index, ["", "", 0])
        self.word_index -= 1
        self.on_next_button_clicked()
