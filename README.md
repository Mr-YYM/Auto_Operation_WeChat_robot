# Auto_subscribe_info_WeChat_robot

## 程序设计
### 1、定时（10min）爬取readhub.me的新闻内容

### 2、将新闻内容存入到数据库当中，此时程序会找出新增的新闻内容

### 3、将得到的新闻内容发送到指定的微信群
使用wxpy模块可实现操作。
为了能够正常获得群对象，需要登录前保证在群说一句话，把群冒上来。谨记！！！

```python
import wxpy
bot = wxpy.Bot() # 扫码登录，获取一个微信机器人对象
friend = bot.search('群的名字或者具体一个人的昵称、备注')
# 也可以使用 bot.groups() 获取所有群组
```
详情查看模块文档：
http://wxpy.readthedocs.io/zh/latest/

### 4、由于信息量较大，为防止发送速度过快，影响群秩序与网络正常通信，因此获取到的内容每隔1min发送一条

### 5、新闻内容形式：【标题】+ 内容 + 链接

### 6、机器人放在服务器上 24h 运行


## 数据库设计
1、创建一个数据库，名为info_crbotdb (你也可以自定义名字，但需要更改程序)
2、创建一个名为information的表，表设计如下：

![db_style](https://raw.githubusercontent.com/Mr-YYM/Auto_subscribe_info_WeChat_robot/master/db_style.png)

代码如下：

```sql
CREATE TABLE information
(
  time        DATETIME     NULL,
  title       VARCHAR(256) NULL,
  content     TEXT         NULL,
  link        TEXT         NULL,
  src_website TEXT         NULL,
  CONSTRAINT information_title_uindex
  UNIQUE (title)
)
  COMMENT '新闻信息'
  ENGINE = InnoDB;
```

