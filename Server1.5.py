# Code by GatoL
# -*- coding:utf-8 -*-
import socket
import re
import os
import thread
from Tkinter import *
from time import sleep
import multiprocessing
import threading
import login_user
def jjcc(string):
    labelindex=[-1]
    for i in range(0,len(string)):
        if  string[i]=='*'or string[i]=='+'or string[i]=='-'or string[i]=='/':
            labelindex.append(i)
    labelindex.append(len(string))
    num=[]
    for i in range(0,len(labelindex)-1):
        num.append(int(string[labelindex[i]+1:labelindex[i+1]]))
    result_un=numcalc_cc(string,labelindex,num)
    
    result=numcalc_jj(string,labelindex,result_un)
    return result[0]

def numcalc_cc(string,labelindex,num):
    if(len(num)>1):
        for i in range(0,len(labelindex)-2):
            if  string[labelindex[i+1]]=='*':
                n_num=[]
                n_num.append(num[i]*num[i+1])
                new_num=num[0:i]+num[i+2:len(num)]
                new_num=n_num+new_num
                labelindex=labelindex[0:i+1]+labelindex[i+2:len(labelindex)]
                return numcalc_cc(string,labelindex,new_num)
            if  string[labelindex[i+1]]=='/':
                n_num=[]
                n_num.append(num[i]/num[i+1])
                new_num=num[0:i]+num[i+2:len(num)]
                new_num=n_num+new_num
                labelindex=labelindex[0:i+1]+labelindex[i+2:len(labelindex)]
                return numcalc_cc(string,labelindex,new_num)
        return num
    if(len(num)==1):
        return num

def numcalc_jj(string,labelindex,num):
    count = 0
    if len(num)>1:
        for i in range(0,len(labelindex)-2):
            if  string[labelindex[i+1]]=='+':
                n_num=[]
                n_num.append(num[0]+num[1])
                new_num=n_num+num[2:]
                labelindex=labelindex[0:i+1]+labelindex[i+2:len(labelindex)]
                return numcalc_jj(string,labelindex,new_num)
            if  string[labelindex[i+1]]=='-':
                n_num=[]
                n_num.append(num[0]-num[1])
                new_num=n_num+num[2:]
                labelindex=labelindex[0:i+1]+labelindex[i+2:len(labelindex)]
                return numcalc_jj(string,labelindex,new_num)

    if len(num)==1:
        return num

def deal_with_string(string):
    
    new_string=''
    for i in map(lambda letter:letter and letter.strip(),string):new_string +=str(i)
    return offThebrackets(new_string)

def offThebrackets(new_string):
    pattern=re.compile('\([^()]+\)')
    brackets=re.findall(pattern,new_string)
    if brackets == []:
        
        return str(jjcc(new_string))
    for group in brackets:
        method= re.escape(group)
        str_f='0'+str(group[1:len(group)-1])
        new_string=re.sub(method,str(jjcc(str_f)),new_string)
    return offThebrackets(new_string)

class Control_window(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.pack(expand = YES, fill = BOTH)
        self.master.title('Server control window')
        username1=StringVar()
        username2=StringVar()
        username3=StringVar()
        username4=StringVar()
        username5=StringVar()
        fee1=StringVar()
        fee2=StringVar()
        fee3=StringVar()
        fee4=StringVar()
        fee5=StringVar()
        
        self.a=[['User1',username1,fee1],['User2',username2,fee2],['User3',username3,fee3],['User4',username4,fee4],['User5',username5,fee5]]
        for user in self.a:
            root=frame(self,TOP)
            Label(root,text=user[0]).pack(side='left')
            Entry(root,textvariable=user[1]).pack(side='right')
            Entry(root,textvariable=user[2]).pack(side='right')
        root=frame(self,TOP)
    def fresh(self,username,fee):
        for user in self.a:
            if len(user[1].get())==0:
                print'fresh success'
                user[1].set(username)
                user[2].set(fee)
                break

def response(connection,address):
    while(1):
        mode=connection.recv(1024)
        if mode=='1':
            usr=connection.recv(1024)
            sleep(0.1)
            pas=connection.recv(1024)
            print usr,pas
            coin=1
            for i in login:
                if usr==i and pas==login[i] and value[usr]>0:
                    connection.sendall('200')
                    sleep(0.1)
                    value[usr]-=1
                    connection.sendall(str(value[usr]))
                    for i in range(0,100):
                        string = connection.recv(1024)
                        try:
                            result = deal_with_string(string)
                            connection.sendall(str(result))
                        except:
                            connection.sendall('error')
                if usr==i and pas==login[i] and value[usr]==0:
                    connection.sendall('100')
                    coin=0
            if coin==1:
                connection.sendall('500')
        if mode=='2':
            usr=connection.recv(1024)
            connection.sendall('1024')
            pas=connection.recv(1024)
            key=1
            if len(usr)!=0 and len(pas)!=0:
                for i in login:
                    if usr==i:
                        key=0
                        connection.sendall('404')
                        print 'already exists'
                if key==1:
                    connection.sendall('200')
                    login[usr]=pas
                    value[usr]=0
            print login
        if mode=='3':
            print'3'
            user2add=connection.recv(1024)
            print user2add
            fee_add=connection.recv(1024)
            print fee_add
            if fee_add!='-1':
                f=0
                for i in login:
                    if user2add==i:
                        print 'exist'
                        sleep(0.1)
                        value[user2add]+=int(fee_add)
                        connection.sendall(str(value[user2add]))
                        f=1
                if f==0:
                    connection.sendall('-1')
                    print 'not exist'
def fresh_window():
    print 'fresh'
    print user_online
    for i in user_online.keys():
        interface.fresh(i,user_online[i])
        user_online.pop(i)
    interface.after(1000,fresh_window)
def frame(root, side):
    w2 = Frame(root)
    w2.pack(side = side, expand = YES, fill = BOTH)
    return w2
def window():
    while(1):
        sleep(0.1)
        connection,address = s.accept()
        thread.start_new_thread(response,(connection,address))
def run(usr):
    inter_root=Tk()
    Label(inter_root,text=usr).pack(side='left')
    Label(inter_root,text=value[usr]).pack(side='right')
    inter_root.mainloop()
if __name__=='__main__':
    #lock=threading.Lock()
    #global user_online
    #manager=multiprocessing.Manager()
    #user_online=manager.dict()
    #user_online['test']='use'
    user_online={}
    login={'user':'10'}
    value={'user':11}
    s=socket.socket()
    s.bind(('localhost',1995))
    s.listen(5)
    # p1=multiprocessing.Process(target=run)
    #  global interface
    # interface=Control_window()

        #interface.after(1000,fresh_window)
        #  p1=multiprocessing.Process(target=run,args=(interface,))
    window()

#p1.start()

#user:user password:1024








