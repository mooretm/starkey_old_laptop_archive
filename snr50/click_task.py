from tkinter import *
from tkinter import ttk
import numpy as np

root = Tk()
frame = Frame(root)
frame.grid(column=0, row=0, sticky=NSEW)
frame.option_add('*Font', '19')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

""" Clicking labels with color change
    Looks nice, but logic doesn't work
    
def prep(event):
    bkgd = event.widget['bg']
    #if event.widget.v() and event.widget.v() != 'A':
    if bkgd != 'light blue':
        event.widget.config(bg='light blue')
        event.widget.focus_set()  # give keyboard focus to the label
        event.widget.bind('<Key>', edit)
    else:
        event.widget.config(bg=root.cget('bg'))
        event.widget.focus_set()  # give keyboard focus to the label
        event.widget.bind('<Key>', edit)

def edit(event):
    print(event.char)

words = ['The', 'DOG', 'is', 'A', 'FAST', 'one']

#v = StringVar()
for index, word in enumerate(words):
    example = Label(frame, text=word)
    example.grid(column=index,row=0)
    example.bind('<Button-1>', prep)

ttk.Separator(frame,orient='horizontal').grid(columnspan=12,row=2,sticky=EW)
"""

import tkinter.font as tkFont
theFont = tkFont.nametofont('TkDefaultFont')

words = ['The', 'DOG', 'is', 'A', 'FAST', 'one']
vals = np.zeros(len(words),dtype=int)
chkbox_dict = dict(zip(words,vals))

for counter, key in enumerate(chkbox_dict):
    chkbox_dict[key] = IntVar()
    if key.isupper() and key != 'A':
        aCheckButton = ttk.Checkbutton(frame,text='',takefocus=0,variable=chkbox_dict[key])
        aCheckButton.grid(column=counter,row=4)
        new = str(theFont) + ' 19 underline'
        theWords = ttk.Label(frame,text=words[counter],font=new).grid(column=counter,row=3)
    else:
        aCheckButton = ttk.Checkbutton(frame,text='',takefocus=0,variable=chkbox_dict[key])
        #aCheckButton.grid(column=counter,row=4) # Do not display these checkboxes
        theWords = ttk.Label(frame,text=words[counter]).grid(column=counter,row=3)

def score():
    for key, value in chkbox_dict.items():
        state = value.get()
        if state != 0:
            print('Correct! ' + key)
            chkbox_dict[key].set(0)
        else:
            if key.isupper() and key != 'A':
                print('Wrong! ' + key)
                chkbox_dict[key].set(0)

button = ttk.Button(frame,text="Submit",command=score).grid(column=len(chkbox_dict)+1, row=4)


mainloop()
