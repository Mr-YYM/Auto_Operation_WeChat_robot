import wxpy
import data_getter
import db_process
import time
import logging


def get_send_contents(amount=None):
    contents = data_getter.read_contents_from_readhub()
    add_cont = db_process.get_addition_contents(contents)
    send_cts = []
    for title, v in add_cont.items():
        send_cts.append('【%s】\n%s\n%s\n' % (title, v['content'], v['link']))

    if amount is None or len(send_cts) < amount:
        return send_cts
    else:
        return [send_cts[t] for t in range(amount)]


def send_contents(contents, member):
    print('有这么一些需要发送：\n')
    show_cts = '--------------------------------------------------------------\n'.join(contents)
    print(show_cts)
    if len(contents) != 0:
        for k, v in enumerate(contents):
            member.send(v)
            logging.error('发送了第{0}个'.format(k + 1))
            if k + 1 == len(contents):
                break
            time.sleep(60)
    else:
        print('nothing')


if __name__ == '__main__':
    bot = wxpy.Bot(cache_path=True)
    # me = bot.search('【可聊】广海互联网社群')[0]
    me = bot.self
    print(me.name)
    times = 0
    while 1:
        times += 1
        str_cts = get_send_contents(2)
        send_contents(str_cts, me)
        print("进行了第%d轮action" % times)
        time.sleep(600)
