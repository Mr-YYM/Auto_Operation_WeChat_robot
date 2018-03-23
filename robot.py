import re
import wxpy
import data_getter
import time
import logging
from threading import Thread


def send_contents(contents, member):
    if contents:
        print('有这么一些需要发送：\n')
        show_cts = '--------------------------------------------------------------\n'.join(contents)
        print(show_cts)

        for k, v in enumerate(contents):
            try:
                member.send(v)
                logging.error('【{name}】已经发送了第{count}个'.format(name=member.name, count=k + 1))
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
        print('【%s】nothing' % member.name)


def send_news_to_groups(a_group, interval):
    times = 0
    previous_cts = []
    while 1:
        times += 1
        print('{line}{group:^16}{line}\n{action:>45}'.format(line='-' * 30, group=a_group.name,
                                                             action='开始进行第%d轮action' % times))

        if times != 1:
            previous_cts += ready_to_send_cts

        if len(previous_cts) > 20:
            previous_cts = []

        ready_to_send_cts = data_getter.get_send_cts()

        to_send_cts = [er for er in ready_to_send_cts if er not in set(previous_cts)]
        print("☆☆群【%s】刚刚获取了一些信息☆☆\n" % a_group.name)

        send_contents(to_send_cts, a_group)

        time.sleep(interval * 60)


if __name__ == '__main__':
    key_text = '''【产品】广海互联网细分群：产品
【设计】广海互联网细分群：设计
【运营】广海互联网细分群：运营
【技术】广海互联网细分群：技术
【市场】广海互联网细分群：市场
【区块链】广海互联网主题群：区块链
【福利】广海互联网社群：福利
【游戏】广海互联网社群：游戏
【资讯】广海互联网社群：资讯
'''
    # ------->机器人关键字识别，待进一步实现完善，重构！<--------
    bot = wxpy.Bot(cache_path=True)
    groups = bot.groups()

    mt = '【.*】广海互联网.*群'
    guanghai_groups = [each_group for each_group in groups if re.match(mt, each_group.name) is not None]

    key_mt = '【.*】'
    join_keys = {}

    for eg in guanghai_groups:
        r = re.search(key_mt, eg.name)
        if r is not None:
            join_keys[r.group()[1:-1]] = eg

    print(join_keys)


    @bot.register(wxpy.Friend)
    def fun(msg):
        if msg.type == wxpy.TEXT:
            if msg.text in join_keys.keys():
                    if msg.sender not in join_keys[msg.text].members:
                        print(msg)
                        try:
                            join_keys[msg.text].add_members(msg.sender)
                        except:
                            msg.sender.send('似乎无法添加进群啊！！！')
                    elif msg.sender in join_keys[msg.text].members:
                        return '你已经在群里边了吧'

            if msg.text == '关键字':
                return key_text


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

    # ↑↑↑↑------->机器人关键字识别，待进一步实现完善，重构！<--------↑↑↑↑

    g_info = bot.search('【资讯】广海互联网社群')[0]
    g_test = bot.search('机器人测试')[0]
    # me = bot.self
    print(g_info.name)

    data_getter.auto_update_db(interval=15)

    t = Thread(target=send_news_to_groups, args=(g_info, 10, ))
    t.start()

    t2 = Thread(target=send_news_to_groups, args=(g_test, 1, ))
    t2.start()
