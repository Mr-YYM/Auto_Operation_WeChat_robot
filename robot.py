import wxpy
import data_getter
import db_process
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


if __name__ == '__main__':
    bot = wxpy.Bot(cache_path=True, console_qr=1)
    me = bot.search('【可聊】广海互联网社群')[0]
    # me = bot.self
    print(me.name)
    times = 0
    while 1:
        times += 1
        print("☆☆开始进行第%d轮action☆☆\n%s" % (times, '-'*60))

        cts = data_getter.read_contents_from_readhub()  # raw contents
        add_cts = db_process.get_addition_contents(cts)  # insert contents into database and get addition contents
        fmt_cts = data_getter.get_formatted_contents(add_cts, 2)  # formatting contents
        to_send_cts = data_getter.get_limited_amount_contents(fmt_cts)  # final contents in a limited amount

        try:
            send_contents(to_send_cts, me)
        except wxpy.ResponseError as exp:
            if exp.err_code == 1100 or 1101 or 1102:
                print('☆☆账号异常退出，请重新登录☆☆')
                bot = wxpy.Bot(cache_path=True, console_qr=1)
            else:
                print('发生了一些错误：', exp)
                break
        print("☆☆刚刚获取了一些信息☆☆\n%s" % '-' * 60)
        time.sleep(900)
