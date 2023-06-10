# Author:Khan
# -*- codeing = utf-8 -*-
# @Time : 2022/12/3 20:13
# @File : RSA.py
# @Software: PyCharm

import time
from makeprime import makeprime
import numpy


# 构造字典
dict = {'a': '31', 'b': '32', 'c': '33', 'd': '34', 'e': '35', 'f': '36', 'g': '37',
        'h': '38', 'i': '39', 'j': '10', 'k': '11', 'l': '12', 'm': '13', 'n': '14',
        'o': '15', 'p': '16', 'q': '17', 'r': '18', 's': '19', 't': '20', 'u': '21',
        'v': '22', 'w': '23', 'x': '24', 'y': '25', 'z': '26', '1': '41', '2': '42',
        '3': '43', '4': '44', '5': '45', '6': '46', '7': '47', '8': '48', '9': '49',
        '0': '40', ' ': '50', 'A': '51', 'B': '52', 'C': '53', 'D': '54', 'E': '55', 'F': '56', 'G': '57',
        'H': '58', 'I': '59', 'J': '60', 'K': '61', 'L': '62', 'M': '63', 'N': '64',
        'O': '65', 'P': '66', 'Q': '67', 'R': '68', 'S': '69', 'T': '70', 'U': '71',
        'V': '72', 'W': '73', 'X': '74', 'Y': '75', 'Z': '76', ',':'77', '.':'78', '\'':'79', '-':'80'}


# 字符与数字之间的映射转换
def transferToNum(str):
    m = ""
    for d in str:
        m += dict[d]
    return m


def transferTostr(num):
    n = ""
    for i in range(0, len(num), 2):
        n += {value: key for key, value in dict.items()}[num[i] + num[i + 1]]
    return n


'''
扩展欧几里的算法
计算 ax + by = 1中的x与y的整数解（a与b互质）
'''


def ext_gcd(a, b):
    if b == 0:
        x1 = 1
        y1 = 0
        x = x1
        y = y1
        r = a
        return r, x, y
    else:
        r, x1, y1 = ext_gcd(b, a % b)
        x = y1
        y = x1 - a // b * y1
        return r, x, y


'''
超大整数超大次幂然后对超大的整数取模
(base ^ exponent) mod n
'''


def exp_mode(base, exponent, n):
    base=int(base)
    exponent=int(exponent)
    n=int(n)
    bin_array = bin(exponent)[2:][::-1]
    r = len(bin_array)
    base_array = []

    pre_base = base
    base_array.append(pre_base)

    for _ in range(r - 1):
        next_base = (pre_base * pre_base) % n
        base_array.append(next_base)
        pre_base = next_base

    a_w_b = __multi(base_array, bin_array, n)
    return a_w_b % n


def __multi(array, bin_array, n):
    result = 1
    for index in range(len(array)):
        a = array[index]
        if not int(bin_array[index]):
            continue
        result *= a
        result = result % n  # 加快连乘的速度
    return result


# 生成公钥私钥，p、q为两个超大质数
def gen_key(p, q):
    n = p * q
    fy = (p - 1) * (q - 1)  # 计算与n互质的整数个数 欧拉函数
    e = 65537  # 选取e 65537
    a = e
    b = fy
    x = ext_gcd(a, b)[1]

    if x < 0:
        d = x + fy
    else:
        d = x
    #print("公钥:" + "(" + str(n) + "," + str(e) + ")\n私钥:" + "(" + str(n) + "," + str(d) + ")")
    return (n, e), (n, d)


# 加密 m是被加密的信息 加密成为c
def encrypt(m, pubkey):
    n = pubkey[0]
    e = pubkey[1]

    c = exp_mode(m, e, n)
    return c


# 解密 c是密文，解密为明文m
def decrypt(c, selfkey):
    n = selfkey[0]
    d = selfkey[1]

    m = exp_mode(c, d, n)
    return m


def rsa_encrypt(pubkey,txt):
    m = str(transferToNum(txt))
    #c=[]
    c=encrypt(m,pubkey)
    '''
    for i in range(0, len(m), 16):
        c.append(encrypt(m[i:i + 16].encode(),pubkey))
    '''
    return c


def rsa_decrypt(privatekey,txt):
    d = []
    m = txt
    d=decrypt(txt, privatekey)
    answer=""
    for i in range(0, len(m), 2):
        if i+1<len(m):
            if m[i] != ',' and m[i] != ' ' and m[i] != '\n':
                answer = answer+m[i]
            if m[i+1] != ',' and m[i+1] != ' ' and m[i] != '\n':
                answer = answer+m[i+1]
        else:
            if m[i] != ',' and m[i] != ' ' and m[i] != '\n':
                answer = answer+m[i]
    for i in range(0, len(answer), 16):
        d.append(decrypt(answer[i:i + 16].encode(), privatekey))
    return d




'''

#测试
number = 50
p = makeprime(number)
q = makeprime(number)
Alice_pub, Alice_priv = gen_key(p, q)
print(Alice_pub,Alice_priv)
filename1='/Users/zhoukehan/Desktop/message.txt'
file1 = open(filename1, 'r')  # 打开文件
message1 = file1.readline()  # 读取所有行
print(message1)
m = str(transferToNum(message1))
print(m)
result1=rsa_encrypt(Alice_pub,message1)
print(result1)
filename='/Users/zhoukehan/Desktop/decrpt_message.txt'
file = open(filename, 'w')  # 打开文件
#result1="".join(map(str,result1))

number_dc = str(rsa_decrypt(Alice_priv, result1))
answer=""
for i in range(0, len(number_dc)):
    if number_dc[i] != ',' and number_dc[i] != ' ' and number_dc[i] != '[' and number_dc[i] != ']' :
        answer = answer + number_dc[i]
message_dc=transferTostr(answer)
file2 = open('/Users/zhoukehan/Desktop/result.txt','w')
file2.write(message_dc)
file2.close()

'''

