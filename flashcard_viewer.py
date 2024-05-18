import tkinter as tk
from utils import get_words_and_scores_from_csv, write_scores_to_csv


class FlashCardViewer(tk.Toplevel):
    def __init__(self):

        tk.Toplevel.__init__(self)

        self.geometry("600x200")
        self.title("Flashcard Viewer")

        # Iterate through each entry in selected config.

        e1 = tk.Entry(self, width=600)
        e2 = tk.Entry(self, width=600)

        e1.grid(row=0, column=0)
        e2.grid(row=1, column=0)

        next_button = tk.Button(text="->", command=self.on_next_button_clicked)

        previous_button = tk.Button(
            text="<-", command=self.on_previous_button_clicked)

        self.mainloop()

    def on_next_button_clicked(self):
        pass

    def on_previous_button_clicked(self):
        pass
