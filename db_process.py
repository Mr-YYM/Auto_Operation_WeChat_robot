import pymysql
import logging
import re


def get_source_link(website):
    if re.search('url=', website) is not None:
        return re.split('url', website)[1]
    else:
        r = re.search('(http|https)(.+)(\.com|\.cn|\.org|\.net)', website)
    if r is not None:
        return r.group()
    else:
        return None


def get_addition_contents(contents):
    info_db = pymysql.connect("localhost", "root", "123456", "info_crbotdb", charset='utf8mb4')
    cursor = info_db.cursor()
    addition_content = {}
    for title, v in contents.items():
        try:
            cursor.execute("INSERT INTO information "
                           "(time, title, content, link, src_website) "
                           "VALUES (%s, %s, %s, %s, %s)",
                           (v['date_time'], title, v['content'], v['link'], get_source_link(v['link']))
                           )
            addition_content[title] = v
            print("更新了" + title)
        except pymysql.IntegrityError:
            logging.error("已经有了：" + title)
        except Exception as exp:
            logging.error("error:" + exp)
    info_db.commit()
    return addition_content
