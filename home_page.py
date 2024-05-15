import tkinter as tk
import configparser
from os.path import join
from os import listdir

FLASHCARD_CFG_PATH = "flashcard-config.cfg"
CONFIG_OBJECT = configparser.ConfigParser()
CONFIG_OBJECT.read(FLASHCARD_CFG_PATH)


class HomePage(tk.Frame):

    def __init__(self: tk.Frame, parent: tk.Frame, controller: tk.Tk):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        label = tk.Label(self, text="FlashcardFile")
        label.grid(row=0, column=0)

        self.selected_file_tkstring = tk.StringVar(self)

        flashcard_file_folder = CONFIG_OBJECT["Variables"]["flashcard-folder"]
        selected_flashcard_file_path = CONFIG_OBJECT["Variables"]["selected-flashcard-file"]
        self.selected_file_tkstring.set(selected_flashcard_file_path)

        flashcard_file_list = listdir(flashcard_file_folder)

        option_menu = tk.OptionMenu(
            self, self.selected_file_tkstring, *flashcard_file_list, command=self.on_new_flashcard_file_selected)
        option_menu.grid(row=0, column=1)

        button = tk.Button(self, text="Start Flashcards",
                           command=self.start_flash_cards)
        button.grid(row=1, column=0)

    def start_flash_cards(self):

        self.controller.show_frame("FlashcardPage")

    def on_new_flashcard_file_selected(self, _):
        new_flashcard_file_name = self.selected_file_tkstring.get()

        CONFIG_OBJECT["Variables"]["selected-flashcard-file"] = new_flashcard_file_name

        with open("flashcard-config.cfg", "w") as f:
            CONFIG_OBJECT.write(f)
