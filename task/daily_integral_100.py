# -*- coding: utf-8 -*-
# @Time    : 2021/08/14 16:30
# @Author  : srcrs
# @Email   : srcrs@foxmail.com
import requests,json,time,re,login,logging,traceback,os,random,notify,datetime
from lxml.html import fromstring

#天天抽奖
#我的 --> 我的金币 --> 天天抽好礼
class daily_integral_100:
    def run(self, client, user):
        data = {
            'from': random.choice('123456789') + ''.join(random.choice('0123456789') for i in range(10))
        }
        try:
            integral = client.post('https://m.client.10010.com/welfare-mall-front/mobile/integral/gettheintegral/v1', data=data)
            integral.encoding = 'utf-8'
            res = integral.json()
            logging.info("【100定向积分】: " + res['msg'])
            time.sleep(1)
        except Exception as e:
            print(traceback.format_exc())
            logging.error('【100定向积分】: 错误，原因为: ' + str(e))