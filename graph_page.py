import tkinter as tk
import csv
import configparser

FLASHCARD_CFG_PATH = "flashcard-config.cfg"
CONFIG_OBJECT = configparser.ConfigParser()
CONFIG_OBJECT.read(FLASHCARD_CFG_PATH)


class GraphPage(tk.Frame):

    # Long __init__. Needs refactor?
    def __init__(self, parent: tk.Frame, controller: tk.Tk):
        tk.Frame.__init__(self, parent)

        self.controller = controller
