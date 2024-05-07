import tkinter as tk

FONTSIZE = 20
FONT = ("Verdana", FONTSIZE)


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
        for FRAME in [FlashcardPage]:
            _frame = FRAME(frame_container, self)

            self.frame_dict[FRAME] = _frame
            _frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(FlashcardPage)

    def show_frame(self, frame_name):

        frame = self.frame_dict[frame_name]
        frame.tkraise()


class FlashcardPage(tk.Frame):
    def __init__(self, parent: tk.Frame, controller: tk.Tk):
        tk.Frame.__init__(self, parent)

        self.word_pair_list = [
            ("Vienas", "One"), ("Du", "Two"), ("Trys", "Three")]
        self.word_index = 0

        self.displayed_word = tk.Label(
            self, text=self.word_pair_list[0][0], font=FONT)
        # Displays text in center of top row
        self.displayed_word.place(relx=0.5, y=0+FONTSIZE, anchor=tk.CENTER)

        self.show_word_button = tk.Button(
            self, text="Show Word", command=self.show_word_button_clicked)
        self.show_word_button.pack(side=tk.BOTTOM, pady=20)

    def show_word_button_clicked(self):
        self.displayed_word.configure(
            text=self.word_pair_list[self.word_index][1])
        self.show_word_button.destroy()


if __name__ == "__main__":
    app = tkinterUI()
    app.mainloop()
