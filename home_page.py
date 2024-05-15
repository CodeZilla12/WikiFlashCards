import tkinter as tk
import configparser
from os.path import join
from os import listdir


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

        flashcard_file_folder = self.CONFIG_OBJECT["Variables"]["flashcard-folder"]
        selected_flashcard_file_path = self.CONFIG_OBJECT["Variables"]["selected-flashcard-file"]
        self.selected_file_tkstring.set(selected_flashcard_file_path)

        flashcard_file_list = listdir(flashcard_file_folder)

        option_menu = tk.OptionMenu(
            self, self.selected_file_tkstring, *flashcard_file_list, command=self.on_new_flashcard_file_selected)
        option_menu.grid(row=0, column=1)

        button = tk.Button(self, text="Start Flashcards",
                           command=self.start_flash_cards)
        button.grid(row=1, column=0)

        top_level_button = tk.Button(
            self, text="Open Toplevel", command=self.on_top_level_button_click)
        top_level_button.grid(row=2, column=0)

    def start_flash_cards(self):

        self.controller.show_frame("FlashcardPage")

    def on_new_flashcard_file_selected(self, _):
        new_flashcard_file_name = self.selected_file_tkstring.get()

        self.CONFIG_OBJECT["Variables"]["selected-flashcard-file"] = new_flashcard_file_name

        with open(self.FLASHCARD_CFG_PATH, "w") as f:
            self.CONFIG_OBJECT.write(f)

    def on_top_level_button_click(self):
        FlashCardViewer()


class FlashCardViewer(tk.Toplevel):
    def __init__(self):

        tk.Toplevel.__init__(self)

        self.geometry("600x200")
        self.title("Flashcard Viewer")

        self.mainloop()
