import pymysql
import logging


def get_addition_contents(contents):
    info_db = pymysql.connect("localhost", "root", "123456", "info_crbotdb", charset='utf8mb4')
    cursor = info_db.cursor()
    addition_content = {}
    alr = 0
    for title, v in contents.items():
        try:
            cursor.execute("INSERT INTO information "
                           "(time, title, content, link, src_website) "
                           "VALUES (%s, %s, %s, %s, %s)",
                           (v['date_time'], title, v['content'], v['link'], v['src_website'])
                           )
            addition_content[title] = v
            print("更新了" + title)
        except pymysql.IntegrityError:
            # logging.error("已经有了：" + title)
            alr += 1
        except Exception as exp:
            logging.error("error:" + exp)
    logging.error("%s\n原来已经有%d个在数据库" % ('-' * 60, alr))
    info_db.commit()
    return addition_content


# if __name__ == '__main__':
#     ad = get_addition_contents(data_getter.read_contents_from_readhub())
