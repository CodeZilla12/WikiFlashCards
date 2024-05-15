import tkinter as tk
import csv
import configparser
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from os.path import isfile, join

FLASHCARD_CFG_PATH = "flashcard-config.cfg"
CONFIG_OBJECT = configparser.ConfigParser()
CONFIG_OBJECT.read(FLASHCARD_CFG_PATH)


class GraphPage(tk.Frame):

    def __init__(self, parent: tk.Frame, controller: tk.Tk):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.fig, self.ax = plt.subplots()

        selected_folder = CONFIG_OBJECT["Variables"]["flashcard-folder"]
        selected_csv_name = CONFIG_OBJECT["Variables"]["selected-flashcard-file"]

        selected_csv = join(selected_folder, selected_csv_name)

        score_data = [int(scores) for word, trans,
                      scores in self.get_words_and_scores_from_csv(selected_csv)]

        x_max = float(
            CONFIG_OBJECT["FlashCard-Preferences"]["upper_score_limit"])
        x_min = float(
            CONFIG_OBJECT["FlashCard-Preferences"]["lower_score_limit"])

        self.ax.set_title(
            "Histogram - Progress for Selected Set")

        self.ax.hist(score_data, range=(x_min, x_max),
                     align="mid", facecolor="grey", rwidth=0.9)
        self.ax.set_xticks([i for i in range(int(x_min), int(x_max)+1)])
        self.ax.yaxis.get_major_locator().set_params(integer=True)

        self.ax.set_xlabel("Score", size=12)
        self.ax.set_ylabel("Frequency", size=12)

        canvas = FigureCanvasTkAgg(self.fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()

        self.bind("<Escape>", self.kill_program)
        self.focus_set()  # Focuses current frame so that it can take keypresses

    def kill_program(self, *_):
        # Should move this into controller to reduce repeated code
        print("Ending Program...")

        self.controller.destroy()

    @ staticmethod
    def get_words_and_scores_from_csv(file_path: str) -> list:

        # This should be moved to an external utilities function as it will likely be used in many places.

        # Items are stored in the csv as:
        # word, trans, score[/n]word,trans,score[\n]....
        word_list = []

        if not isfile(file_path):
            raise FileNotFoundError("word_scores.csv missing")

        with open(file_path, 'r', encoding="utf8") as f:
            csv_reader = csv.reader(f, delimiter=",")
            for row in csv_reader:

                if len(row) == 0:
                    continue

                if len(row) == 2:  # Make this check more specific
                    row.append(0)

                word, translated_word, score = row
                word_list.append([word, translated_word, float(score)])

        return word_list
