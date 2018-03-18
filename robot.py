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
            previous_cts = ready_to_send_cts

        ready_to_send_cts = data_getter.get_send_cts()

        to_send_cts = [er for er in ready_to_send_cts if er not in previous_cts]
        print("☆☆群【%s】刚刚获取了一些信息☆☆\n" % a_group.name)

        send_contents(to_send_cts, a_group)

        time.sleep(interval * 60)


if __name__ == '__main__':
    # ------->机器人关键字识别，待进一步实现完善，重构！<--------
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

    print(keys)


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
