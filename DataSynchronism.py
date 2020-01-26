"""
@FileName   : DataSynchronism.py
@Author     : Chen Wang
@Version    : Python3.8 、Windows or Linux
@Description: 后端用户名数据的同步采用 Mysql+Redis；
读：在不是高并发情况下先查询Redis，有返回，无则查mysql，有更新Redis数据。
写：直接写入mysql数据库，然后删除缓存Redis，更新写入Redis数据。
@Time       : 2020/1/25 13:51
@Software   : PyCharm
@Contact    : 1416825008@qq.com
@Github     : https://github.com/JackMin1314/Python_Study
@Gitee      : https://gitee.com/JackMin1314/Python_Study
代 码 仅 限 学 习 ，严 禁 商 业 用 途，转 载 请 注 明 出 处~

"""
# import lib
import pymysql
import redis

# global mysql and redis config
mysql_base = 'spider'
mysql_table = 'userinfo'
mysql_passwd = '5201020116'
redis_passwd = '5201020116'


# 读取Redis数据和Mysql
def query_redis(username):
    """读取Redis数据和Mysql

    :param username: 需要查询的用户名
    :return: json格式结果
    """
    # 与Redis建立连接(连接池)
    redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, password='5201020116')
    r = redis.Redis(connection_pool=redis_pool)
    result_redis = r.hgetall(username)
    result_json = {
        "code": '',
        "data": '',
        "msg": ''
    }
    # 如果数据存在则输出，不存在则重新查询mysql数据库
    if result_redis:
        # print("Redis查询到的 {0} 数据为: {1}".format(username, result_redis))
        # r.delete(username)
        #         # print("删除成功")
        # 成功返回json数据
        result_json["code"] = '0'
        result_json["data"] = result_redis
        result_json["msg"] = 'Success'

    else:
        # 连接mysql
        db = pymysql.Connect('localhost', 'root', mysql_passwd, mysql_base, charset='utf8')
        cursor = db.cursor()
        # 查询数据库 userinfo 表格中是否存有数据
        sql = 'select USER_ID, USER_PASSWD from {0} where USER_NAME=%s;'.format(mysql_table)
        cursor.execute(sql, username)
        result_mysql = cursor.fetchall()
        # 数据库没有数据返回Failed;有数据写入Redis并返回
        if not result_mysql:
            print('Mysql中没有该 %s 用户' % username)
            result_json["code"] = '-1'
            result_json["msg"] = 'Failed'
        else:
            # 查询到数据的时候写入Redis存储并设置过期时间（秒）
            print("Mysql中查询到的{0}数据为: {1}".format(username, result_mysql))
            r.hmset(username, {
                "username": result_mysql[0][0],
                "passwd": result_mysql[0][1]
            })
            r.expire(username, 60*60*60*6)
            print("写入Redis存储成功")
            result_json["code"] = '1'
            result_json["data"] = result_redis
            result_json["msg"] = 'Success'
        db.close()
    r.close()
    return result_json


