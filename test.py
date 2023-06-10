# Author:Khan
# -*- codeing = utf-8 -*-
# @Time : 2022/12/13 18:13
# @File : test.py
# @Software: PyCharm
import time
from makeprime import makeprime
import numpy
import logging
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64
from RSA import transferTostr,transferToNum,gen_key


logger = logging.getLogger(__name__)


def rsa_long_encrypt(publickey, msg, length=100):
    """
    单次加密串的长度最大为 (key_size/8)-11
    1024bit的证书用100， 2048bit的证书用 200
    """
    key = publickey
    msg=base64.b64encode(msg.encode("utf-8")).decode()
    pubobj = RSA.importKey(key)
    pubobj = PKCS1_v1_5.new(pubobj)
    res = []
    for i in range(0, len(msg), length):
        res.append(pubobj.encrypt(msg[i:i + length].encode()))
    return b"".join(res)


def rsa_long_decrypt(secretkey, message, default_length=128):
    private_key = secretkey
    # msg = base64.b64decode(message)
    msg=message
    length = len(msg)
    # default_length = 256
    # 私钥解密
    priobj = PKCS1_v1_5.new(RSA.importKey(private_key))
    # 长度不用分段
    if length < default_length:
        return b''.join(priobj.decrypt(msg, b'ubout'))
    # 需要分段
    offset = 0
    res = []
    while length - offset > 0:
        if length - offset > default_length:
            res.append(priobj.decrypt(msg[offset:offset + default_length], b'ubout'))
        else:
            res.append(priobj.decrypt(msg[offset:], b'ubout'))
        offset += default_length
        m = b''.join(res)
        n = m.decode("utf-8")
        # print(n)
    return base64.b64decode(n).decode('utf-8')

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
result1=rsa_long_encrypt(str(Alice_pub),str(message1))
print(result1)
filename='/Users/zhoukehan/Desktop/decrpt_message.txt'
file = open(filename, 'w')  # 打开文件
#result1="".join(map(str,result1))

number_dc = str(rsa_long_decrypt(str(Alice_priv), str(result1)))
answer=""
for i in range(0, len(number_dc)):
    if number_dc[i] != ',' and number_dc[i] != ' ' and number_dc[i] != '[' and number_dc[i] != ']' :
        answer = answer + number_dc[i]
message_dc=transferTostr(answer)
file2 = open('/Users/zhoukehan/Desktop/result.txt','w')
file2.write(message_dc)
file2.close()



