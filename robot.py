import wxpy
import data_getter
import db_process
import time
import logging


def get_send_contents():
    contents = data_getter.read_contents_from_readhub()
    add_cont = db_process.get_addition_contents(contents)
    send_cts = []
    print('有这么一些需要发送：\n')
    for title, v in add_cont.items():
        send_cts.append('【%s】\n%s\n%s\n' % (title, v['content'], v['link']))
    show_cts = '--------------------------------------------------------------\n'.join(send_cts)
    print(show_cts)

    return send_cts


def send_contents(sending_cts, member):
    if len(sending_cts) != 0:
        for k, v in enumerate(sending_cts):
            member.send(v)
            logging.error('发送了第{0}个'.format(k + 1))
            if k + 1 == len(sending_cts):
                break
            time.sleep(180)
    else:
        print('nothing')


if __name__ == '__main__':
    bot = wxpy.Bot(cache_path=True, console_qr=True)
    me = bot.search('【可聊】广海互联网社群')[0]
    print(me.name)
    times = 0
    while 1:
        times += 1
        str_cts = get_send_contents()
        send_contents(str_cts, me)
        print("进行了第%d轮action" % times)
        time.sleep(600)
