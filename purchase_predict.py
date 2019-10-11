import inline as inline
import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
#%matplotlib inline

bankdata = pd.read_csv("C:\\Users\\User\\Documents\\Book1.csv")
X = bankdata.drop(['Purchased','Gender'], axis=1)
y = bankdata['Purchased']
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)
from sklearn.svm import SVC
svclassifier = SVC(kernel='linear')
svclassifier.fit(X_train, y_train)
#y_pred = svclassifier.predict(X_test)
#from sklearn.metrics import classification_report, confusion_matrix
#print(confusion_matrix(y_test,y_pred))
#print(classification_report(y_test,y_pred))

# imports
from tkinter import *
from tkinter import messagebox as ms
import sqlite3

# make database and users (if not exists already) table at programme start up
with sqlite3.connect('quit.db') as db:
    c = db.cursor()

c.execute('CREATE TABLE IF NOT EXISTS user (username TEXT NOT NULL ,password TEX NOT NULL);')
db.commit()
db.close()


# main Class
class main:
    global p
    def __init__(self, master):
        # Window
        self.master = master
        # Some Usefull variables
        self.username = StringVar()
        self.password = StringVar()
        self.n_username = StringVar()
        self.n_password = StringVar()
        self.gender = StringVar()
        self.age = StringVar()
        self.salary = StringVar()
        # Create Widgets
        self.widgets()

    # Login Function
    def login(self):
        # Establish Connection
        with sqlite3.connect('quit.db') as db:
            c = db.cursor()

        # Find user If there is any take proper action
        find_user = ('SELECT * FROM user WHERE username = ? and password = ?')
        c.execute(find_user, [(self.username.get()), (self.password.get())])
        result = c.fetchall()
        if result:
            self.logf.pack_forget()
            # self.head['text'] = self.username.get() + '\n Loged In'
            self.head = Label(self.master, text='Details', font=('', 35), pady=10)
            self.head.pack()
            self.detf = Frame(self.master, padx=10, pady=10)
            Label(self.detf, text='Gender: ', font=('', 20), pady=5, padx=5).grid(sticky=W)
            Entry(self.detf, textvariable=self.gender, bd=5, font=('', 15)).grid(row=0, column=1)
            Label(self.detf, text='Age: ', font=('', 20), pady=5, padx=5).grid(sticky=W)
            Entry(self.detf, textvariable=self.age, bd=5, font=('', 15)).grid(row=1, column=1)
            Label(self.detf, text='Salary: ', font=('', 20), pady=5, padx=5).grid(sticky=W)
            Entry(self.detf, textvariable=self.salary, bd=5, font=('', 15)).grid(row=2, column=1)
            Button(self.detf, text=' Submit ', bd=3, font=('', 15), padx=5, pady=5, command=self.algo).grid()
            # Button(self.detf,text = ' Create Account ',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.cr).grid(row=2,column=1)
            self.detf.pack()
        else:
            ms.showerror('Oops!', 'Username Not Found.')

    def new_user(self):
        # Establish Connection
        with sqlite3.connect('quit.db') as db:
            c = db.cursor()

        # Find Existing username if any take proper action
        find_user = ('SELECT * FROM user WHERE username = ?')
        c.execute(find_user, [(self.username.get())])
        if c.fetchall():
            ms.showerror('Error!', 'Username Taken Try a Diffrent One.')
        else:
            ms.showinfo('Success!', 'Account Created!')
            self.log()
        # Create New Account
        insert = 'INSERT INTO user(username,password) VALUES(?,?)'
        c.execute(insert, [(self.n_username.get()), (self.n_password.get())])
        db.commit()

        # Frame Packing Methords

    def log(self):
        self.username.set('')
        self.password.set('')
        self.crf.pack_forget()
        self.head['text'] = 'LOGIN'
        self.logf.pack()

    def cr(self):
        self.n_username.set('')
        self.n_password.set('')
        self.logf.pack_forget()
        self.head['text'] = 'Create Account'
        self.crf.pack()

    def algo(self):
        a = self.age.get()
        b = self.salary.get()
        c = svclassifier.predict([[a, b]])
        if (c==0):
            p = "Not purchased"
        else:
            p = "purchased"
        self.detf.pack_forget()
        #self.head['text'] = 'Result'
        #self.result.pack()
        Label(self.head, text=p, font=('', 20), pady=5, padx=5).grid(sticky=W)
        self.head.pack()


    # Draw Widgets
    def widgets(self):
        self.head = Label(self.master, text='WELCOME', font=('', 35), pady=10)
        self.head.pack()
        self.logf = Frame(self.master, padx=10, pady=10)
        self.head = Label(self.logf, text='Login', font=('', 35), pady=10)
        Label(self.logf, text='Username: ', font=('', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.logf, textvariable=self.username, bd=5, font=('', 15)).grid(row=0, column=1)
        Label(self.logf, text='Password: ', font=('', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.logf, textvariable=self.password, bd=5, font=('', 15), show='*').grid(row=1, column=1)
        Button(self.logf, text=' Login ', bd=3, font=('', 15), padx=5, pady=5, command=self.login).grid()
        Button(self.logf, text=' Create Account ', bd=3, font=('', 15), padx=5, pady=5, command=self.cr).grid(row=2,column=1)
        self.logf.pack()

        self.crf = Frame(self.master, padx=10, pady=10)
        Label(self.crf, text='Username: ', font=('', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.crf, textvariable=self.n_username, bd=5, font=('', 15)).grid(row=0, column=1)
        Label(self.crf, text='Password: ', font=('', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.crf, textvariable=self.n_password, bd=5, font=('', 15), show='*').grid(row=1, column=1)
        Button(self.crf, text='Create Account', bd=3, font=('', 15), padx=5, pady=5, command=self.new_user).grid()
        Button(self.crf, text='Go to Login', bd=3, font=('', 15), padx=5, pady=5, command=self.log).grid(row=2,column=1)

        #self.result = Frame(self.master, padx=10, pady=10)
        #Label(self.result, text=p, font=('',20), pady=5, padx=5).grid(sticky=W)
        #self.result.pack()


# create window and application object
root = Tk()
# root.title("Login Form")
main(root)
root.mainloop()