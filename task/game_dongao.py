# -*- coding: utf-8 -*-
# @Time    : 2021/08/14 16:30
# @Author  : srcrs
# @Email   : srcrs@foxmail.com
import requests,json,time,re,login,logging,traceback,os,random,notify,datetime
from lxml.html import fromstring

#冬奥积分活动，第1和7天，可领取600定向积分，其余领取300定向积分,有效期至下月底
#位置: 发现 --> 定向积分 --> 每日领积分超值兑东奥特许商品
class game_dongao:
    def run(self, client, user):
        data = {
            'from': random.choice('123456789') + ''.join(random.choice('0123456789') for i in range(10))
        }
        trance = [600,300,300,300,300,300,300]
        try:
            #领取积分奖励
            dongaoPoint = client.post('https://m.client.10010.com/welfare-mall-front/mobile/winterTwo/getIntegral/v1', data=data)
            dongaoPoint.encoding = 'utf-8'
            res1 = dongaoPoint.json()
            #查询领了多少积分
            dongaoNum = client.post('https://m.client.10010.com/welfare-mall-front/mobile/winterTwo/winterTwoShop/v1', data=data)
            dongaoNum.encoding = 'utf-8'
            res2 = dongaoNum.json()
            #领取成功
            if res1['resdata']['code'] == '0000':
                #当前为连续签到的第几天
                day = int(res2['resdata']['signDays'])
                #签到得到的积分
                point = trance[day%7] + 300 if day==1 else trance[day%7]
                logging.info('【东奥积分活动】: ' + res1['resdata']['desc'] + '，' + str(point) + '积分')
            else:
                logging.info('【东奥积分活动】: ' + res1['resdata']['desc'] + '，' + res2['resdata']['desc'])
            time.sleep(1)
        except Exception as e:
            print(traceback.format_exc())
            logging.error('【东奥积分活动】: 错误，原因为: ' + str(e))