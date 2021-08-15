# -*- coding: utf-8 -*-
# @Time    : 2021/08/14 16:30
# @Author  : srcrs
# @Email   : srcrs@foxmail.com
import requests,json,time,re,login,logging,traceback,os,random,notify,datetime,util
from lxml.html import fromstring

#沃之树任务
#位置: 首页 --> 游戏 --> 沃之树
class wo_tree:
    def run(self, client, user):
        #领取4M流量*3
        try:
            flowList = self.get_woTree_glowList(client)
            num = 1
            for flow in flowList:
                #这里会请求很长时间，发送即请求成功
                flag = False
                try:
                    takeFlow = client.get('https://m.client.10010.com/mactivity/flowData/takeFlow.htm?flowId=' + flow['id'], timeout=1)
                except Exception as e:
                    flag = True
                    logging.info('【沃之树-领流量新】: 4M流量 x' + str(num))
                #等待1秒钟
                time.sleep(1)
                num = num + 1
                if flag:
                    continue
                takeFlow.encoding='utf-8'
                res1 = takeFlow.json()
                if res1['code'] == '0000':
                    logging.info('【沃之树-领流量】: 4M流量 x' + str(num))
                else:
                    logging.info('【沃之树-领流量】: 已领取过 x' + str(num))
                #等待1秒钟
                time.sleep(1)
                num = num + 1
            client.post('https://m.client.10010.com/mactivity/arbordayJson/getChanceByIndex.htm?index=0')
            #浇水
            grow = client.post('https://m.client.10010.com/mactivity/arbordayJson/arbor/3/0/3/grow.htm')
            grow.encoding='utf-8'
            res2 = grow.json()
            logging.info('【沃之树-浇水】: 获得' + str(res2['data']['addedValue']) + '培养值')
            time.sleep(1)
        except Exception as e:
            print(traceback.format_exc())
            logging.error('【沃之树】: 错误，原因为: ' + str(e))

    #获取沃之树首页，得到领流量的目标值
    def get_woTree_glowList(self, client):
        index = client.post('https://m.client.10010.com/mactivity/arbordayJson/index.htm')
        index.encoding='utf-8'
        res = index.json()
        output = res['data']['flowChangeList']
        output += res['data']['shareFlowChangeList']
        return output
