# -*- coding: utf-8 -*-
import os
import sys, urllib, json
import urllib.request
import asyncio
from typing import Optional, Union
from wechaty import Wechaty, Contact, Room
from wechaty.user import Message
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from wechaty import (
    Contact,
    FileBox,
    Message,
    Wechaty,
    ScanStatus,
)

APIKEY = '**************天行key************'


class MyBot(Wechaty):

    def __init__(self):
        super().__init__()
        self.busy = False
        self.auto_reply_comment = "Automatic Reply: I cannot read your message because I'm busy now, will talk to you when I get back."

    async def on_message(self, msg: Message):
        """back on message"""
        from_contact = msg.talker()
        text = msg.text()
        room = msg.room()
        conversation: Union[
            Room, Contact] = from_contact if room is None else room
        if text.startswith('#投稿：'):
            await conversation.ready()
            await conversation.say('项目已收，谢谢！')
            f = open('xm.txt', 'a')
            f.write(text + '\n')
            f.close()


    async def on_login(self, contact: Contact):
        print(f'user: {contact} has login')


bot: Optional[MyBot] = None
global one_words
global one_picture


# 催稿
async def expediting(bot: Wechaty):
    """
    找到作者群、或者直接找作者
    """
    # room = bot.Room.load('room-id')
    # room= await bot.Room.find({'wechatyabc'})
    room = await bot.Room.find('wechatyabc')

    await room.ready()
    file_box_zuoye = FileBox.from_file('zuoye.jpg')
    await room.say(file_box_zuoye)
    await room.say(f'家人们，周三了，交项目了！！！')


# 一刻下载
async def download_one():
    global one_words
    global one_picture
    url = 'http://api.tianapi.com/txapi/one/index?key=' + APIKEY
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    content = json.loads(resp.read())
    print(content)
    if (content):
        words = content['newslist'][0]['word']
        print(words)
        img_url = content['newslist'][0]["imgurl"]
        local = str(content['newslist'][0]["oneid"]) + '.jpg'
        # urllib.request.urlretrieve(img_url, local)
        one_words = words
        one_picture = img_url


# 一刻发送
async def send_one(bot: Wechaty):
    """
    找到发送对象（微信群或者微信号）
    """
    global one_words
    global one_picture
    room = await bot.Room.find('wechatyabc')
    await room.ready()
    # file_box_one = FileBox.from_file(one_picture)
    print(one_picture)
    print(one_words)
    file_box_one = FileBox.from_url(one_picture, name='one.jpg')
    await room.say(file_box_one)
    await room.say(f'{one_words}   {datetime.now()}')


async def main():
    """程序入口"""
    if 'WECHATY_PUPPET_SERVICE_TOKEN' not in os.environ:
        print('''
            Error: WECHATY_PUPPET_SERVICE_TOKEN 没有设置
        ''')

    global bot
    bot = MyBot()
    await download_one()
    scheduler = AsyncIOScheduler()
    # 催稿
    scheduler.add_job(expediting, 'cron', hour='0', minute='*/1', args=[bot])
    # 每天报送一刻消息
    scheduler.add_job(send_one, 'cron', hour='0', minute='*/1', args=[bot])
    # 每天爬取一刻消息
    scheduler.add_job(download_one, 'cron', hour='00', minute='00', second='00')
    # 交稿
    # 待续
    scheduler.start()
    await bot.start()


asyncio.run(main())
