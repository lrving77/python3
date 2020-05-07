#!/usr/bin/env python3.6
# -*- conding:utf-8 -*-
# @Time   : 2019/10/21 3:09 下午
# @Author : liwenfeng 
# @Desc   :
# @Note   :

import boto3
import datetime
import requests
import json


# 检查aws预留实例过期时间
def check_reserved_instance_time():
    ec2 = boto3.client('ec2')
    reserved_instances = ec2.describe_reserved_instances()
    current_time = datetime.datetime.now()
    for reserved_instance in reserved_instances['ReservedInstances']:
        if reserved_instance['State'] != 'active':
            continue
        else:
            reserved_type = reserved_instance['InstanceType']
            reserved_count = reserved_instance['InstanceCount']
            reserved_time = reserved_instance['End']
            reserved_time = datetime.datetime.strptime(str(reserved_time).split('+')[0], "%Y-%m-%d %H:%M:%S")
            retired_time = (reserved_time - current_time).days
            if retired_time <= 3:
                message = "预留实例类型:" + reserved_type, "数量:" + str(reserved_count), "多少天后过期:" + str(retired_time)
                # print(message)
                send_ding(message)


# 钉钉报警
def send_ding(txt):
    txt = "## **warning**\n" + str(txt)
    token = '42d59d3a06a14729f830ffdc5f996f6957c951dc2f31d0061e411f6c2b46c4bb'
    url = 'https://oapi.dingtalk.com/robot/send?access_token=%s' % token
    head = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "warinnig",
            "text": txt
        }
    }
    r = requests.post(url, data=json.dumps(data), headers=head)
    # print(r.status_code)   #获取响应状态码
    # print(r.content)       #获取响应消息
    # print(r.headers)       #获取响应头


if __name__ == '__main__':
    check_reserved_instance_time()
