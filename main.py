import tkinter
import pandas
import random
from tkinter import messagebox

BACKGROUND_COLOR = "#B1DDC6"
TITLE_FONT = "Arial 40 italic"
WORD_FONT = ("Arial", 60, "bold")
HOW_LONG_TO_WAIT = 3000


def get_words():
    global words, ind
    try:
        words = pandas.read_csv("./data/words_to_learn.csv")
    except FileNotFoundError:
        words = pandas.read_csv("./data/french_words.csv")
        words.to_csv("./data/words_to_learn.csv")
    else:
        if len(words) == 0:
            words = pandas.read_csv("./data/french_words.csv")
    ind = 0


def show_random_word():
    global ind, waiting, words
    window.after_cancel(waiting)
    if len(words) > 0:
        ind = random.randint(0, len(words)-1)
        fr_word = words["French"][ind]
        canvas.itemconfig(card_image, image=image_card_front)
        canvas.itemconfigure(card_word, text=fr_word, fill="black")
        canvas.itemconfig(card_title, text="French", fill="black")
        waiting = window.after(ms=1000, func=flip_the_card)
    else:
        messagebox.showinfo(message="All words learned")


def flip_the_card():
    global ind, words
    en_word = words["English"][ind]
    canvas.itemconfig(card_image, image=image_card_back)
    canvas.itemconfigure(card_word, text=en_word, fill="white")
    canvas.itemconfig(card_title, text="English", fill="white")


def answer_wrong():
    global words
    show_random_word()


def answer_right():
    global words
    update_words_to_learn()
    show_random_word()


def update_words_to_learn():
    global ind, words
    if len(words) > 0:
        words.drop(index=ind, inplace=True)
        words.reset_index(drop=True, inplace=True)
        words.to_csv("./data/words_to_learn.csv")


# ---------------------------- UI SETUP ------------------------------- #


window = tkinter.Tk()
window.title("Flashcards")
window.config(padx=30, pady=30, bg=BACKGROUND_COLOR)

waiting = window.after(ms=HOW_LONG_TO_WAIT, func=flip_the_card)

image_card_back = tkinter.PhotoImage(file="./images/card_back.png")
image_card_front = tkinter.PhotoImage(file="./images/card_front.png")
image_right = tkinter.PhotoImage(file="./images/right.png")
image_wrong = tkinter.PhotoImage(file="./images/wrong.png")

canvas = tkinter.Canvas(width=800, height=550, bg=BACKGROUND_COLOR, highlightthickness=0)
card_image = canvas.create_image(400, 250, image=image_card_front)
canvas.grid(column=0, row=0, columnspan=2)
card_title = canvas.create_text(400, 150, text="Title", font=TITLE_FONT)
card_word = canvas.create_text(400, 250, text="Word", font=WORD_FONT)


# buttons
button_wrong = tkinter.Button(image=image_wrong, command=answer_wrong, highlightthickness=0)
button_wrong.grid(column=0, row=1)

button_right = tkinter.Button(image=image_right, command=answer_right, highlightthickness=0)
button_right.grid(column=1, row=1)

get_words()
show_random_word()


window.mainloop()

