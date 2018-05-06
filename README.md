# Auto_Operation_WeChat_robot

这个项目是一个微信机器人，由广东海洋大学互联网社群技术部开发。通过本机器人可以实现自动化的管理社群涉及的大量群聊，减轻管理人员的压力。

## 功能一：定时向指定群聊发送新闻
自动爬取网页信息，然后对信息进行处理之后，发送到特定微信群的中。有以下这些功能：
### 1、定时（15min）爬取readhub.me的新闻内容

### 2、将新闻内容存入到数据库当中

数据库长这样：

![db_sample](https://codingnote.oss-cn-shenzhen.aliyuncs.com/db_sample.png)

### 3、定时从数据库中获取新闻内容发送到指定的微信群
#### 机器人能够同时管理多个群

### 4、由于信息量较大，为防止发送速度过快，影响群秩序与网络正常通信，因此获取到的内容每隔1min发送一条

### 5、新闻内容形式：【标题】+ 内容 + 链接

sample：

【放弃 WP 是必然：微软持续推进 Surface Phone】

之前微软曾宣布，从 2 月 20 日起，Windows Phone 7 以及 Windows Phone 8 系统的手机用户，将不再支持通知信息推送，而一些有价值的动态方块更新功能也将停止 ... 了，Windows Phone 8.1、Windows 10 移动版的用户将依然享受上述功能，不过这样状况也不会持续太久，仅仅只是维持，因为微软已经从根本上放弃了这个移动系统 ... 从外媒给出的最新报道称，放弃 WP 系统后，微软目前仍然在秘密暗中推进自家的 Surface Phone 项目，这不仅仅是一台手机那么简单，而众多专利图显示，该设备采用双屏折叠设计，合起来是手机的形态，而展开后就是个微型电脑，属于 One Core 大框架下的产品。

http://tech.sina.com.cn/mobile/n/n/2018-02-22/doc-ifyrswmu8256844.shtml


## 功能二、机器人放在服务器上 24h 运行

## 功能三、回复关键字自动拉人进群

## 功能四、回复关键字自动回复相关的新闻信息（待实现）

## 功能五、建设黑名单，禁止违反群规人士进群（待实现）

## 功能六、建设机器人的client与server互通，实现client远程控制（待实现）

## 功能七、client的GUI可视化界面

### （一些想法）

* IOS、Android、Win三平台通用，使用前端通用框架建设应用！

### feature：
* 获取远程的二维码，扫码登录，自动提示登录成功
* 自动拉取群列表、、、需要机器人管理的群

### 机器人properties的修改：

* 每个群的关键字可以自定义
* 自动添加好友，请求关键字自定义

## 功能八、机器人的属性热修改，更新参数不需要重启。

## 数据库设计
1、创建一个数据库，名为info_crbotdb (你也可以自定义名字，但需要更改程序)
2、创建一个名为information的表，表结构设计如下：

![db_style](https://codingnote.oss-cn-shenzhen.aliyuncs.com/db_style.png)

表结构代码如下：

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

如果遇到数据库报错：
Incorrect string value: '...' for column 'title' at row 1
执行以下sql命令解决：
```sql
alter table information convert to character set utf8mb4 collate utf8mb4_bin
```

## wxpy模块的用法
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

## 开发人员名单
1、Mr.YYM
