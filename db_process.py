import pymysql
import logging


def insert_cts_toDB(contents):
    info_db = pymysql.connect("localhost", "root", "123456", "info_crbotdb", charset='utf8mb4')
    cursor = info_db.cursor()
    alr = 0
    for title, v in contents.items():
        try:
            cursor.execute("INSERT INTO information "
                           "(time, title, content, link, src_website) "
                           "VALUES (%s, %s, %s, %s, %s)",
                           (v['date_time'], title, v['content'], v['link'], v['src_website'])
                           )
            print("☆☆数据库更新了: %s " % title)
        except pymysql.IntegrityError:
            # logging.error("已经有了：" + title)
            alr += 1
        except Exception as exp:
            logging.error("error:" + exp)
    logging.error("%s\n原来已经有%d个在数据库" % ('-' * 60, alr))
    info_db.commit()


def get_contents(amount):
    info_db = pymysql.connect("localhost", "root", "123456", "info_crbotdb", charset='utf8mb4')
    cursor = info_db.cursor()
    cursor.execute("SELECT time, title, content, link FROM information ORDER BY time DESC limit %d" % amount)
    raw = cursor.fetchall()
    article = {e[1]:
                    {'content': e[2], 'link': e[3]}
               for e in raw}
    return article

# if __name__ == '__main__':
#     ad = get_addition_contents(data_getter.read_contents_from_readhub())
