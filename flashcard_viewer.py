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
        self.title("Flashcard Viewer")

        # Iterate through each entry in selected config.

        e1 = tk.Entry(self)
        e2 = tk.Entry(self)

        e1.grid(row=0, column=0)
        e2.grid(row=1, column=0)

        button_frame = tk.Frame(self)

        next_button = tk.Button(
            button_frame, text="->", command=self.on_next_button_clicked)

        previous_button = tk.Button(button_frame,
                                    text="<-", command=self.on_previous_button_clicked)

        add_new_flashcard_button = tk.Button(
            button_frame, text="+", command=self.on_add_new_flashcard_button_clicked)

        save_button = tk.Button(button_frame,
                                text="save", command=self.on_save_button_clicked)

        # Packing buttons into frame
        previous_button.grid(row=2, column=0)
        next_button.grid(row=2, column=1)
        add_new_flashcard_button.grid(row=2, column=2)
        save_button.grid(row=2, column=3)
        button_frame.grid(row=2, column=0)

        self.mainloop()

    def on_next_button_clicked(self):
        pass

    def on_previous_button_clicked(self):
        pass

    def on_save_button_clicked(self):
        pass

    def on_add_new_flashcard_button_clicked(self):
        pass
