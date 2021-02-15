from tkinter import *
from PIL import ImageTk, Image
import string
import random
from functools import partial

#creating window
window = Tk()
window.title('Hangman Game')
window.state('zoomed')

#variables
words = open('words.txt', 'r')
words = words.read().split(';')
print(words)
word = random.choice(words)
move = 0
letters = list(string.ascii_lowercase)
btn = []

#functions
def guesses_create():
  for i in range(len(guesses)):
    guesses[i].destroy()
  guesses.clear()
  for i in range(len(word)):
    new = Label(guessing_frame, text='', font=("Courier", 15), padx=13, pady=12, borderwidth=4, relief="ridge", highlightbackground='black')
    guesses.append(new)
    guesses[i].grid(row=0, column=i, padx=5, pady=2)

def again_click(img, target):
  target.destroy()
  global move
  move=0
  image = ImageTk.PhotoImage(Image.open('hangman0.png'))
  img.configure(image=image, borderwidth=0)
  img.image = image
  for i in range(len(btn)):
    btn[i]["state"] = NORMAL
  global word
  word = random.choice(words)
  guesses_create()
  return None

def btn_click(n, img):
  letter = btn[n]['text']
  btn[n].configure('state')
  btn[n]["state"] = DISABLED
  #adding letter to guessing fields
  if letter in word:
    goals = []
    for i in range(len(word)):
      if letter == word[i]:
        goals.append(i)
    for i in range(len(goals)):
      guesses[goals[i]]['text'] = letter
  #changing image if wrong letter
  else:
    global move
    if move >= 12:
      score_frame = LabelFrame(window)
      score_frame.pack()
      again_btn = Button(score_frame, text='Play again.', font=("Courier", 15), command=partial(again_click, img, score_frame))
      again_btn.grid(row=0, column=0)
      win_label = Label(score_frame, text='You lost!', font=("Courier", 30), padx=5)
      win_label.grid(row=0, column=1)
      exit_btn = Button(score_frame, text='Exit game.', font=("Courier", 15), command=exit)
      exit_btn.grid(row=0, column=2)
      return None
    else:
      move += 1
      key = 'hangman' + str(move) + '.png'
      image = ImageTk.PhotoImage(Image.open(key))
      img.configure(image=image, borderwidth=0)
      img.image = image
      return None
  #chekcing if word is complete
  guess = ''
  for i in range(len(guesses)):
    guess += guesses[i]['text']
  if guess == word:
    score_frame = LabelFrame(window)
    score_frame.pack(pady=5)
    again_btn = Button(score_frame, text='Play again.', font=("Courier", 15), command=partial(again_click, img, score_frame))
    again_btn.grid(row=0, column=0)
    win_label = Label(score_frame, text='You won!', font=("Courier", 30), padx=5)
    win_label.grid(row=0, column=1)
    exit_btn = Button(score_frame, text='Exit game.', font=("Courier", 15), command=exit)
    exit_btn.grid(row=0, column=3)

#title
title = Label(window, text='The Hangman', font=('Comic Sans MS', 40, "bold"))
title.pack()

#image frame
image_frame = LabelFrame(window, borderwidth=0)
image_frame.pack()
image = ImageTk.PhotoImage(Image.open('hangman0.png'))
image_label =Label(image_frame, image=image, borderwidth=0)
image_label.pack()

#guesses frame
guesses = []
guessing_frame = LabelFrame(window, borderwidth=0)
guessing_frame.pack()
#creating letter fields
guesses_create()

#letters frame
letter_frame = LabelFrame(window, borderwidth=0)
letter_frame.pack()
#creating buttons
for x in range(len(letters)):
  new = Button(letter_frame, text=letters[x], command=partial(btn_click, x, image_label), font=("Courier", 18), padx=4, pady=5)
  btn.append(new)
  if x < len(letters)/2:
    row = 0
    cl = 0
  else:
    row = 1
    cl = 13
  btn[x].grid(row = row, column = (x-cl), padx=2, pady=2)

window.mainloop()
