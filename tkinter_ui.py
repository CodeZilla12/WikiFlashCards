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

        self.frame_container = tk.Frame(self)
        self.frame_container.pack(side="top", fill="both", expand=True)
        self.frame_container.grid_rowconfigure(0, weight=1)
        self.frame_container.grid_columnconfigure(0, weight=1)

        self.frame_dict = {
            "FlashcardPage": FlashcardPage, "GraphPage": GraphPage}
        self.show_frame("FlashcardPage")

    def show_frame(self, frame_name):
        self.clear_frame(self.frame_container)

        frame = self.frame_dict[frame_name](self.frame_container, self)
        frame.grid(sticky="nsew")

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = tkinterUI()
    app.mainloop()