# Mysql数据库添加更新后同步到Redis
def sync_redis_insert(username, passwd):
    """Mysql数据库用户更新后同步到Redis

    :param username: 刚注册的用户名
    :param passwd: 刚注册的用户密码
    :return: bool
    """
    redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, password=redis_passwd)
    r = redis.Redis(connection_pool=redis_pool)
    flag = False  # 标记操作成功或失败
    db = pymysql.Connect('localhost', 'root', mysql_passwd, mysql_base, charset='utf8')
    cursor = db.cursor()

    # 先查询本地mysql是否有该数据记录，有的话则修改,然后同步 到redis;没有则是插入，同步到Redis
    checkjson = query_redis(username)
    if checkjson["code"] == "-1":
        print("新用户注册")
        try:
            sql = "insert ignore into {0}(USER_ID,USER_NAME,USER_PASSWD,SUBMISSION_DATE) values('',%s,{1},CURRENT_DATE);".format(mysql_table, passwd)
            cursor.execute(sql, [username])     # 新用户直接添加
            db.commit()
            # 再次查询该用户然后同步到Redis
            sql = 'select USER_ID, USER_PASSWD from {} where USER_NAME=%s;'.format(mysql_table)
            cursor.execute(sql, [username])
            result_mysql = cursor.fetchall()
            r.hmset(username, {
                "username": result_mysql[0][0],
                "passwd": result_mysql[0][1]
            })
            r.expire(username, 60 * 60 * 60 * 6)
            flag = True
        except:
            print("新用户注册入库失败")
            db.rollback()
            flag = False
    else:
        # 本地mysql有该用户直接更新密码并同步Redis
        print("mysql本地有 %s 用户,直接修改并同步" % username)

        try:
            sql = 'update {0} set USER_PASSWD={1},SUBMISSION_DATE=CURRENT_DATE where USER_NAME=%s;'.format(mysql_table, passwd)
            cursor.execute(sql, [username])
            db.commit()
            sql = 'select USER_NAME, USER_PASSWD from {} where USER_NAME=%s;'.format(mysql_table)
            cursor.execute(sql, [username])
            result_mysql = cursor.fetchall()
            r.hmset(username, {
                "username": result_mysql[0][0],
                "passwd": result_mysql[0][1]
            })
            r.expire(username, 60 * 5)
            flag = True
        except:
            print("用户修改密码失败")
            db.rollback()
            flag = False
    r.close()
    db.close()
    return flag


# MySQL数据库删除数据同步到Redis
def sync_redis_delete(username):
    """MySQL数据库删除数据同步到Redis

    :param username: 需要删除的用户名
    :return: bool
    """
    redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, password=redis_passwd)
    r = redis.Redis(connection_pool=redis_pool)
    flag = True  # 标记操作成功或失败
    db = pymysql.Connect('localhost', 'root', mysql_passwd, mysql_base, charset='utf8')
    cursor = db.cursor()

    # 先查询本地mysql是否有用户数据记录,有的话则删除,然后同步到redis;没有则不执行任何操作返回true
    checkjson = query_redis(username)
    if checkjson["code"] == "-1":
        r.close()
        db.close()
        flag = True
    else:
        # 有用户数据，直接删除mysql和Redis
        print("mysql本地有 %s 用户,直接删除并同步" % username)
        isRedis = False
        try:
            # 直接删除数据库
            sql = 'delete from {0} where USER_NAME=%s;'.format(mysql_table)
            cursor.execute(sql, [username])
            sql = 'Alter table {0} AUTO_INCREMENT=1;'.format(mysql_table)
            cursor.execute(sql)
            db.commit()
            isRedis = True
            # 删除redis缓存的用户数据
            r.delete(username)
        except:
            print("删除Redis用户缓存失败" if isRedis else "删除MySQL用户数据失败")
            db.rollback()
            flag = False
        db.close()
        r.close()
    return flag



if __name__ == "__main__":
    # db_init()
    username = 'Peter'
    ansjson = query_redis(username)
    if ansjson["data"]:
        # 将byte转成了str
        print("%s的密码为 " % username, str(ansjson["data"][b"passwd"], encoding='utf-8'))
    else:
        print("status: " + ansjson["code"], "message: " + ansjson["msg"])

    isChanged = sync_redis_insert("Peter", "1789")
    if isChanged:
        print("insert ok")
    else:
        print("insert err")

    isChanged = sync_redis_delete("Peter")
    if isChanged:
        print("delete ok")
    else:
        print("delete err")


# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
# 初始化数据库代码
# 首先 mysql -u root -p 输入密码
# 然后 source  /绝对路径下的/Mysql_Init_Script.sql
'''
CREATE DATABASE  if NOT EXISTS spider;
use spider;
CREATE TABLE  if NOT EXISTS userinfo(
USER_ID INT AUTO_INCREMENT,
USER_NAME VARCHAR(40) NOT NULL,
USER_PASSWD VARCHAR(100) NOT NULL,
SUBMISSION_DATE VARCHAR(40),
PRIMARY KEY (USER_ID, USER_NAME)
)ENGINE=INNODB DEFAULT CHARSET="utf8";

'''
