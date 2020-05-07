#!/usr/bin/env python3.6
# -*- conding:utf-8 -*-
# @Time   : 2019/10/14 2:29 下午
# @Author : liwenfeng 
# @Desc   : aws sdk send messages
# @Note   :

import boto3
from flask import Flask, request

client = boto3.client('sns')
app = Flask(__name__)


# 发送短信
def send_sms(tel, mess):
    send = client.publish(
        PhoneNumber=tel,
        Message=mess)
    return send


@app.route('/sms', methods=['post'])
# 获取请求的值
def get_value():
    op_tel = request.form.get('tos')
    mes = request.form.get('content')
    op_tel1 = op_tel.split(',')
    for tel in op_tel1:
        tel = '+86'+tel
        send_sms(tel, mes)
    return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8005, debug=False)
