# 功能

- 沃之树领流量、浇水(12M日流量)
- 每日签到(1积分+翻倍4积分+第七天1G流量日包)
- 天天抽奖，每天三次免费机会(随机奖励)
- 游戏中心每日打卡(连续打卡，积分递增至最高7，第七天1G流量日包)
- 每日领取100定向积分
- 积分抽奖，每天最多抽30次(中奖几率渺茫)
- 冬奥积分活动(第1和7天，可领取600定向积分，其余领取300定向积分,有效期至下月底)
- 获取每日1G流量日包(截止日期暂时不知道)
- 增加沃邮箱签到，连续签到可获得话费奖励（需绑定沃邮箱公众号）
- 邮件、钉钉、Tg、企业微信等推送运行结果

# 使用方法

## docker

在当前文件夹创建config.json，用于存储账户信息。

```bash
#步骤1
docker run -itd \
  -v $PWD/config.json:/root/config.json \
  --name unicom-task \
  --restart always \
  srcrs/unicom-task
#步骤2
docker exec unicom-task /bin/bash -c 'service cron start'
```

## docker-compose

更改unicom-task/config/config.json

```bash
docker-compose up -d
```

完成上述操作后，容器中每天会自动跑两个脚本，一个会在6:30的时候自动执行任务，一个会在5:00自动更新最新代码。

## 腾讯云函数

已经对云函数有过了解，并且已在腾讯云开通过云函数功能。

### 通过yaml文件

需要本地具备npm环境

- git clone https://github.com/srcrs/unicom-task.git

- npm install -g serverless

- cd ./UnicomTask-docker/serverless/tencent-scf

- sls deploy --debug

- 微信扫码登陆

- 进入到unicom-Task容器中，在config.json填写账号信息，点击测试，手动运行一次，如果能够正常运行就说明部署成功。


### 通过zip包

1. 在[releases](http://github.com/srcrs/UnicomTask-docker/releases/latest)下载最新的unicomtask-tenscf.zip包

2. 进入 [创建自定义云函数](https://console.cloud.tencent.com/scf/list-create?rid=1&ns=default&functionName=helloworld-1621082690&createType=empty)

3. 必要配置
  - (1) 函数代码 --> 选择本地上传zip包 --> 上传unicomtask-tenscf.zip
  - (2) 高级配置 --> 环境配置 --> 执行超时时间设置为 900
  - (3) 触发器配置 --> 自定义创建 --> 触发周期 --> 自定义出发周期 --> Cron表达式 --> `0 30 6 * * * *`

4. 点击完成。最后，进入到刚才创建的云函数，找到config.json填写账号信息，点击测试，手动运行一次，如果能够正常运行就说明部署成功。
>注：最后一步在config.json填写账号信息，也可以先把unicomtask-tenscf.zip解压，待config.json信息完善后，再进行压缩。就不用在第4步完善测试了。

### 通过脚本一键部署
需要本地具备 npm 环境
- Clone 本项目
 ```git clone https://github.com/srcrs/unicom-task.git```
- 进入该项目
 ```cd unicom-task```
- 修改 ```config``` 文件夹中的 ```config.conf``` 为你的账号信息
```
[
    {
        "username": "1390000000",
        "password": "000000",
        "appId": "00000000000000000"
    },
    {
        "username": "13333333333",
        "password": "000000",
        "appId": "00000000000000000"
    }
]
```
- 赋予脚本可执行权限
 ```chmod +x ./serverless/local_deploy.sh```
- 运行脚本 
  ```./serverless/local_deploy.sh```
- 扫码或网页登录腾讯云
- 完成部署
