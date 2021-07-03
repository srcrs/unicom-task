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

def login(womail_url):
        try:
            url = womail_url
            headers = {
                "User-Agent": "User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3868.400 QQBrowser/10.8.4394.400"
            }
            res = requests.get(url=url, headers=headers, allow_redirects=False)
            set_cookie = res.headers["Set-Cookie"]
            cookies = re.findall("YZKF_SESSION.*?;", set_cookie)[0]
            if "YZKF_SESSION" in cookies:
                return cookies
            else:
                logging.info('【沃邮箱获取 cookies 失败】cookies: ' + json.dumps(res))
                return None
        except Exception as e:
            print("沃邮箱错误:", e)
            logging.error('【沃邮箱错误】' + str(e))
            return None

def dotask(cookies):
        msg = ""
        headers = {
            "User-Agent": "User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3868.400 QQBrowser/10.8.4394.400",
            "Cookie": cookies,
        }
        try:
            url = "https://nyan.mail.wo.cn/cn/sign/index/userinfo.do?rand=0.8897817905278955"
            res = requests.post(url=url, headers=headers)
            result = res.json()
            wxName = result.get("result").get("wxName")
            userMobile = result.get("result").get("userMobile")
            userdata = f"帐号信息: {wxName} - {userMobile[:3]}****{userMobile[-4:]}\n"
            msg += userdata
        except Exception as e:
            print("沃邮箱获取用户信息失败", e)
            logging.error('【沃邮箱获取用户信息失败】' + str(e))
            msg += "沃邮箱获取用户信息失败\n"
        try:
            url = "https://nyan.mail.wo.cn/cn/sign/user/checkin.do?rand=0.913524814493383"
            res = requests.post(url=url, headers=headers).json()
            result = res.get("result")
            if result == -2:
                msg += "每日签到: 已签到\n"
            elif result is None:
                msg += f"每日签到: 签到失败\n"
            else:
                msg += f"每日签到: 签到成功~已签到{result}天！\n"
        except Exception as e:
            print("沃邮箱签到错误", e)
            msg += "沃邮箱签到错误\n"
        try:
            url = "https://nyan.mail.wo.cn/cn/sign/user/doTask.do?rand=0.8776674762904109"
            data_params = {
                "每日首次登录手机邮箱": {"taskName": "loginmail"},
                "和WOWO熊一起寻宝": {"taskName": "treasure"},
                "去用户俱乐部逛一逛": {"taskName": "club"},
            }
            for key, data in dict.items(data_params):
                try:
                    res = requests.post(url=url, data=data, headers=headers).json()
                    result = res.get("result")
                    if result == 1:
                        msg += f"{key}: 做任务成功\n"
                    elif result == -1:
                        msg += f"{key}: 任务已做过\n"
                    elif result == -2:
                        msg += f"{key}: 请检查登录状态\n"
                    else:
                        msg += f"{key}: 未知错误\n"
                except Exception as e:
                    print(f"沃邮箱执行任务【{key}】错误", e)
                    msg += f"沃邮箱执行任务【{key}】错误"

        except Exception as e:
            print("沃邮箱执行任务错误", e)
            msg += "沃邮箱执行任务错误错误"
        return msg

def WoMailCheckIn(womail_url):
        try:
            cookies = login(womail_url)
            if cookies:
                msg = dotask(cookies)
                logging.info('【沃邮箱】'+msg)
            else:
                msg = "登录失败"
        except Exception as e:
            print(e)
            logging.error('登录失败')
            logging.error(e)
            msg = "登录失败"
        return msg

def main_handler(event, context):
    users = readJson()
    for user in users:
        #清空上一个用户的日志记录
        open('./log.txt',mode='w',encoding='utf-8')
        #开始任务
        global womail_url

        womail_url=user['womail_url']
        
        if len(womail_url)>0:
            WoMailCheckIn(womail_url)
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
