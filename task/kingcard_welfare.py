# -*- coding: utf-8 -*-
# @Time    : 2021/08/14 16:30
# @Author  : srcrs
# @Email   : srcrs@foxmail.com
import requests,json,time,re,login,logging,traceback,os,random,notify,datetime,util
from lxml.html import fromstring

#自动续约王卡福利二选一 每个月3次
class kingcard_welfare:
    def run(self, client, user):
        if 'autoKingCardType' not in user:
            return False
        #获取当前是本月几号
        now = util.getTimezone()
        timeArray = time.localtime(now)
        day = time.strftime("%d",timeArray)
        url = "https://m.client.10010.com/mobileService/businessTransact/tencentCardUpgradeChg.htm"
        data = {
            'upgradeType': user['autoKingCardType']
        }
        #每月3号领取
        if day=="2" or day=="3" or day=="4":
            stat = client.post(url,data=data)
            stat.encoding = 'utf-8'
            stat = stat.json()
            try:
                if stat['msg'] == 'ok':
                    if len(stat['content']) != 0:
                        logging.info('【王卡福利续约】: 成功, ' + stat['content'])
                    else:
                        logging.info('【王卡福利续约】: 失败')
                else:
                    logging.info('【王卡福利续约】: 失败, ' + stat['msgStr'])
            except Exception as e:
                print(traceback.format_exc())
                logging.error('【王卡福利续约】: 错误, ' + stat['msgStr'])