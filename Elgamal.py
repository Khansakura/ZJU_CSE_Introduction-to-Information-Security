# Author:Khan
# -*- codeing = utf-8 -*-
# @Time : 2022/12/13 20:47
# @File : elgmal.py
# @Software: PyCharm

import random
from math import pow

a = random.randint(2, 10) #产生小于p的随机常数a

def gcd(a, b):
  if a < b:
    return gcd(b, a)
  elif a % b == 0:
    return b;
  else:
    return gcd(b, a % b)
  # Generating large random numbers

def gen_key(q):
  key = random.randint(pow(10, 20), q)
  while gcd(q, key) != 1:
    key = random.randint(pow(10, 20), q)
  return key

# Modular exponentiation
def power(a, b, c):
  x = 1
  y = a
  while b > 0:
    if b % 2 == 0:
      x = (x * y) % c;
    y = (y * y) % c
    b = int(b / 2)
  return x % c

# Asymmetric encryption
def encrypt(msg, p, h, r):
  en_msg = []
  b = gen_key(p) # 得b
  K = power(h, b, p)#K=(Sa)^b mod p
  C1 = power(r, b, p) #C1=Sb=r^b mod p
  for i in range(0, len(msg)):
    en_msg.append(msg[i])
  #print("密钥C1 : ", C1)
  # print("(Sa)^b mod p used : ", K)
  for i in range(0, len(en_msg)):
    en_msg[i] = K * ord(en_msg[i])
  #print("密钥C2 : ", en_msg)
  print("密钥为：",(C1,en_msg))
  return en_msg, C1

def decrypt(C2, C1, a, p):
  dr_msg = []
  h = power(C1, a, p)
  for i in range(0, len(C2)):
    dr_msg.append(chr(int(C2[i] / h)))
  return dr_msg

# Driver code
def main():
  msg = '12345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345'        # 共125位数字，1000bit
  print("需要加密的明文为 :", msg)
  p = random.randint(pow(10, 20), pow(10, 50))# 获得大素数q
  r = random.randint(2, p)#得r
  a = gen_key(p) # Private key for receiver
  h = power(r, a, p)
  C2, C1 = encrypt(msg, p, h, r)
  dr_msg = decrypt(C2, C1, a, p)
  dmsg = ''.join(dr_msg)
  print("解密后得到的明文为 :", dmsg);

if __name__ == '__main__':
  main()
