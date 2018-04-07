import re
import wxpy
# import data_getter
import time
import logging
import threading
from threading import Thread

lock = threading.Lock()


def send_contents(contents, chat):
    """
    发送内容信息到指定的chat(聊天对象，群聊或者好友)

    :param contents:内容信息
    :param chat:聊天对象，群聊（wxpy.Group）或者好友(wxpy.Friend)
    """
    if contents:
        print('有这么一些需要发送：\n')
        show_cts = '--------------------------------------------------------------\n'.join(contents)
        print(show_cts)

        for k, v in enumerate(contents):
            try:
                chat.send(v)
                logging.error('【{name}】已经发送了第{count}个'.format(name=chat.name, count=k + 1))
            except wxpy.ResponseError as exp:
                if exp.err_code == 1100 or 1101 or 1102:
                    print('☆☆账号异常退出，请重新登录☆☆')
                else:
                    print('发生了一些错误：', exp)

                break

            if k + 1 == len(contents):
                break
            time.sleep(60)
    else:
        print('【%s】nothing' % chat.name)


def send_news_to_chat(a_chat, interval):
    """
    ☆☆ 发送新闻主函数 ☆☆

    :param a_chat: 聊天对象，群聊（wxpy.Group）或者好友(wxpy.Friend)
    :param interval: 时间间隔
    """
    times = 0
    previous_cts = []
    while 1:
        times += 1
        lock.acquire()
        try:
            print('{line}{group:^16}{line}\n{action:>45}'.format(line='↓' * 30, group=a_chat.name,
                                                                 action='☆☆开始进行第%d轮action☆☆' % times))

            if times != 1:
                previous_cts += ready_to_send_cts

            if len(previous_cts) > 60:
                previous_cts = []

            ready_to_send_cts = data_getter.get_send_cts()

            to_send_cts = [er for er in ready_to_send_cts if er not in set(previous_cts)]
            print("☆☆群【%s】刚刚获取了一些信息☆☆\n" % a_chat.name)

            send_contents(to_send_cts, a_chat)

            print('{action:>45}\n{line}{group:^16}{line}\n'.format(line='↑' * 30, group=a_chat.name,
                                                                   action='☆☆第%d轮action完成了☆☆' % times))

        finally:
            lock.release()

        time.sleep(interval * 60)


def fun():
    times = 0
    while True:
        print("Running")
        time.sleep(1800)
        times += 0.5
        print('安全运行%d小时了' % times)


if __name__ == '__main__':
    other_group_keys = """广海小米校园俱乐部:mifan
广海互联网社群(8):闲聊"""  # 自定义群关键字
    key_text = '''1.互联网人工智能群……发送"AI"
2.互联网区块链群……发送"区块链"
3.互联网电子商务群……发送"电商"
4.互联网读书兴趣群……发送"读书"
5.互联网游戏策划群……发送"游戏"
6.互联网日常福利群……发送"福利"
7.互联网编程技术群……发送"技术"
8.互联网平面设计群……发送"设计"
9.互联网产品运营群……发送"产品"
10.互联网新媒体运营群……发送"新媒体"
11.互联网市场营销群……发送"市场"
12.广海小米俱乐部……发送"mifan"
13.广海互联网闲聊群……发送"闲聊"
'''
    # 扫码登录机器人，并获取所有可识别群组
    bot = wxpy.Bot(cache_path=True, console_qr=1)
    groups = bot.groups()

    # 获取所有广海群
    mt = '【.*】广海互联网.*群'
    guanghai_groups = [each_group for each_group in groups if re.match(mt, each_group.name) is not None]

    # ↓↓↓↓↓↓------->提取入群关键字<--------↓↓↓↓↓↓
    key_mt = '【.*】'
    join_keys = {}

    for eg in guanghai_groups:
        r = re.search(key_mt, eg.name)
        if r is not None:
            join_keys[r.group()[1:-1]] = eg

    for ek in other_group_keys.split('\n'):
        g_name_key = ek.split(':')
        g = bot.search(g_name_key[0])
        if g:
            join_keys[g_name_key[1]] = g[0]

    print(join_keys)
    # ↑↑↑↑↑↑------->提取入群关键字<--------↑↑↑↑↑↑

    # ------->机器人关键字识别，待进一步实现完善，重构！<--------
    @bot.register(wxpy.Friend)
    def auto_invite(msg):
        """
        识别关键字，自动邀请好友进群

        """
        # sender：好友对象
        sender = msg.sender

        if msg.type == wxpy.TEXT:
            text = msg.text
            if text in join_keys.keys():
                group = join_keys[text]
                members = group.members  # 群所有成员的集合

                if sender not in members:
                    print(msg)
                    add_member_to_group(group, sender)
                    time.sleep(0.5)
                    return '【机器人】已经拉你进群或发送邀请，请确认！'
                else:
                    # 更新群成员列表
                    group.update_group()
                    if sender in group.members:
                        return '【机器人】你已经在群里边了吧'
                    else:
                        add_member_to_group(group, sender)

            if msg.text == '进群':
                return key_text

    # 添加好友进群
    def add_member_to_group(group, sender):
        try:
            group.add_members(sender)
        except Exception as exp:
            print(exp)
            sender.send('似乎无法添加进群啊！！！')


    # 注册好友请求类消息
    @bot.register(msg_types=wxpy.FRIENDS)
    # 自动接受验证信息中包含 'wxpy' 的好友请求
    def auto_accept_friends(msg):
        # 判断好友请求中的验证文本
        if 'wxpy' in msg.text.lower():
            # 接受好友 (msg.card 为该请求的用户对象)
            new_friend = bot.accept_friend(msg.card)
            # 或 new_friend = msg.card.accept()
            # 向新的好友发送消息
            new_friend.send('哈哈，我自动接受了你的好友请求')

    embed = Thread(target=fun)
    embed.start()


    # ↑↑↑↑↑↑------->机器人关键字识别，待进一步实现完善，重构！<--------↑↑↑↑↑↑

    # ↓↓↓↓↓↓------->当时（15min）爬取网站，自动更新数据库<--------↓↓↓↓↓↓
    # data_getter.auto_update_db(interval=60)

    # ↓↓↓↓↓↓------->创建和启动发送新闻的线程--------↓↓↓↓↓↓
    # if '资讯' in join_keys.keys():
    #     g_info = join_keys['资讯']
    #     t = Thread(target=send_news_to_chat, args=(g_info, 60,))
    #     t.start()
    #
    # if '可聊' in join_keys.keys():
    #     g_chat = join_keys['可聊']
    #     t3 = Thread(target=send_news_to_chat, args=(g_chat, 300,))
    #     t3.start()

    # g_test = bot.search('机器人测试')[0]
    #
    # t2 = Thread(target=send_news_to_chat, args=(g_test, 5,))
    # t2.start()

    # ↑↑↑↑↑↑------->创建和启动发送新闻的线程<--------↑↑↑↑↑↑
