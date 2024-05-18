import tkinter as tk
import configparser
from os.path import join
from os import listdir
from utils import get_words_and_scores_from_csv, write_scores_to_csv
from flashcard_viewer import FlashcardViewer

# Have it make a backup of flashcard files on startup


class HomePage(tk.Frame):

    def __init__(self: tk.Frame, parent: tk.Frame, controller: tk.Tk):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.FLASHCARD_CFG_PATH = "flashcard-config.cfg"
        self.CONFIG_OBJECT = configparser.ConfigParser()
        self.CONFIG_OBJECT.read(self.FLASHCARD_CFG_PATH)

        label = tk.Label(self, text="FlashcardFile")
        label.grid(row=0, column=0)

        self.selected_file_tkstring = tk.StringVar(self)

        self.flashcard_file_folder = self.CONFIG_OBJECT["Variables"]["flashcard-folder"]
        selected_flashcard_file_path = self.CONFIG_OBJECT["Variables"]["selected-flashcard-file"]
        self.selected_file_tkstring.set(selected_flashcard_file_path)

        flashcard_file_list = listdir(self.flashcard_file_folder)

        self.option_menu = tk.OptionMenu(
            self, self.selected_file_tkstring, *flashcard_file_list, command=self.on_new_flashcard_file_selected)
        self.option_menu.grid(row=0, column=1)

        button = tk.Button(self, text="Start Flashcards",
                           command=self.start_flash_cards)
        button.grid(row=1, column=0)

        edit_flashcards = tk.Button(
            self, text="Edit Selected", command=self.on_top_level_button_click)
        edit_flashcards.grid(row=2, column=0)

        new_flashcard_frame = tk.Frame(self)
        new_flashcard_file_button = tk.Button(
            new_flashcard_frame, text="Create New File", command=self.new_flashcard_file_button_clicked)
        self.new_flashcard_entry = tk.Entry(new_flashcard_frame)
        new_flashcard_file_button.pack(side=tk.RIGHT)
        self.new_flashcard_entry.pack(side=tk.LEFT)
        new_flashcard_frame.grid(row=3, column=0)

    def new_flashcard_file_button_clicked(self):
        filename = join(self.flashcard_file_folder,
                        self.new_flashcard_entry.get() + ".flashcards")
        current_files = listdir(self.flashcard_file_folder)
        if filename in current_files:
            self.set_entry_text(self.new_flashcard_entry,
                                "FILE ALREADY EXISTS!!!")
            return
        with open(filename, 'w+') as f:
            f.write(",,0")
        self.set_entry_text(self.new_flashcard_entry, "Creation Successful!")

        # Bit hacky, but it works
        self.controller.show_frame("HomePage")

        # Refreshing option menu
        # Currently this breaks the stringvar, needing a program reset before editing files
        # self.option_menu["menu"].delete(0, 'end')
        # for choice in listdir(self.flashcard_file_folder):
        #     self.option_menu["menu"].add_command(
        #         label=choice, command=tk._setit(self.selected_file_tkstring, choice))

    def set_entry_text(self, entry_object, new_text):
        entry_object.delete(0, tk.END)
        entry_object.insert(0, new_text)

    def start_flash_cards(self):
        self.controller.show_frame("FlashcardPage")

    def on_new_flashcard_file_selected(self, _):
        new_flashcard_file_name = self.selected_file_tkstring.get()

        self.CONFIG_OBJECT["Variables"]["selected-flashcard-file"] = new_flashcard_file_name

        with open(self.FLASHCARD_CFG_PATH, "w") as f:
            self.CONFIG_OBJECT.write(f)

    def on_top_level_button_click(self):
        # Atm this is a floating top window - link to current window
        FlashcardViewer()
