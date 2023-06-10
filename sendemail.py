# Author:Khan
# -*- codeing = utf-8 -*-
# @Time : 2022/12/3 19:53
# @File : main.py
# @Software: PyCharm

import rsa
from RSA import rsa_encrypt,rsa_decrypt
from RSA import gen_key,transferTostr
from makeprime import makeprime
from email.mime.text import MIMEText
from email.header import Header
import smtplib


def Alice_send_email(publickey):
    # 发信方的信息：发信邮箱，QQ 邮箱授权码
    from_addr = '1850188140@qq.com'
    password = 'dtrowmklxfsihabb'
    # 收信方邮箱
    to_addr = '1850188140@qq.com'
    # 发信服务器
    smtp_server = 'smtp.qq.com'

    # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
    msg = MIMEText('Alice_publickey is: '+publickey, 'plain', 'utf-8')
    # 邮件头信息
    msg['From'] = Header('Alice')  # 发送者
    msg['To'] = Header('Bob')  # 接收者
    subject = 'Alice_Pub'
    msg['Subject'] = Header(subject, 'utf-8')  # 邮件主题

    try:
        smtpobj = smtplib.SMTP_SSL(smtp_server)
        # 建立连接--qq邮箱服务和端口号（可百度查询）
        smtpobj.connect(smtp_server, 465)
        # 登录--发送者账号和口令
        smtpobj.login(from_addr, password)
        # 发送邮件
        smtpobj.sendmail(from_addr, to_addr, msg.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("无法发送邮件")
    finally:
        # 关闭服务器
        smtpobj.quit()

def Bob_send_email(message):
    # 发信方的信息：发信邮箱，QQ 邮箱授权码
    from_addr = '1850188140@qq.com'
    password = 'dtrowmklxfsihabb'
    # 收信方邮箱
    to_addr = '1850188140@qq.com'
    # 发信服务器
    smtp_server = 'smtp.qq.com'
    message=str(message)
    # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
    msg = MIMEText('The message is: '+message, 'plain', 'utf-8')
    # 邮件头信息
    msg['From'] = Header('Bob')  # 发送者
    msg['To'] = Header('Alice')  # 接收者
    subject = 'Bob_message'
    msg['Subject'] = Header(subject, 'utf-8')  # 邮件主题

    try:
        smtpobj = smtplib.SMTP_SSL(smtp_server)
        # 建立连接--qq邮箱服务和端口号（可百度查询）
        smtpobj.connect(smtp_server, 465)
        # 登录--发送者账号和口令
        smtpobj.login(from_addr, password)
        # 发送邮件
        smtpobj.sendmail(from_addr, to_addr, msg.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("无法发送邮件")
    finally:
        # 关闭服务器
        smtpobj.quit()