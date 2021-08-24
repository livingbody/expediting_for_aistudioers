# 一、在线催稿系统
Aistudio地址[https://aistudio.baidu.com/aistudio/projectdetail/2307495](https://aistudio.baidu.com/aistudio/projectdetail/2307495)

# 二、主机申请
**免费云主机、数据库申请：**
[https://activity.huaweicloud.com/free_test/index.html?ticket=ST-1062828-tac3TOvziy1tfRkSfmBcYPDl-sso](https://activity.huaweicloud.com/free_test/index.html?ticket=ST-1062828-tac3TOvziy1tfRkSfmBcYPDl-sso)

![](https://ai-studio-static-online.cdn.bcebos.com/1c2aa0255193484ba3737dfc355efc0d454eb60a870a42f4801efcdca68beec3)

![](https://ai-studio-static-online.cdn.bcebos.com/59a8272da9074cf78949dd27deeb5976f59459df75324a21bad4371d0b124dd3)


# 三、docker安装配置
```
apt install docker.io
# 可以使用加速
docker login --username=ji***********@mail.com registry.cn-qingdao.aliyuncs.comPassword: 
docker pull wechaty/wechaty:latest& 
```

![](https://ai-studio-static-online.cdn.bcebos.com/ff410db704564fcbb0d3ae924d35df2e6f45f760c54943c891b817fb9eebfbc6)

![](https://ai-studio-static-online.cdn.bcebos.com/a0468e750f834205bd0d3b46e4d84949d40aecad811a493c8e5efc9bfed2a5a6)



# 四、python环境配置
## 1.下载miniconda
打开[https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/](https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/)，查找适合的安装包

地址： [https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-py37_4.9.2-Linux-x86_64.sh](https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-py37_4.9.2-Linux-x86_64.sh)

![](https://ai-studio-static-online.cdn.bcebos.com/6e5db6d4072f4fd58bd3deab48aa2780d82e78babef24eb3ae99e7664e14f67f)

## 2.安装
默认安装即可

```
bash Miniconda3-py37_4.9.2-Linux-x86_64.sh
source .bashrc
```

## 3.软件包安装
地址：[https://tuna.moe/oh-my-tuna/](https://tuna.moe/oh-my-tuna/)

![](https://ai-studio-static-online.cdn.bcebos.com/1468f6933d544a358bc4de0f75f8b0706b895549ec124215866b7c49b4e9eae6)

```
#修改conda源加速下载
python oh-my-tuna.py
创建虚拟环境
conda create -n p2 python=3.7
```

```
#修改pip源加速下载
conda activate p2
(base) root@hecs-x-medium-2-linux-20210824111228:~# python oh-my-tuna.py 
[pypi]: Activating...
[pypi]: Mirror has been activated
[Anaconda]: Activating...
[Anaconda]: Mirror has been activated
(base) root@hecs-x-medium-2-linux-20210824111228:~# 

pip install paddlepaddle
pip install paddlehub
pip install wechaty
```

![](https://ai-studio-static-online.cdn.bcebos.com/f1422e1d404f4772866831bb93f143f7e62d46ab89624260a9998707690a79a3)

## 4.环境变量配置
修改用户目录下.bashrc文件，添加下面内容
```
export WECHATY_LOG="verbose"
export WECHATY_PUPPET="wechaty-puppet-wechat"
export WECHATY_PUPPET_SERVER_PORT="8080"
export WECHATY_TOKEN="puppet_padlocal_2e352aac*******替换位自己的token******"
```
## 5.环境验证
```
(p2) root@hecs-x-medium-2-linux-20210824111228:~# pip list|grep paddle
paddle2onnx                       0.7
paddlehub                         2.1.0
paddlenlp                         2.0.8
paddlepaddle                      2.1.2
(p2) root@hecs-x-medium-2-linux-20210824111228:~# pip list|grep wechaty
wechaty                           0.8.16
wechaty-grpc                      0.20.19
wechaty-puppet                    0.3.dev10
wechaty-puppet-service            0.8.5

```
## 6.启动docker
启动过程中会有二维码链接出现，需要手动打开扫码

 `docker run -ti --name wechaty_puppet_service_token_gateway --rm -e WECHATY_LOG -e WECHATY_PUPPET -e WECHATY_TOKEN -e WECHATY_PUPPET_SERVER_PORT -p "$WECHATY_PUPPET_SERVER_PORT:$WECHATY_PUPPET_SERVER_PORT" wechaty/wechaty:latest`

 ![](https://ai-studio-static-online.cdn.bcebos.com/f3a968a0f0d44680a068651b8c0a46a024ce73e9e48f4983b2f212516355699f)


# 五、代码实现

## 1.安装apscheduler 定时框架
```
pip install apscheduler
```

## 2.催稿
```

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

```

## 3.每天报送“一刻”节目
```

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
```

## 4.收稿
```
    # '投稿：' 激活收项目
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
            # 保存项目到xm.txt文件
            f = open('xm.txt', 'a')
            f.write(text.strip('投稿：') + '\n')
            f.close()
```

## 5.定时调度
**此处测试用，所以时间间隔设置很小，有关时间设置建议参照apscheduler框架说明，很简单**

```

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
```

# 六、后续计划
后续拟采用mysql存储配置、存储项目，采用simpleui作为管理，并引入规则对发广告行为进行检测，发现就自动TTT，大家觉得怎样？
