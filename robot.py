import wxpy
import data_getter
import db_process
import time
import logging

contents = data_getter.read_contents_from_readhub()
add_cont = db_process.get_addition_contents(contents)

str_cts = []
print('有这么一些需要发送：\n')
for title, v in add_cont.items():
    str_cts.append('【%s】\n%s\n%s\n' % (title, v['content'], v['link']))
show_cts = '--------------------------------------------------------------\n'.join(str_cts)
print(show_cts)

if len(str_cts) != 0:
    bot = wxpy.Bot(cache_path=True)
    me = bot.self
    for k, v in enumerate(str_cts):
        me.send(v)
        logging.error('发送了第{0}个'.format(k+1))
        if k+1 == len(str_cts):
            break
        time.sleep(5)
else:
    print('nothing')
# print(show_cts)
