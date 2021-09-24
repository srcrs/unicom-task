import requests,logging,urllib.parse

class email_task:
    def dotask(self, email):
        msg = ""
        try:
            url = "https://nyan.mail.wo.cn/cn/sign/user/checkin.do?rand=0.913524814493383"
            res = email.post(url=url).json()
            result = res.get("result")
            if result == -2:
                msg += "【沃邮箱签到】: 已签到\n"
            elif result is None:
                msg += f"【沃邮箱签到】: 签到失败\n"
            else:
                msg += f"【沃邮箱签到】: 签到成功~已签到{result}天！\n"
        except Exception as e:
            print("沃邮箱签到错误", e)
            msg += "沃邮箱签到错误\n"
        try:
            url = "https://nyan.mail.wo.cn/cn/sign/user/doTask.do?rand=0.8776674762904109"
            data_params = {
                "沃邮箱每日首次登录": {"taskName": "loginmail"},
                "浅秋领福利": {"taskName": "clubactivity"},
                "下载沃邮箱app": {"taskName": "download"},
                "去用户俱乐部逛一逛": {"taskName": "club"},
            }
            for key, data in dict.items(data_params):
                try:
                    res = email.post(url=url, data=data).json()
                    result = res.get("result")
                    if result == 1:
                        msg += f"【{key}】: 做任务成功\n"
                    elif result == -1:
                        msg += f"【{key}】: 任务已做过\n"
                    elif result == -2:
                        msg += f"【{key}】: 请检查登录状态\n"
                    else:
                        msg += f"【{key}】: 未知错误\n"
                except Exception as e:
                    print(f"沃邮箱执行任务【{key}】错误", e)
                    msg += f"沃邮箱执行任务【{key}】错误"
        except Exception as e:
            print("沃邮箱执行任务错误", e)
            msg += "沃邮箱执行任务错误错误"
        logging.info(msg)
    def run(self, client, user):
        if "woEmail" not in user:
            return False
        email = requests.Session()
        headers = {
            'Host': 'nyan.mail.wo.cn',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.7(0x18000733) NetType/WIFI Language/zh_CN',
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }

        query = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(user['woEmail']).query))
        params = (
            ('mobile', query['mobile'].replace(' ', '+')),
            ('userName', ''),
            ('openId', query['openId'].replace(' ', '+')),
        )
        email.get('https://nyan.mail.wo.cn/cn/sign/index/index', headers=headers, params=params)
        self.dotask(email)
