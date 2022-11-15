# ---------------------------- CONSTANTS ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Arial"
current_word = {}
reps = 0
finalcheckmark = ""
timer = None

from tkinter import *
import pandas
import random
import os

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
cardfront_img = PhotoImage(file="images/card_front.png")
cardback_img = PhotoImage(file="images/card_back.png")
img = canvas.create_image(400, 263, image=cardfront_img)
lang1_text = canvas.create_text(400,150, text="French", fill="black", font=(FONT_NAME, 40, 'italic'))
lang2_text = canvas.create_text(400,263, text="trouve", fill="black", font=(FONT_NAME, 60, 'bold'))
canvas.grid(column=1, row=1, columnspan=2)
right_img = PhotoImage(file="images/right.png")
wrong_img = PhotoImage(file="images/wrong.png")

currdir = os.getcwd()
path = currdir + "\data\words_to_learn.csv"
isdir = os.path.exists(path)
if isdir:
    french_data = pandas.read_csv("data/words_to_learn.csv")
else:
    french_data = pandas.read_csv("data/french_words.csv")

french_dict = french_data.to_dict(orient='records')

def count_down(count, pos):
    global timer, reps, checkmark, finalcheckmark
    if count > 0:
        timer = window.after(1000, count_down, count - 1, pos)
        # canvas.itemconfig(timer_text, text=finaltext)
        print(count)
    else:
        canvas.itemconfig(img, image=cardback_img)
        canvas.itemconfig(lang1_text, text="English", fill="white")
        canvas.itemconfig(lang2_text, text=french_dict[pos]["English"], fill="white")
        window.after_cancel(timer)

def generate_word():
    global current_word
    canvas.itemconfig(img, image=cardfront_img)
    res = random.randint(0, len(french_dict) - 1)
    current_word = french_dict[res]
    canvas.itemconfig(lang1_text, text="French", fill="black")
    canvas.itemconfig(lang2_text, text=french_dict[res]["French"], fill="black")
    count_down(3, res)

generate_word()
# print(french_dict[random.randint(0, i1 - 1)])


# ---------------------------- TIMER MECHANISM ------------------------------- #
def wrong_clicked():
    generate_word()

dictlist = []

def ok_clicked():
    french_dict.remove(current_word)
    pandas.DataFrame(french_dict).to_csv("data\words_to_learn.csv", index=0)
    generate_word()

wrong_button = Button(image=wrong_img, highlightthickness=0, command=wrong_clicked, padx=50, pady=50)
wrong_button.grid(column=1,row=2)

ok_button = Button(image=right_img, highlightthickness=0, command=ok_clicked, padx=50, pady=50)
ok_button.grid(column=2,row=2)

window.mainloop()
