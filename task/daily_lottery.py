# -*- coding: utf-8 -*-
# @Time    : 2021/08/14 16:30
# @Author  : srcrs
# @Email   : srcrs@foxmail.com
import requests,json,time,re,login,logging,traceback,os,random,notify,datetime,util
from lxml.html import fromstring

#天天抽奖
#我的 --> 我的金币 --> 天天抽好礼
class daily_lottery:
    def run(self, client, user):
        try:
            numjsp = util.get_encryptmobile(client)
            #加上这一堆，看中奖率会不会高点
            client.post('https://m.client.10010.com/mobileservicequery/customerService/share/defaultShare.htm')
            client.get('https://m.client.10010.com/dailylottery/static/doubleball/firstpage?encryptmobile=' + numjsp)
            client.get('https://m.client.10010.com/dailylottery/static/outdailylottery/getRandomGoodsAndInfo?areaCode=076')
            client.get('https://m.client.10010.com/dailylottery/static/active/findActivityInfo?areaCode=076&groupByType=&mobile=' + numjsp)
            for i in range(3):
                luck = client.post('https://m.client.10010.com/dailylottery/static/doubleball/choujiang?usernumberofjsp=' + numjsp)
                luck.encoding='utf-8'
                res = luck.json()
                logging.info('【天天抽奖】: ' + res['RspMsg'] + ' x' + str(i+1))
                #等待1秒钟
                time.sleep(5)
        except Exception as e:
            print(traceback.format_exc())
            logging.error('【天天抽奖】: 错误，原因为: ' + str(e))
