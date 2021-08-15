# -*- coding: utf-8 -*-
# @Time    : 2021/08/14 16:30
# @Author  : srcrs
# @Email   : srcrs@foxmail.com
import requests,json,time,re,login,logging,traceback,os,random,notify,datetime
from lxml.html import fromstring

#每日签到，1积分 ，第七天得到 1G 日包
#位置: 我的 --> 我的金币
class daily_daysign:
    def run(self, client, user):
        try:
            #参考同类项目 HiCnUnicom 待明日验证是否能加倍成功
            client.headers.update({'referer': 'https://img.client.10010.com/activitys/member/index.html'})
            param = 'yw_code=&desmobile=' + user['username'] + '&version=android@$8.0100'
            client.get('https://act.10010.com/SigninApp/signin/querySigninActivity.htm?' + param)
            client.headers.update({'referer': 'https://act.10010.com/SigninApp/signin/querySigninActivity.htm?' + param})
            daySign = client.post('https://act.10010.com/SigninApp/signin/daySign')
            daySign.encoding='utf-8'
            #本来是不想加这个的，但是会出现加倍失败的状况，暂时加上也是有可能出问题
            client.post('https://act.10010.com/SigninApp/signin/todaySign')
            client.post('https://act.10010.com/SigninApp/signin/addIntegralDA')
            client.post('https://act.10010.com/SigninApp/signin/getContinuous')
            client.post('https://act.10010.com/SigninApp/signin/getIntegral')
            client.post('https://act.10010.com/SigninApp/signin/getGoldTotal')
            client.headers.pop('referer')
            res = daySign.json()
            if res['status'] == '0000':
                logging.info('【每日签到】: ' + '打卡成功')
            elif res['status'] == '0002':
                logging.info('【每日签到】: ' + res['msg'])
            time.sleep(1)
        except Exception as e:
            print(traceback.format_exc())
            logging.error('【每日签到】: 错误，原因为: ' + str(e))