import tkinter as tk
import csv
import configparser
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from os.path import isfile, join
from utils import get_words_and_scores_from_csv


class GraphPage(tk.Frame):

    def __init__(self, parent: tk.Frame, controller: tk.Tk):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.FLASHCARD_CFG_PATH = "flashcard-config.cfg"
        self.CONFIG_OBJECT = configparser.ConfigParser()
        self.CONFIG_OBJECT.read(self.FLASHCARD_CFG_PATH)

        self.fig, self.ax = plt.subplots()

        selected_folder = self.CONFIG_OBJECT["Variables"]["flashcard-folder"]
        selected_csv_name = self.CONFIG_OBJECT["Variables"]["selected-flashcard-file"]

        selected_csv = join(selected_folder, selected_csv_name)

        score_data = [int(scores) for word, trans,
                      scores in get_words_and_scores_from_csv(selected_csv)]

        x_max = float(
            self.CONFIG_OBJECT["FlashCard-Preferences"]["upper_score_limit"])
        x_min = float(
            self.CONFIG_OBJECT["FlashCard-Preferences"]["lower_score_limit"])

        selected_flashcard_set = self.CONFIG_OBJECT["Variables"]["selected-flashcard-file"].split(".")[
            0]

        controller.title("Histogram - Progress for " + selected_flashcard_set)

        self.ax.hist(score_data, range=(x_min, x_max),
                     align="mid", facecolor="grey", rwidth=0.9)
        self.ax.set_xticks([i for i in range(int(x_min), int(x_max)+1)])
        self.ax.yaxis.get_major_locator().set_params(integer=True)
        self.fig.set_size_inches(8, 3.7)
        self.ax.set_xlabel("Score", size=12)
        self.ax.set_ylabel("Frequency", size=12)

        canvas = FigureCanvasTkAgg(self.fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0)

        exit_button = tk.Button(self, text="Return Home",
                                command=self.on_return_home_clicked)

        exit_button.grid(row=1, column=0)

        self.bind("<Escape>", self.kill_program)
        self.focus_set()  # Focuses current frame so that it can take keypresses

    def on_return_home_clicked(self):
        self.controller.show_frame("HomePage")

    def kill_program(self, *_):
        # Could move this into controller to avoid repeated code
        print("Ending Program...")

        self.controller.destroy()
        quit()
