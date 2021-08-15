# -*- coding: utf-8 -*-
# @Time    : 2021/08/14 16:30
# @Author  : srcrs
# @Email   : srcrs@foxmail.com
import requests,json,time,re,login,logging,traceback,os,random,notify,datetime,util
from lxml.html import fromstring

#积分抽奖，可在环境变量中设置抽奖次数，否则每天将只会抽奖一次
#需要注意的是，配置完抽奖次数，程序每运行一次都将触发积分抽奖，直至达每日30次抽奖用完或积分不够(测试过程中未中过奖)
#位置: 发现 --> 定向积分 --> 小积分，抽好礼
class points_lottery:
    def run(self, client, user):
        if ('lotteryNum' not in user):
            return False
        try:
            numjsp = util.get_encryptmobile(client)
            #如果用户未设置此值，将不会自动抽奖
            #预防用户输入10以上，造成不必要的抽奖操作
            n = user['lotteryNum']
            num = min(10,int(n))
            for i in range(num):
                #用积分兑换抽奖机会
                client.get('https://m.client.10010.com/dailylottery/static/integral/duihuan?goldnumber=10&banrate=30&usernumberofjsp=' + numjsp)
                #进行抽奖
                payx = client.post('https://m.client.10010.com/dailylottery/static/integral/choujiang?usernumberofjsp=' + numjsp + '&flag=convert')
                payx.encoding = 'utf-8'
                res2 = payx.json()
                logging.info("【积分抽奖】: " + res2['RspMsg'] + ' x' + str(i+1))
                #等待随机秒钟
                time.sleep(5)
        except Exception as e:
            print(traceback.format_exc())
            logging.error('【积分抽奖】: 错误，原因为: ' + str(e))