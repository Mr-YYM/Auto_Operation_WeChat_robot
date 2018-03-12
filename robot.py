import wxpy
import data_getter
import time
import logging


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


def send_news_to_groups(a_bot):
    me = a_bot.search('【资讯】广海互联网社群')[0]
    # me = bot.self
    print(me.name)

    times = 0
    while 1:
        times += 1
        print("☆☆群【%s】开始进行第%d轮action☆☆\n%s" % (me.name, times, '-' * 60))

        to_send_cts = data_getter.get_send_cts()

        try:
            send_contents(to_send_cts, me)
            print("☆☆刚刚获取了一些信息☆☆\n%s" % ('-' * 60))
        except wxpy.ResponseError as exp:
            if exp.err_code == 1100 or 1101 or 1102:
                print('☆☆账号异常退出，请重新登录☆☆')
                a_bot = wxpy.Bot(console_qr=1)
            else:
                print('发生了一些错误：', exp)
                break
        time.sleep(900)


if __name__ == '__main__':
    bot = wxpy.Bot(cache_path=True, console_qr=1)
    send_news_to_groups(bot)
