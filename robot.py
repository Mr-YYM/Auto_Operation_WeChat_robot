import wxpy
import data_getter
import time
import logging
from threading import Thread


def send_contents(contents, member):
    if len(contents) != 0:
        print('有这么一些需要发送：\n')
        show_cts = '--------------------------------------------------------------\n'.join(contents)
        print(show_cts)

        for k, v in enumerate(contents):
            member.send(v)
            logging.error('已经发送了第{0}个'.format(k + 1))
            if k + 1 == len(contents):
                break
            time.sleep(60)
    else:
        print('nothing')


def send_news_to_groups(a_group, interval):
    times = 0
    while 1:
        times += 1
        print("☆☆群【%s】开始进行第%d轮action☆☆\n%s" % (a_group.name, times, '-' * 60))

        to_send_cts = data_getter.get_send_cts()
        print("☆☆刚刚获取了一些信息☆☆\n%s" % ('-' * 60))

        try:
            send_contents(to_send_cts, a_group)
        except wxpy.ResponseError as exp:
            if exp.err_code == 1100 or 1101 or 1102:
                print('☆☆账号异常退出，请重新登录☆☆')
            else:
                print('发生了一些错误：', exp)

        time.sleep(interval*60)


if __name__ == '__main__':
    bot = wxpy.Bot(cache_path=True)
    s_keys = {'产品': '【产品】广海互联网细分群',
              '设计': '【设计】广海互联网细分群',
              '运营': '【运营】广海互联网细分群',
              '技术': '【技术】广海互联网细分群',
              '市场': '【市场】广海互联网细分群',
              '区块链': '【区块链】广海互联网专题群',
              '福利': '【福利】广海互联网社群',
              '游戏': '【游戏】广海互联网社群',
              '资讯': '【资讯】广海互联网社群'}
    keys = {}
    for k, v in s_keys.items():
        gs = bot.search(v)
        if gs:
            keys[k] = gs[0]


    @bot.register(wxpy.Member)
    def fun(msg):
        if msg.type == wxpy.TEXT:
            if msg.text in keys.keys() and msg.sender not in keys[msg.text].members:
                print(msg)
                try:
                    keys[msg.text].add_members(msg.sender)
                except:
                    msg.sender.send('似乎无法添加进群啊！！！')
            else:
                return '你已经在群里边了吧'


    g_info = bot.search('【资讯】广海互联网社群')[0]
    g_test = bot.search('机器人测试')[0]
    # me = bot.self
    print(g_info.name)

    t = Thread(target=send_news_to_groups, args=(g_info, 15,))
    t.start()

    t2 = Thread(target=send_news_to_groups, args=(g_test, 1,))
    t2.start()
