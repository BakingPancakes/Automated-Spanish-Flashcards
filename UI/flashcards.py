import json
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Spanish Flashcards")
root.geometry('510x350')

home_window = tk.Frame(root,width=510,height=325)
home_window.grid(row=0, column=0, sticky="nsew")
entry_frame = tk.Frame(root,width=519,height=100)
entry_frame.grid(row=1, column=1, sticky="nsew")

all_words_window = tk.Frame(root,width=510,height=350)

word_definition_window = tk.Frame(root,width=510,height=350)

def exit_window():
    root.destroy()

def display_frame(frame):
    frame.tkraise()

def view_all_words():
    with open('UI\wordbank.json') as f:
        data = json.load(f)
    populate_treeview(tree,data)
    all_words_window.grid(row=0, column=0, sticky="nsew")
    home_window.grid_forget()
    entry_frame.grid_forget()

def populate_treeview(tree,data):
    # Remove existing data
    for item in tree.get_children():
        tree.delete(item)

    # Populate the Treeview with word data
    for i in range(len(data['words'])):
        tree.insert("", "end", values=(data["words"][i], data["meaning"][i]))

def view_home():
    home_window.grid(row=0, column=0, sticky="nsew")
    word_definition_window.grid_forget()
    all_words_window.grid_forget()

def add_new_words():
    word_entry.grid(row=1, column=1, pady=10)

def on_entry_click(event):
    if word_entry.get() == "Enter new word here...":
        word_entry.delete(0, tk.END)
        word_entry.config(fg='black')

def query_random_word():
    word_definition_window.grid(row=0,column=0,sticky='nsew')
    home_window.grid_forget()

def display_previous_word():
    pass

def display_next_word():
    pass


### Home Window Widgets ###

title = tk.Label(
    home_window,
    text = 'Spanish Flashcards', font=('Arial',24)
)
title.pack(anchor='w',padx=10)

# exit_button = tk.Button(
#     home_window,
#     text="Exit", bg='red', fg='white',
#     command=exit_window
#     )
# exit_button.pack(side=tk.RIGHT)

welcome_label = tk.Label(
    home_window,
    text="Welcome :)\nClick your selection below to get started", font=('Arial',20),bg='#2C88D9',fg='white'
)
welcome_label.pack(pady=5,padx=10)

view_all_words_button = tk.Button(
    home_window,
    text="View All Words", bg='#2C88D9', fg='white', font=('Helvetica',12),
    command=view_all_words,
    width=15,
    height=2
    )
view_all_words_button.pack(side=tk.LEFT, padx=(10, 5), pady=50)

add_new_words_button = tk.Button(
    home_window,
    text="Add New Words", bg = '#2C88D9', fg='white', font=('Helvetica',12),
    command=add_new_words,
    width=15,
    height=2
)
add_new_words_button.pack(side=tk.LEFT, padx=(22), pady=50)

study_random_word_button = tk.Button(
    home_window,
    text="Study Random Word", bg='#2C88D9',fg='white', font=('Helvetica',12),
    command=query_random_word,
    width=15,
    height = 2
    )
study_random_word_button.pack(side=tk.RIGHT, padx=(5, 10), pady=50)

#! this doesn't work yet
word_entry = tk.Entry(
    entry_frame, width=20
)
word_entry.insert(0, "Enter new word here...")
word_entry.bind('<FocusIn>', on_entry_click)

word_entry_log = tk.Label()


### All Words Widgets ###

all_words_title = tk.Label(
    all_words_window,
    text='All Words',
    font=('Arial',20)
)
all_words_title.pack()

all_words_instructions_prompt = tk.Label(
    all_words_window,
    text='Automated Spanish Flashcards comes with several words to study\nby default. Feel free to study with this selection or add more.',
    font=('Arial',13),bg='#2C88D9',fg='white'
)
all_words_instructions_prompt.pack(pady=3,padx=10)

columns = ('Words','Meaning')
tree = ttk.Treeview(all_words_window,columns=columns,show='headings')

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(expand=tk.YES, fill=tk.BOTH)

back_to_home_button = tk.Button(
    all_words_window,
    text = 'Back To Home', font=('Helvetica',10), bg='#2C88D9',fg='white',
    command=view_home,
    width=20,
    height = 3
)
back_to_home_button.pack()


### Word Definition ###

definition_placeholder = tk.Label(
    word_definition_window,
    text='definition goes here',
    width=100,
    height=10
)
definition_placeholder.pack()

previous_word_button = tk.Button(
    word_definition_window,
    text="Previous Word", font=('Helvetica',10), bg='#2C88D9',fg='white',
    command=display_previous_word,
    width=20,
    height = 3
)
previous_word_button.pack(side=tk.LEFT, padx=(10, 5), pady=50)

back_to_home_button = tk.Button(
    word_definition_window,
    text = 'Back To Home', font=('Helvetica',10), bg='#2C88D9',fg='white',
    command=view_home,
    width=20,
    height = 3
)
back_to_home_button.pack(side=tk.LEFT, padx=5, pady=50)

query_another_word = tk.Button(
    word_definition_window,
    text='Query Another Word', font=('Helvetica',10), bg='#2C88D9',fg='white',
    command=display_next_word,
    width=20,
    height = 3
)
query_another_word.pack(side=tk.LEFT, padx=(5, 10), pady=50)

display_frame(home_window)

root.mainloop()