# Code by GatoL
# -*- coding:utf-8 -*-
from Tkinter import *
import os
import socket
import time

def frame(root, side):
    w2 = Frame(root)
    w2.pack(side = side, expand = YES, fill = BOTH)
    return w2
def button(root, side, text, command = None):  
    w2 = Button(root, text = text, command = command)
    w2.pack(side = side, expand = YES, fill = BOTH)
    return w2

def login_server():
    if len(usrname.get())==0 or len(pasword.get())==0:
        usrname.set('error')
        pasword.set('error')
    else:
        s_client.sendall('1')
        time.sleep(0.1)
        s_client.sendall(usrname.get())
        time.sleep(0.1)
        s_client.sendall(pasword.get())
        switch=s_client.recv(1024)
        if switch=='500':
            usrname.set('incorrect username')
            pasword.set('incorrect password')
            print 'error'
        if switch=='200':
            global fee
            fee=s_client.recv(1024)
            w.destroy()
            Calculator().mainloop()
        if switch=='100':
            usrname.set('overdue')
            pasword.set('overdue')

class Recharge(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.pack(expand = YES, fill = BOTH)
        self.master.title('recharge')
        root_c=frame(self,TOP)
        label2=Label(root_c,text='Username')
        label2.pack(side='left')
        self.user2add=StringVar()
        entry1=Entry(root_c,textvariable=self.user2add)
        entry1.pack(side='right')
        root_c=frame(self,TOP)
        label3=Label(root_c,text='How much you wanna buy?')
        label3.pack(side='left')
        self.fee_add=StringVar()
        entry2=Entry(root_c,textvariable=self.fee_add)
        entry2.pack(side='right')
        root_c=frame(self,TOP)
        button1=Button(root_c,text='Confirm',command=self.buy)
        button1.pack(side='left')
        button2=Button(root_c,text='Close',command=self.recharge_close)
        button2.pack(side='right')
    def recharge_close(self):
        self.destroy()
    def buy(self):
        print 'buy'
        s_client.sendall('3')
        time.sleep(0.01)
        print self.user2add.get()
        s_client.sendall(self.user2add.get())
        time.sleep(0.01)
        frank=0
        for i in self.fee_add.get():
            if i not in '0123456789':
                s_client.sendall('-1')
                self.fee_add.set('pls type nothing but number')
                frank=1
                break
        if frank==0:
            s_client.sendall(self.fee_add.get())
            print self.fee_add.get()
            fee_buy=s_client.recv(1024)
            print fee_buy
            buy_window=Tk()
            root_buy=Frame(buy_window)
            root_buy.pack(side=TOP,expand=YES,fill=BOTH)
            if fee_buy=='-1':
                print 'not exist'
                Label(root_buy,text='No such username').pack()
            else:
                print 'exist'
                Label(root_buy,text='User '+self.user2add.get()+'\'s fee is '+fee_buy).pack()
            buy_window.title('Result of recharge')
            buy_window.mainloop()
class Calculator(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.pack(expand = YES, fill = BOTH)
        self.master.title('Simple Calculater')  
        display = StringVar()
        Entry(self, relief = SUNKEN,  
              textvariable = display).pack(side = TOP, expand = YES,fill = BOTH)
        display.set('You can login another '+fee+' times')
        for key in('123', '456', '789', '(0)'):  
            keyF = frame(self, TOP)  
            for char in key:  
                button(keyF, LEFT, char, lambda w = display, c = char:w.set(w.get() + c))
        opsF = frame(self, TOP)  
        for char in '+-*/=':
            if char == '=':  
                btn = button(opsF, LEFT, char)  
                btn.bind('<ButtonRelease - 1>', lambda e, s = self, w = display:s.calc(w), '+')
            else:  
                btn = button(opsF, LEFT, char, lambda w = display, s = '%s' %char:w.set(w.get() + s))
        clearF = frame(self, BOTTOM)  
        button(clearF, LEFT, 'clear', lambda w = display:w.set(''))

    def calc(self, display):
        try:
            s_client.sendall(display.get())
            result=s_client.recv(1024)
            display.set(result)
        except:
            display.set("ERROR")
def register():
    if len(usrname.get())==0 or len(pasword.get())==0:
        usrname.set('error')
        pasword.set('error')
    else:
        s_client.sendall('2')
        time.sleep(0.1)
        s_client.sendall(usrname.get())
        switch=s_client.recv(1024)
        if switch=='1024':
            s_client.sendall(pasword.get())
        result=s_client.recv(1024)
        if result=='200':
            usrname.set('register succeed')

        if result=='404':
            usrname.set('The username already exists')

def recharge_open():
    Recharge().mainloop()



global s_client
try:
    s_client=socket.socket()
    s_client.connect(('localhost',1995))
    w=Tk()
    usrname=StringVar()
    pasword=StringVar()
    root=Frame(w)
    root.pack(side=TOP,expand=YES,fill=BOTH)
    label_No1=Label(root,text='pls login')
    label_No1.pack()
    root=Frame(w)
    root.pack(side=TOP,expand=YES,fill=BOTH)
    label_No2=Label(root,text='username')
    label_No2.pack(side='left')
    entry_No1=Entry(root,textvariable=usrname)
    entry_No1.pack(side='right')
    root=Frame(w)
    root.pack(side=TOP,expand=YES,fill=BOTH)
    label_No3=Label(root,text='password')
    label_No3.pack(side='left')
    entry_No2=Entry(root,textvariable=pasword,show='*')
    entry_No2.pack(side='right')
    root=Frame(w)
    root.pack(side=TOP,expand=YES,fill=BOTH)
    button_No1=Button(root,text='login',command=login_server)
    button_No1.pack(side='left')
    button_No2=Button(root,text='register',command=register)
    button_No2.pack(side='right')
    button(root, side='right', text='recharge',command=recharge_open)
    w.title('login remote server')
    w.mainloop()

except:
    w=Tk()
    Label(text='Server not found,pls close').pack()
    w.mainloop()

