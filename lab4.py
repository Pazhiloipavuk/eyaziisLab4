
import nltk
from pathlib import Path
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import filedialog
from nltk import *
from nltk.corpus import stopwords
from string import punctuation
import tkinter as tk
import pyodbc
import requests

connect_data = 'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + os.path.dirname(os.path.abspath( __file__ )) + 'PEREV.mdb;'
conn = pyodbc.connect(connect_data)
cursor = conn.cursor()
cursor.execute('select * from Dict')
db_tuples = list()
for row in cursor.fetchall():
    db_tuples.append(row[1:3])

grammar = """
            NP: {<DT|JJ|NN.*>+}             # Chunk sequences of DT, JJ, NN
            PP: {<IN><NP>}                  # Chunk prepositions followed by NP
            VP: {<VB.*><NP|PP|CLAUSE>+$}    # Chunk verbs and their arguments
            CLAUSE: {<NP><VP>}              # Chunk NP, VP
          """
regexpParser = nltk.RegexpParser(grammar, loop=100)

doc_name = ""
text = ""
translated_text = ""
lang = "en|ru"

root=Tk()
space0 = Label(root,text='\n')
aboutButton = Button(root,text='About',width=8,height=2,bg='light grey')
space1 = Label(root,text='\n')
chooseDocButton=Button(root,text='Choose doc',width=55,height=2,bg='light grey')
space11 = Label(root,text='\nSelect language\n')
enButton=Button(root,text='English',width=55,height=2,bg='light grey')
ruButton=Button(root,text='Russian',width=55,height=2,bg='light grey')
space2 = Label(root,text='\n')
resultText = tk.Text(root, state='disabled', width=80, height=20)
space3 = Label(root,text='\n')
translateButton=Button(root,text='Translate from Mymemory and PEREV.mdb',width=55,height=2,bg='light grey')
space4 = Label(root,text='\nEnter sentence:\n')
sentenceText = tk.Text(root, width=80, height=2)
treeButton=Button(root,text='Generate tree',width=55,height=2,bg='light grey')
space5 = Label(root,text='\n')
saveButton=Button(root,text='Save',width=55,height=2,bg='light grey')
space6 = Label(root,text='\n')

def nameOf(path):
    return Path(path).stem

def chooseDocsClicked():
    global doc_name, text
    files = filedialog.askopenfilename(multiple=False)
    splitlist = root.tk.splitlist(files)
    for doc in splitlist:
        doc_name = nameOf(doc)
        text = Path(doc, encoding="UTF-8", errors='ignore').read_text(encoding="UTF-8", errors='ignore')
    resultText.configure(state='normal')
    resultText.delete('1.0', END)
    resultText.insert('end', text)
    resultText.configure(state='disabled')

def enClicked():
    global lang
    lang = "en|ru"

def ruClicked():
    global lang
    lang = "ru|en"

def translateClicked():
    global text, translated_text, db_tuples, lang
    translated_text = text
    for db_tuple in db_tuples:
        if db_tuple[0] != " ":
            translated_text = translated_text.replace(db_tuple[0], db_tuple[1])
    URL = "https://api.mymemory.translated.net/get"
    PARAMS = {'q':translated_text, 'langpair':lang} 
    r = requests.get(url = URL, params = PARAMS)
    translated_text = r.json()['responseData']['translatedText']
    resultText.configure(state='normal')
    resultText.delete('0.0', END)
    resultText.insert('end', translated_text)
    resultText.configure(state='disabled')

def treeClicked():
    tokens = nltk.word_tokenize(sentenceText.get('1.0', END))
    tokens_with_pos_tag = nltk.pos_tag(tokens)
    tree = regexpParser.parse(tokens_with_pos_tag)
    tree.draw()

def saveClicked():
    global doc_name, translated_text
    file = open(doc_name + '_translated.txt', 'w', encoding="utf8")
    file.write(translated_text)
    file.close()

def aboutButtonClicked():
    messagebox.showinfo("Lab 3", "Usage: Choose file. Then click \"Translate from Mymemory and PEREV.mdb\" button.\nYou can also create tree from sentence and save translate result.\n\nDeveloped by: Artyom Gurbovich and Pavel Kalenik.")

aboutButton.config(command=aboutButtonClicked)
chooseDocButton.config(command=chooseDocsClicked)
enButton.config(command=enClicked)
ruButton.config(command=ruClicked)
translateButton.config(command=translateClicked)
treeButton.config(command=treeClicked)
saveButton.config(command=saveClicked)

space0.pack()
aboutButton.pack()
space1.pack()
chooseDocButton.pack()
space11.pack()
enButton.pack()
ruButton.pack()
space2.pack()
resultText.pack()
space3.pack()
translateButton.pack()
space4.pack()
sentenceText.pack()
treeButton.pack()
space5.pack()
saveButton.pack()
space6.pack()
root.mainloop()