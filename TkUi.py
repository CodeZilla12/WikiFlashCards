import tkinter as tk
#from tkinter import ttk
from functools import partial
import csv

FONTSIZE = 30
FONT = ("Helvetica", FONTSIZE)


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

#Each page class should have its own file probably
class FlashcardPage(tk.Frame):
    def __init__(self, parent: tk.Frame, controller: tk.Tk):
        tk.Frame.__init__(self, parent)

        WORD_CSV_PATH = "word_scores.csv"
        self.word_pair_list = self.get_words_and_scores_from_csv(WORD_CSV_PATH)
        self.word_index = 0
        self.waiting_for_answer = False
        self.word_list_complete = False

        #Initialising Initial display widgets
        self.displayed_word = tk.Label(
            self,text = self.word_pair_list[self.word_index][0] ,font=FONT)
        self.displayed_word.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        self.show_word_button = tk.Button(
            self, text="Show Word (space)", command=self.show_word_button_clicked)
        self.show_word_button.pack(side=tk.BOTTOM, pady=20)


        #Initialising answering widgets
        self.button_frame = tk.Frame()

        self.easy_button = tk.Button(self.button_frame, text = "Easy (v)", command = partial(self.answer_button_clicked, "easy")) #Instead of generating these every time - have them show and hide accordingly
        self.hard_button = tk.Button(self.button_frame, text = "Hard (x)", command = partial(self.answer_button_clicked, "hard"))
        self.okay_button = tk.Button(self.button_frame, text = "Okay (c)", command = partial(self.answer_button_clicked, "okay"))
        self.fail_button = tk.Button(self.button_frame, text = "Fail (z)", command = partial(self.answer_button_clicked, "fail"))
        
        #Packs buttons into button_frame side-by-side
        self.fail_button.grid(row=0,column=0)
        self.hard_button.grid(row=0,column=1)
        self.okay_button.grid(row=0,column=2)
        self.easy_button.grid(row=0,column=3)


        #Initialising Hotkeys
        self.bind("<space>", self.show_word_button_clicked)
        self.bind("z", partial(self.answer_button_clicked, "fail"))
        self.bind("x", partial(self.answer_button_clicked, "hard"))
        self.bind("c", partial(self.answer_button_clicked, "okay"))
        self.bind("v", partial(self.answer_button_clicked, "easy"))
        self.focus_set()    #Focuses current frame so that it can take keypresses
    
    @staticmethod
    def get_words_and_scores_from_csv(file_path:str):

        #Items are stored in the csv as:
        #word,score[/n]word,score[\n]....
        word_list = []
        with open(file_path,'r',encoding="utf8") as f:
            csv_reader = csv.reader(f,delimiter=",")
            for row in csv_reader:

                if len(row) == 2:
                    row.append(0)
                    
                word,translated_word,score = row
                word_list.append( (word,translated_word,score) )
        
        return word_list

            


    def display_next_word(self):
        self.word_index += 1

        if self.word_index >= len( self.word_pair_list ):
            self.word_list_complete = True
            self.displayed_word.config(text= "Complete")
            self.show_word_button.pack_forget()
            return
        
        self.displayed_word.config(text = self.word_pair_list[self.word_index][0])

    def show_word_button_clicked(self, *_):

        #*_ is to capture keyboard event input.

        #In case of function called from hotkey
        if self.waiting_for_answer or self.word_list_complete:
            return

        self.waiting_for_answer = True
        self.displayed_word.configure(
            text=self.word_pair_list[self.word_index][1])
        self.show_word_button.pack_forget()

        self.button_frame.pack(side = tk.BOTTOM, pady="10px")

    def answer_button_clicked(self,answer:str, *_):

        #*_ is to capture keyboard event input.

        #In case of function called from hotkey
        if not self.waiting_for_answer or self.word_list_complete:
            return

        self.button_frame.pack_forget()
        self.show_word_button.pack(side=tk.BOTTOM, pady=20)
        self.display_next_word()
        self.waiting_for_answer = False




if __name__ == "__main__":
    app = tkinterUI()
    app.mainloop()
