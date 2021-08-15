# -*- coding: utf-8 -*-
# @Time    : 2021/08/14 16:30
# @Author  : srcrs
# @Email   : srcrs@foxmail.com
import requests,json,time,re,login,logging,traceback,os,random,notify,datetime
from lxml.html import fromstring
import pytz

#获取 encrymobile，用于抽奖
def get_encryptmobile(client):
    page = client.post('https://m.client.10010.com/dailylottery/static/textdl/userLogin')
    page.encoding='utf-8'
    match = re.search('encryptmobile=\w+',page.text,flags=0)
    usernumber = match.group(0)[14:]
    return usernumber

#获取Asia/Shanghai时区时间戳
def getTimezone():
    timezone = pytz.timezone('Asia/Shanghai')
    dt = datetime.datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S")
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp

#获取积分余额
#分类：奖励积分、定向积分、通信积分
def getIntegral(client):
    try:
        integral = client.post('https://m.client.10010.com/welfare-mall-front/mobile/show/bj2205/v2/Y')
        integral.encoding = 'utf-8'
        res = integral.json()
        for r in res['resdata']['data']:
            if r['name'] != None and r['number'] != None:
                logging.info('【'+str(r['name'])+'】: ' + str(r['number']))
        time.sleep(1)
    except Exception as e:
        print(traceback.format_exc())
        logging.error('【积分余额】: 错误，原因为: ' + str(e))