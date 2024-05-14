import tkinter as tk


class HomePage(tk.Frame):

    def __init__(self: tk.Frame, parent: tk.Frame, controller: tk.Tk):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        label = tk.Label(self, text="FlashcardFile")
        label.grid(row=0, column=0)
        variable = tk.StringVar(self)
        option_menu = tk.OptionMenu(self, variable, "One", "Two", "Three")
        option_menu.grid(row=0, column=1)

        button = tk.Button(self, text="Start Flashcards",
                           command=self.start_flash_cards)
        button.grid(row=1, column=0)

    def start_flash_cards(self):

        self.controller.show_frame("FlashcardPage")
