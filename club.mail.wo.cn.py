# -*- coding: utf-8 -*-
# @Time    : 2021/6/23 13:30
# @Author  : lhx11187
# @Email   : lhx11187@qq.com
#
# 沃邮箱签到抽奖


import requests,json,time,re,login,logging,traceback,os,random,notify,datetime
from lxml.html import fromstring
import pytz

def main_handler(event, context):
    users = readJson()
    for user in users:
        #清空上一个用户的日志记录
        open('./log.txt',mode='w',encoding='utf-8')
        //
        global Cookies=user['Cookies']
        if len(Cookies)>0:
          daySign()
          lottery()
        if ('email' in user) :
            notify.sendEmail(user['email'])
        if ('dingtalkWebhook' in user) :
            notify.sendDing(user['dingtalkWebhook'])
        if ('telegramBot' in user) :
            notify.sendTg(user['telegramBot'])
        if ('pushplusToken' in user) :
            notify.sendPushplus(user['pushplusToken'])
        if ('serverchanSCKEY' in user) :
            notify.sendServerChan(user['serverchanSCKEY'])
        if('enterpriseWechat' in user) :
            notify.sendWechat(user['enterpriseWechat'])
        if('IFTTT' in user) :
            notify.sendIFTTT(user['IFTTT'])
        if('Bark' in user) :
            notify.sendBark(user['Bark'])

#主函数入口
if __name__ == '__main__':
    main_handler("","")
