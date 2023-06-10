# Author:Khan
# -*- codeing = utf-8 -*-
# @Time : 2022/12/3 22:17
# @File : draw.py
# @Software: PyCharm

from RSA import gen_key,transferTostr,rsa_encrypt,rsa_decrypt
from makeprime import makeprime
from tkinter import *
from tkinter import messagebox
import tkinter.filedialog
from sendemail import Alice_send_email,Bob_send_email

Alice_priv=0
Alice_pub=0

root = Tk()
root.title('信息安全导论')
root.geometry("600x500+200+200") #500x(注意是x)300表示窗口大小，+100+200表示距屏幕的距离
btn01 = Button(root)
btn01["text"] = "Alice"
btn01.place(width=100,height=100,x=250,y=300)
btn02 = Button(root)
btn02["text"] = "Bob"
btn02.place(width=100,height=100,x=250,y=100)
label = Label(root,text='选择一个人',bg='grey',fg='#F0F0F0',font=('华文新魏',15),bd=5,relief='groove')
label.place(x=240,y=40)


def Alice(e):
    winNew = Toplevel(root)
    winNew.geometry('600x600')
    winNew.title('Alice')
    label2 = Label(winNew,text='输入密钥位数',bg='grey',fg='#F0F0F0',font=('华文新魏',15),bd=5,relief='groove')
    label2.place(x=250,y=50)
    inp1 = Entry(winNew)
    inp1.place(width=400, height=50, x=100, y=100)

    btn03 = Button(winNew)
    btn03["text"] = "生成密钥"
    btn03.place(width=100, height=100, x=250, y=200)

    btn04 = Button(winNew)
    btn04["text"] = "信息解密"
    btn04.place(width=100, height=100, x=250, y=400)

    btClose = Button(winNew, text='关闭', command=winNew.destroy)
    btClose.place(relx=0.7, rely=0.5)

    def GenerateKey(e):
        number = int(inp1.get())
        lb = Label(root, text='')
        lb.pack()
        p = makeprime(number)
        q = makeprime(number)
        global Alice_priv,Alice_pub
        Alice_pub, Alice_priv = gen_key(p, q)

        if Alice_pub==0:
            return_value = messagebox.showinfo('生成结果','生成失败')
            # <class 'str'> ok
        else:
            str1='生成成功，明码为'+str(Alice_pub)+',已发送至Bob邮箱'
            print(str(Alice_priv))
            Alice_send_email(str(Alice_pub))
            return_value = messagebox.showinfo('生成结果',str1)

    def Decrypt(e):
        filename = tkinter.filedialog.askopenfilename()
        if filename != '':
            file = open(filename, 'r')  # 打开文件
            message = file.readline()  # 读取所有行
            number_dc = str(rsa_decrypt(Alice_priv, message))
            answer = ""
            for i in range(0, len(number_dc)):
                if number_dc[i] != ',' and number_dc[i] != ' ' and number_dc[i] != '[' and number_dc[i] != ']':
                    answer = answer + number_dc[i]
            message_dc = transferTostr(answer)
            #message_dc=transferTostr(number_dc)
            file2 = open('/Users/zhoukehan/Desktop/decrpt_message.txt','w')
            file2.write(message_dc)
            file2.close()
            return_value = messagebox.showinfo('信息处理结果', '解密成功！')
        else:
            pass

    btn03.bind("<Button-1>", GenerateKey)
    btn04.bind("<Button-1>", Decrypt)

def Bob(e):
    winNew = Toplevel(root)
    winNew.geometry('600x600')
    winNew.title('Bob')
    label3 = Label(winNew, text='Alice_pub', bg='grey', fg='#F0F0F0', font=('华文新魏', 15), bd=5, relief='groove')
    label3.place(x=250, y=20)
    inp2 = Entry(winNew)
    inp2.place(width=400, height=50, x=100, y=100)
    def getkey():
        Thepubkey = str(inp2.get())
        countindex = Thepubkey.index(', ')
        global Alice_pub
        Alice_pub = [Thepubkey[0:countindex], Thepubkey[countindex + 1:]]
    btn07 = Button(winNew, command=getkey)
    btn07["text"] = "确认"
    btn07.place(width=50, height=50, x=550, y=100)
    def sendmessage_yes():
        filename = tkinter.filedialog.askopenfilename()
        if filename != '':
            file = open(filename, 'r')  # 打开文件
            message = file.readline()  # 读取所有行
            key = rsa_encrypt(Alice_pub, message)
            Bob_send_email(key)
            return_value = messagebox.showinfo('发送结果', '发送成功')
        else:
            pass
    btn05 = Button(winNew,command=sendmessage_yes)
    btn05["text"] = "RSA信息加密传输"
    btn05.place(width=100, height=100, x=250, y=200)
    def sendmessage_not():
        filename = tkinter.filedialog.askopenfilename()
        if filename != '':
            file = open(filename, 'r')# 打开文件
            message = file.readline()  # 读取所有行
            Bob_send_email(message)
            return_value = messagebox.showinfo('发送结果', '发送成功')
        else:
            pass
    btn06 = Button(winNew,command=sendmessage_not)
    btn06["text"] = "信息不加密传输"
    btn06.place(width=100, height=100, x=250, y=400)
    btClose = Button(winNew, text='关闭', command=winNew.destroy)
    btClose.place(relx=0.7, rely=0.5)





btn01.bind("<Button-1>", Alice)  # 事件绑定
btn02.bind("<Button-1>", Bob)  # 事件绑定


root.mainloop()  # 调用组件的mainloop()方法,进入事件循环