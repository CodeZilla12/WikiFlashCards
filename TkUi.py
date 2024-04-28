import tkinter as tk
from tkinter import ttk

FONT = ("Verdana", 35)


class tkinterUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        frame_container = tk.Frame(self)
        frame_container.pack(side="top", fill="both", expand=True)
        frame_container.grid_rowconfigure(0, weight=1)
        frame_container.grid_columnconfigure(0, weight=1)

        self.frame_dict = {}

        # All frames are rendered at all times, just 'focused' as needed.
        for FRAME in [StartPage]:
            _frame = FRAME(frame_container, self)

            self.frame_dict[FRAME] = _frame
            _frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, frame_name):

        frame = self.frame_dict[frame_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent: tk.Frame, controller: tk.Tk):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Start Page", font=FONT)

        label.grid(row=0, column=4, padx=10, pady=10)


if __name__ == "__main__":
    app = tkinterUI()
    app.mainloop()
