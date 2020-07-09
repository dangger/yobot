'''
自定义功能：

在这里可以编写自定义的功能，
编写完毕后记得 git commit，

这个模块只是为了快速编写小功能，如果想编写完整插件可以使用：
https://github.com/richardchien/python-aiocqhttp
或者
https://github.com/richardchien/nonebot

关于PR：
如果基于此文件的PR，请在此目录下新建一个`.py`文件，并修改类名
然后在`yobot.py`中添加`import`（这一步可以交给仓库管理者做）
'''

import asyncio
from typing import Any, Dict, Union
import requests
from aiocqhttp.api import Api
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from quart import Quart
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
import datetime

headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'DNT': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'Content-Type': 'application/json',
    'Origin': 'https://kengxxiao.github.io',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://kengxxiao.github.io/Kyouka/',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,zh-TW;q=0.6',
}

data = '{"history":0,"clanName":"\u58A8\u6C60\u82D1"}'
class clan_rank:
    Passive = False
    Active = True
    Request = False
    def __init__(self, glo_setting: dict, *args, **kwargs):
        '''
        初始化，只在启动时执行一次

        参数：
            glo_setting 包含所有设置项，具体见default_config.json
            bot_api 是调用机器人API的接口，具体见<https://python-aiocqhttp.cqp.moe/>
            scheduler 是与机器人一同启动的AsyncIOScheduler实例
            app 是机器人后台Quart服务器实例
        '''
        # 注意：这个类加载时，asyncio事件循环尚未启动，且bot_api没有连接
        # 此时不要调用bot_api
        # 此时没有running_loop，不要直接使用await，请使用asyncio.ensure_future并指定loop=asyncio.get_event_loop()

        # 如果需要启用，请注释掉下面一行
        # return

        # 这是来自yobot_config.json的设置，如果需要增加设置项，请修改default_config.json文件
        self.setting = glo_setting

        # 这是cqhttp的api，详见cqhttp文档
        #self.api = bot_api

        # # 注册定时任务，详见apscheduler文档
        # @scheduler.scheduled_job('cron', hour='8-23', minute="*")
        async def get_clan_rank():
            print("开始查询公会战排名...")
            response = await requests.post('https://service-kjcbcnmw-1254119946.gz.apigw.tencentcs.com/name/0', headers=headers, data=data.encode('utf-8'))
            sub_groups = self.setting.get("notify_groups", [])
            if response.json()["code"] == 0:
                send_message = "当前公会战排名为:第"+str(response.json()['data'][0]['rank'])+"名"
                print(send_message)
                for group in sub_groups:
                    self.api.send_group_msg(group_id=group, message=send_message)
            else:
                print("请求公会战排名失败！")
                print(response.text())

        # # 注册web路由，详见flask与quart文档
        # @app.route('/is-bot-running', methods=['GET'])
        # async def check_bot():
        #     return 'yes, bot is running'
    def jobs(self):
        trigger = CronTrigger(hour="5-23", minute="*")
        job = (trigger, self.get_clan_rank)
        init_trigger = DateTrigger(
            datetime.datetime.now() +
            datetime.timedelta(seconds=5)
        )  # 启动5秒后初始化
        init_job = (init_trigger, self.send_clan_rank)
        return (job, init_job)
    async def execute_async(self, ctx: Dict[str, Any]) -> Union[None, bool, str]:
        '''
        每次bot接收有效消息时触发

        参数ctx 具体格式见：https://cqhttp.cc/docs/#/Post
        '''
        # 注意：这是一个异步函数，禁止使用阻塞操作（比如requests）

        # 如果需要使用，请注释掉下面一行
        return

        cmd = ctx['raw_message']
        if cmd == '你好':

            # 调用api发送消息，详见cqhttp文档
            await self.api.send_private_msg(
                user_id=123456, message='收到问好')

            # 返回字符串：发送消息并阻止后续插件
            return '世界'

        # 返回布尔值：是否阻止后续插件（返回None视作False）
        return False
