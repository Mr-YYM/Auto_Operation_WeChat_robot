import pymysql
import logging

def get_addition_contents(contents):
    info_db = pymysql.connect("localhost", "root", "123456", "info_crbotdb", charset='utf8mb4')
    cursor = info_db.cursor()
    addition_content = {}
    for title, v in contents.items():
        try:
            cursor.execute("INSERT INTO information "
                           "(time, title, content, link) "
                           "VALUES (%s, %s, %s, %s)", (v['date_time'], title, v['content'], v['link']))
            addition_content[title] = v
            print("更新了" + title)
        except:
            logging.error("已经有了：" + title)
    info_db.commit()
    return addition_content