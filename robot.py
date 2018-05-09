import datetime
import re
import warnings
import wxpy
import data_getter
import time
import logging
import threading
from threading import Thread

lock = threading.Lock()
warnings.filterwarnings('ignore')


def is_time(hour, minute):
    current_time = datetime.datetime.now().time()
    return current_time.hour == hour and current_time.minute == minute


def send_contents(content, chat):
    """
    发送内容信息到指定的chat(聊天对象，群聊或者好友)

    :param content:内容信息
    :param chat:聊天对象，群聊（wxpy.Group）或者好友(wxpy.Friend)
    """
    try:
        chat.send(content)
    except wxpy.ResponseError as exp:
        if exp.err_code == 1100 or 1101 or 1102:
            logging.error('☆☆账号异常退出，请重新登录☆☆')
        else:
            logging.error('发生了一些错误：', exp)


def send_news_to_chat(a_chat):
    """
    ☆☆ 发送新闻主函数 ☆☆

    :param a_chat: 聊天对象，群聊（wxpy.Group）或者好友(wxpy.Friend)
    """
    times = 0
    while 1:
        lock.acquire()
        try:
            if is_time(7, 0):
                times += 1
                logging.info('{line}{group:^16}{line}\n{action:>45}'.format(line='↓' * 30, group=a_chat.name,
                                                                            action='☆☆开始进行第%d轮的早报推送☆☆' % times))

                to_send_cts = '校友会早间新闻：\n' + data_getter.get_send_cts(12)

                logging.info("☆☆已经为群【%s】获取了早报信息☆☆\n" % a_chat.name)

                send_contents(to_send_cts, a_chat)

                logging.info('{action:>45}\n{line}{group:^16}{line}\n'.format(line='↑' * 30, group=a_chat.name,
                                                                              action='☆☆第%d轮的早报推送完成了☆☆' % times))

        finally:
            lock.release()

        time.sleep(60)


if __name__ == '__main__':
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    logging.getLogger("requests").setLevel(logging.ERROR)
    logging.getLogger("wxpy").setLevel(logging.WARNING)

    key_text = '''【读书】广海互联网社群
    KW：读书
【游戏】广海互联网社群
    KW：游戏
【福利】广海互联网社群
    KW：福利
【比赛】广海互联网社群
    KW：比赛
【共创】广海共创者社群
    KW：共创
【区块链】广海互联网社群
    KW：区块链
【小程序】广海互联网社群
    KW：小程序
【电商】广海互联网社群
    KW：电商
【AI】广海互联网社群
    KW：AI
【新媒体】广海互联网社群
    KW：新媒体
【市场】广海互联网社群
    KW：市场
【资讯】广海互联网社群
    KW：资讯
【H5】广海互联网社群
    KW：H5
【设计】广海互联网社群
    KW：设计

【小米】广海小米俱乐部
    KW：小米

【前端】广海互联网社群
    KW：前端
【JAVA】广海互联网社群
    KW：JAV
【PHP】广海互联网社群
    KW：PHP
【算法】广海互联网社群
    KW：算法
【C++】广海互联网社群
    KW：C++
【安卓】广海互联网社群
    KW：安卓
【python】广海互联网社群
    KW：python
【产品】广海互联网社群
    KW：产品
【技术】广海互联网社群
    KW：技术
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
            join_keys[r.group()[1:-1].lower()] = eg

    for ek in join_keys.items():
        print(ek)

    # ↑↑↑↑↑↑------->提取入群关键字<--------↑↑↑↑↑↑

    # ------->机器人关键字识别，待进一步实现完善，重构！<--------
    @bot.register(wxpy.Friend)
    def auto_invite(msg):
        """
        识别关键字，自动邀请好友进群

        """
        request_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')  # 获取请求发出的时间（'20XX-XX-XX XX:XX'）

        # sender：好友对象
        sender = msg.sender

        if msg.type == wxpy.TEXT:
            text = msg.text.lower()
            if text in join_keys.keys():
                group = join_keys[text]
                members = group.members  # 群所有成员的集合

                if sender not in members:
                    if add_member_to_group(group, sender):
                        logging.info('%s 邀请了%s进群【%s】' % (request_time, msg.sender.name, group.name))
                        time.sleep(0.5)
                        return '【机器人】已经拉你进群或发送邀请，请确认！'
                else:
                    # 更新群成员列表
                    group.update_group()
                    if sender in group.members:
                        logging.info('%s 尝试邀请%s进群【%s】但Ta已经在群里了' % (request_time, msg.sender.name, group.name))
                        return '【机器人】你已经在群里边了吧'
                    else:
                        if add_member_to_group(group, sender):
                            logging.info('%s 邀请了%s进群【%s】' % (request_time, msg.sender.name, group.name))
                            time.sleep(0.5)
                            return '【机器人】已经拉你进群或发送邀请，请确认！'

            if msg.text == '进群':
                logging.info('%s %s发送了‘进群’指令' % (request_time, msg.sender.name))
                return key_text


    # 添加好友进群
    def add_member_to_group(group, sender):
        try:
            group.add_members(sender)
            return True
        except Exception as exp:
            print(exp)
            sender.send('似乎无法添加进群啊！！！')
            return False


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


    # ↑↑↑↑↑↑------->机器人关键字识别，待进一步实现完善，重构！<--------↑↑↑↑↑↑

    # ↓↓↓↓↓↓------->定时（60min）爬取网站，自动更新数据库<--------↓↓↓↓↓↓
    data_getter.auto_update_db(interval=60)

    # ↓↓↓↓↓↓------->创建和启动发送新闻的线程--------↓↓↓↓↓↓
    # if '资讯' in join_keys.keys():
    #     g_info = join_keys['资讯']
    #     t = Thread(target=send_news_to_chat, args=(g_info,))
    #     t.start()

    g_xiaoyou2 = bot.search('NO.2【深圳市广东海洋大学校友会】')
    if g_xiaoyou2:
        g_xiaoyou2 = g_xiaoyou2[0]

        print('找到了No.2校友群')
        t2 = Thread(target=send_news_to_chat, args=(g_xiaoyou2,))
        t2.start()
    else:
        print('没找到No.2校友群')

    g_xiaoyou3 = bot.search('NO.3深圳市广东海洋大学校友会')
    if g_xiaoyou3:
        g_xiaoyou3 = g_xiaoyou3[0]

        print('找到了No.3校友群')
        t3 = Thread(target=send_news_to_chat, args=(g_xiaoyou3,))
        t3.start()
    else:
        print('没找到No.3校友群')

    g_test = bot.search('机器人测试')
    if g_test:
        g_test = g_test[0]
        print('找到了机器人测试')
        t4 = Thread(target=send_news_to_chat, args=(g_test,))
        t4.start()
    else:
        print('没找到机器人测试')

    # ↑↑↑↑↑↑------->创建和启动发送新闻的线程<--------↑↑↑↑↑↑
