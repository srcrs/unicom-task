# -*- coding: utf-8 -*-
# @Time    : 2021/08/14 16:30
# @Author  : srcrs
# @Email   : srcrs@foxmail.com
import requests,json,time,re,login,logging,traceback,os,random,notify,datetime
from lxml.html import fromstring

#游戏任务中心每日打卡领积分，游戏任务自然数递增至7，游戏频道每日1积分
#位置: 首页 --> 游戏 --> 每日打卡
class game_signin:
    def run(self, client, user):
        data1 = {
            'methodType': 'iOSIntegralGet',
            'gameLevel': '1',
            'deviceType': 'iOS'
        }
        try:
            client.get('https://img.client.10010.com/gametask/index.html?yw_code=&desmobile=' + user['username'] + '&version=android@8.0100')
            time.sleep(2)
            headers = {
                'origin': 'https://img.client.10010.com',
                'referer': 'https://img.client.10010.com/gametask/index.html?yw_code=&desmobile=' + user['username'] + '&version=android@8.0100'
            }
            client.headers.update(headers)
            #游戏频道积分
            gameCenter_exp = client.post('https://m.client.10010.com/producGameApp',data=data1)
            gameCenter_exp.encoding='utf-8'
            res1 = gameCenter_exp.json()
            if res1['code'] == '0000':
                logging.info('【游戏频道打卡】: 获得' + str(res1['integralNum']) + '积分')
            else:
                logging.info('【游戏频道打卡】: ' + res1['msg'])
            client.headers.pop('referer')
            client.headers.pop('origin')
            time.sleep(1)
        except Exception as e:
            print(traceback.format_exc())
            logging.error('【游戏频道打卡】: 错误，原因为: ' + str(e))
