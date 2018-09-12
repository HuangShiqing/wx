from wxpy import *

Gb_senter = list()
Gb_receive = 0
Gb_step = 0
Gb_temp = None

# 初始化机器人，扫码登陆
bot = Bot()
found = bot.friends().search('新号')
master = ensure_one(found)
message = bot.messages


# 转发消息
@bot.register(chats=Friend)
def forward(msg):
    if msg.sender not in Gb_senter:
        Gb_senter.append(msg.sender)
    msg.forward(master, msg.sender, '代号:' + str(Gb_senter.index(msg.sender)))


@bot.register(master)
def receive_cmd(msg):
    global Gb_senter
    global Gb_receive
    global Gb_step
    global Gb_temp

    if Gb_step == 0:
        #     print(msg)
        text = msg.text
        #     如果是数字，则认为是修改接受对象的cmd
        if text.isdigit():
            Gb_receive = int(text)
            if int(text) < len(Gb_senter):
                master.send('当前接受者为:' + str(Gb_receive))
            else:
                master.send('越界了')
        #     拉取当前人物列表
        elif text == 'List':
            master.send(Gb_senter)
            master.send('当前:' + str(Gb_receive))
        #         清除人物列表
        elif text == 'Clear':
            Gb_senter = list()
            Gb_receive = 0
            master.send('Clear Ok')
        #     查找聊天对象
        elif text[0:6] == 'Search':
            found = bot.friends().search(text[7:])
            if len(found) == 0:
                master.send('No Found')
            if len(found) == 1:
                friend = found[0]
                if friend not in Gb_senter:
                    Gb_senter.append(friend)
                    Gb_receive = len(Gb_senter) - 1
                else:
                    Gb_receive = Gb_senter.index(friend)
                master.send(Gb_senter)
                master.send('当前:' + str(Gb_receive))
            else:
                master.send(found)
                Gb_temp = found
                Gb_step = 1
        else:
            msg.forward(Gb_senter[Gb_receive])
    else:
        text = msg.text
        if Gb_step == 1:
            friend = Gb_temp[int(text)]
            if friend not in Gb_senter:
                Gb_senter.append(friend)
                Gb_receive = len(Gb_senter) - 1
            else:
                Gb_receive = Gb_senter.index(friend)
            master.send(Gb_senter)
            master.send('当前:' + str(Gb_receive))


embed()
