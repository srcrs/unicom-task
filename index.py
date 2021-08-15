import requests,json,time,re,login,logging,traceback,os,random,notify,datetime,util
from lxml.html import fromstring
import pytz,importlib

#用户登录全局变量
client = None

#读取用户配置信息
#错误原因有两种：格式错误、未读取到错误
def readJson():
    try:
        #用户配置信息
        with open('./config/config.json','r') as fp:
            users = json.load(fp)
            return users
    except Exception as e:
        print(traceback.format_exc())
        logging.error('账号信息获取失败错误，原因为: ' + str(e))
        logging.error('1.请检查是否在Secrets添加了账号信息，以及添加的位置是否正确。')
        logging.error('2.填写之前，是否在网站验证过Json格式的正确性。')

#运行任务
def runTask(client, user):
    with os.scandir('./task') as entries:
        for entry in entries:
            if entry.is_file():
                if entry.name == '__init__.py':
                    continue
                task_module = importlib.import_module('task.'+entry.name[:-3])
                task_class = getattr(task_module, entry.name[0:-3])
                task_obj = task_class()
                task_obj.run(client, user)

def sendNotice(user):
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

#腾讯云函数入口
def main_handler(event, context):
    users = readJson()
    for user in users:
        #清空上一个用户的日志记录
        open('./log.txt',mode='w',encoding='utf-8')
        global client
        client = login.login(user['username'],user['password'],user['appId'])
        #获取账户信息
        util.getIntegral(client)
        if client != False:
            runTask(client, user)
        sendNotice(user)

#主函数入口
if __name__ == '__main__':
    main_handler("","")