import tkinter as tk
# from tkinter import ttk
from flashcard_page import FlashcardPage
from graph_page import GraphPage


class tkinterUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Set as class variable so frames can access.
        tkinterUI.width, tkinterUI.height = 800, 400

        self.geometry(f"{self.width}x{self.height}")

        frame_container = tk.Frame(self)
        frame_container.pack(side="top", fill="both", expand=True)
        frame_container.grid_rowconfigure(0, weight=1)
        frame_container.grid_columnconfigure(0, weight=1)

        self.frame_dict = {}

        # All frames are rendered at all times, just 'focused' as needed.
        # Definitely not the best way to do this, just a prototype.
        for FRAME in [FlashcardPage, GraphPage]:
            _frame = FRAME(frame_container, self)

            self.frame_dict[FRAME] = _frame
            _frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(GraphPage)

    def show_frame(self, frame_name):

        frame = self.frame_dict[frame_name]
        frame.tkraise()


if __name__ == "__main__":
    app = tkinterUI()
    app.mainloop()
