# -*- coding: utf-8 -*-
# @Time    : 2021/6/23 13:30
# @Author  : lhx11187
# @Email   : lhx11187@qq.com
#
# 沃邮箱签到抽奖


import requests,json,time,re,login,logging,traceback,os,random,notify,datetime
from lxml.html import fromstring
import pytz

Cookies = None
PhoneNo = None

#读取用户配置信息
#错误原因有两种：格式错误、未读取到错误
def readJson():
    try:
        #用户配置信息
        with open('./config.json','r') as fp:
            users = json.load(fp)
            return users
    except Exception as e:
        print(traceback.format_exc())
        logging.error('账号信息获取失败错误，原因为: ' + str(e))
        logging.error('1.请检查是否在Secrets添加了账号信息，以及添加的位置是否正确。')
        logging.error('2.填写之前，是否在网站验证过Json格式的正确性。')
        

#每日签到
def daySign():
    try:
        url = 'https://club.mail.wo.cn/clubwebservice/club-user/user-sign/create'
        url1 = 'https://club.mail.wo.cn/clubwebservice/growth/userSign'
        url2 = 'https://club.mail.wo.cn/clubwebservice/growth/addIntegral?phoneNum='+PhoneNo+'&resourceType=huodong'
        url3 = 'https://club.mail.wo.cn/clubwebservice/growth/addIntegral?phoneNum='+PhoneNo+'&resourceType=lookMail'
        url4 = 'https://club.mail.wo.cn/clubwebservice/growth/addIntegral?phoneNum='+PhoneNo+'&resourceType=womenhuzhuye'
        url5 = 'https://club.mail.wo.cn/clubwebservice/growth/addIntegral?phoneNum='+PhoneNo+'&resourceType=appxiazai'
        headers = {
                    'Cookie':Cookies,
                    'Content-Type': 'application/json;charset=utf-8',
                    'Host': 'club.mail.wo.cn',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Connection': 'keep-alive',
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.17(0x17001126) NetType/4G Language/zh_CN miniProgram',
                  }
        #params={"wd":"Python"}
        
        
        #body = json.dumps(data).encode(encoding='utf-8')
        #body = urllib.parse.urlencode(data).encode(encoding='utf-8')
        #resp = requests.post(url, data=body, headers=headers)
        #resp = requests.get(url=url,params=params,headers=headers)
        msg=""
        res = requests.get(url=url,headers=headers)
        res.encoding = 'utf-8'
        #print(type(res))
        print(res.text)
        logging.info('【每日签到】: ' + res.text)
        result = res.json().get("status")
        if result == "EUS0011":
            msg += "每日签到: 已签到\n"
        elif result =="0000":
            msg += f"每日签到: 签到成功\n"
        else:
            msg += f"每日签到: 签到失败\n"
        logging.info('【每日签到】: ' + msg)

        msg=""
        res = requests.get(url=url1,headers=headers)
        res.encoding = 'utf-8'
        print(res.text)
        logging.info('【每日签到】: ' + res.text)
        result = res.json().get("status")
        if result == "ERROR":
            msg += res.json().get("description")
        else:
            msg += f"每日签到: 签到成功\n"
        logging.info('【每日签到】: ' + msg)
        '''
        res = requests.get(url=url2,headers=headers)
        res.encoding = 'utf-8'
        res = res.json()
        logging.info('【每日签到】: ' + json.dumps(res))
        
        res = requests.get(url=url3,headers=headers)
        res.encoding = 'utf-8'
        res = res.json()
        logging.info('【每日签到】: ' + json.dumps(res))

        res = requests.get(url=url4,headers=headers)
        res.encoding = 'utf-8'
        res = res.json()
        logging.info('【每日签到】: ' + json.dumps(res))

        res = requests.get(url=url5,headers=headers)
        res.encoding = 'utf-8'
        res = res.json()
        logging.info('【每日签到】: ' + json.dumps(res))

        
        if res['status'] == '200':
            logging.info('【每日签到】: ' + '打卡成功')
        elif res['status'] == 'ERROR':
            logging.info('【每日签到】: ' + res['description'])
        '''
        time.sleep(1)
    except Exception as e:
        print(traceback.format_exc())
        logging.error('【每日签到】: 错误，原因为: ' + str(e))

#每日签到
def lottery():
    try:
        url = 'https://club.mail.wo.cn/clubwebservice/lottery-record/executive-activity-draw/main-activity'
        headers = {
                    'Cookie':Cookies,
                    'Content-Type': 'application/json;charset=utf-8',
                    'Host': 'club.mail.wo.cn',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Connection': 'keep-alive',
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.17(0x17001126) NetType/4G Language/zh_CN miniProgram',
                  }
        #params={"wd":"Python"}
        
        
        #body = json.dumps(data).encode(encoding='utf-8')
        #body = urllib.parse.urlencode(data).encode(encoding='utf-8')
        #resp = requests.post(url, data=body, headers=headers)
        #resp = requests.get(url=url,params=params,headers=headers)


        res = requests.get(url=url,headers=headers)
        res.encoding = 'utf-8'
        res = res.json()
        logging.info('【每日抽奖】: ' + json.dumps(res))
        
        if res['status'] == '0000':
            logging.info('【每日抽奖】: ' + '抽奖成功')
        elif res['status'] == '0002':
            logging.info('【每日抽奖】: ' + res['msg'])
        time.sleep(1)
    except Exception as e:
        print(traceback.format_exc())
        logging.error('【每日抽奖】: 错误，原因为: ' + str(e))

def main_handler(event, context):
    users = readJson()
    for user in users:
        #清空上一个用户的日志记录
        open('./log.txt',mode='w',encoding='utf-8')
        #开始任务
        global Cookies
        global PhoneNo

        Cookies=user['mailwoCookies']
        PhoneNo=user['username']
        
        if len(Cookies)>0:
          daySign()
          #lottery()
        if ('email' in user) :
            notify.sendEmail(user['email'])
            notify.sendMail(user['email'],user['wo_email'],user['wo_email_pwd'])
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
