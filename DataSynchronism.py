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
from BackServer.log.errlogs import logger


from BackServer.Config.config import mysql_base, mysql_table, mysql_passwd, redis_passwd, max_EmailCodeTime

# global mysql and redis Config
# mysql_base = 'spider'
# mysql_table = 'userinfo'
# mysql_passwd = '5201020116'
# redis_passwd = '5201020116'


# 读取Redis数据和Mysql
def query_redis(username: str):
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
    print("query redis结果", result_redis)
    # 如果数据存在则输出，不存在则重新查询mysql数据库
    if result_redis:
        # print("Redis查询到的 {0} 数据为: {1}".format(username, result_redis))
        # r.delete(username)
        #         # print("删除成功")
        # 成功返回json数据
        result_json["code"] = '0'
        result_json["data"] = result_redis
        result_json["msg"] = 'Success'
        logger.info("查询redis中%s用户数据为%s:" % (username, result_redis))

    else:
        # 连接mysql
        db = pymysql.Connect('localhost', 'root', mysql_passwd, mysql_base, charset='utf8')
        cursor = db.cursor()
        myname = "\"{0}\"".format(username)
        # 查询数据库 userinfo 表格中是否存有数据
        sql = 'select USER_TYPE, USER_LOCK, USER_NAME, USER_PASSWD, USER_SALT, USER_MAIL, SUBMISSION_DATE from {0} where USER_NAME={1};'.format(mysql_table, myname)
        print('未知列字段sql', sql)
        cursor.execute(sql)
        result_mysql = cursor.fetchall()
        print("test sql %s \n" % sql, result_mysql)
        # 数据库没有数据返回Failed;有数据写入Redis并返回
        if not result_mysql:
            print('Mysql中没有该 %s 用户' % username)
            result_json["code"] = '-1'
            result_json["msg"] = 'Failed'
            logger.warning("MySQL中无%s用户" % username)
        else:
            # 查询到数据的时候写入Redis存储并设置过期时间（秒）
            print("Mysql中查询到{0}用户数据为: {1}".format(username, result_mysql))
            r.delete(username)
            r.hmset(username, {
                "usertype": result_mysql[0][0],
                "userlock": result_mysql[0][1],
                "username": result_mysql[0][2],
                "passwd": result_mysql[0][3],
                "salt": result_mysql[0][4],
                "usermail": result_mysql[0][5],
                "submission": result_mysql[0][6]
            })
            r.expire(username, 60*60*24*6)
            print("{}写入Redis存储成功".format(username))
            result_redis = r.hgetall(username)
            result_json["code"] = '1'
            result_json["data"] = result_redis
            result_json["msg"] = 'Success'
            logger.info("MySQL写入redis中%s用户数据为%s:" % (username, result_redis))
        db.close()
    r.close()
    return result_json


# Mysql数据库添加更新后同步到Redis
def sync_redis_insert(username:str, passwd, salt_value, *kv):
    """Mysql数据库用户更新后同步到Redis

    :param username: 刚注册的用户名
    :param passwd: 刚注册的用户加密后的密码
    :param salt_value: 注册或修改密码时候用于MD5的盐urandom(32).hex()
    :param *kv: 针对email，调用函数时候可选参数，仅用于注册时候使用
    :return: bool
    """
    # pymysql执行sql语句时候set，insert需要注意参数“”的转义


    passwd = "\"{0}\"".format(str(passwd,'utf-8'))
    salt_value = "\"{0}\"".format(str(salt_value,'utf-8'))
    redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, password=redis_passwd)
    r = redis.Redis(connection_pool=redis_pool)
    db = pymysql.Connect('localhost', 'root', mysql_passwd, mysql_base, charset='utf8')
    cursor = db.cursor()

    # （改密码）先查询本地mysql是否有该数据记录，有的话则修改,然后同步 到redis;
    # （新用户注册）没有则是插入，同步到Redis
    checkjson = query_redis(username)

    if checkjson["code"] == "-1":
        print("新用户注册")
        # 因为代码逻辑太复杂，新用户注册时候默认usertype为user而userlock为0不锁定
        username = "\"{0}\"".format(username)
        try:
            email = "\"{0}\"".format(kv[0])
            sql = "insert  into {0}(USER_NAME, USER_PASSWD, USER_SALT, USER_MAIL, SUBMISSION_DATE) values({1},{2},{3},{4},CURRENT_DATE);".format(
                mysql_table, username, passwd, salt_value, email)
            cursor.execute(sql)
            db.commit()
            # 再次查询该用户然后同步到Redis
            sql = 'select USER_TYPE, USER_LOCK, USER_NAME, USER_PASSWD, USER_SALT, USER_MAIL, SUBMISSION_DATE from {0} where USER_NAME={1};'.format(mysql_table, username)
            cursor.execute(sql)
            result_mysql = cursor.fetchall()
            r.hmset(username, {
                "usertype": result_mysql[0][0],
                "userlock": result_mysql[0][1],
                "username": result_mysql[0][2],
                "passwd": result_mysql[0][3],
                "salt": result_mysql[0][4],
                "usermail": result_mysql[0][5],
                "submission": result_mysql[0][6]
            })
            r.expire(username, 60*60*24*6)
            flag = True
        except:
            # 也有可能是email或者用户名重复了，默认是一个email下跟一个用户绑定
            print("新用户注册入库失败")
            db.rollback()
            flag = False
    else:
        # 本地mysql有该用户直接更新密码并同步Redis
        print("mysql本地有 %s 用户,直接修改密码并同步" % username)
        try:
            myname = "\"{0}\"".format(username)
            sql = 'update {0} set USER_PASSWD={1},USER_SALT={2},SUBMISSION_DATE=CURRENT_DATE where USER_NAME={3};'.format(
                mysql_table, passwd, salt_value, myname)
            cursor.execute(sql)
            print("update sql", sql)
            db.commit()
            if refresh_redis(username):
                print("refresh redis中用户%s数据成功..."% username)
            else:
                print("refresh redis中用户%s数据失败..."% username)
            # sql = 'select  USER_NAME, USER_PASSWD, USER_SALT from {0} where USER_NAME={1};'.format(mysql_table, username)
            # cursor.execute(sql)
            # result_mysql = cursor.fetchall()
            # r.hmset(username, {
            #     "username": result_mysql[0][0],
            #     "passwd": result_mysql[0][1],
            #     "salt": result_mysql[0][2]
            # })
            # r.expire(username, 60*60*24*6)
            flag = True
        except:
            print("修改mysql用户密码失败")
            db.rollback()
            flag = False
    db.close()
    r.close()
    return flag


# MySQL数据库删除数据同步到Redis
def sync_redis_delete(username: str, email: str):
    """MySQL数据库删除数据同步到Redis

    :param username: 需要删除的用户名
    :param email: 用户的邮箱
    :return: bool
    """
    redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, password=redis_passwd)
    r = redis.Redis(connection_pool=redis_pool)
    flag = True  # 标记操作成功或失败
    db = pymysql.Connect('localhost', 'root', mysql_passwd, mysql_base, charset='utf8')
    cursor = db.cursor()

    # 先查询本地mysql是否有用户数据记录,有的话则删除,然后同步到redis;没有则不执行任何操作返回true
    if not exist_UserName_email(username, email):
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
            # sql = 'Alter table {0} AUTO_INCREMENT=1;'.format(mysql_table)
            # cursor.execute(sql)
            db.commit()
            isRedis = True
            # 删除redis缓存的用户数据
            r.delete(username)
            logger.info("本地有%s用户数据删除成功" % username)
        except Exception as e:
            print("删除Redis用户缓存失败" if isRedis else "删除MySQL用户数据失败")
            db.rollback()
            flag = False
            logger.error("本地有%s用户数据删除失败，原因%s" % (username, e))
    db.close()
    r.close()
    return flag


# 从mysql刷新数据到Redis
def refresh_redis(username: str):
    """从mysql刷新数据到Redis
    :param username: 需要刷新的用户名
    :return bool
    """
    redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, password=redis_passwd)
    r = redis.Redis(connection_pool=redis_pool)
    db = pymysql.Connect('localhost', 'root', mysql_passwd, mysql_base, charset='utf8')
    cursor = db.cursor()
    myname = "\"{0}\"".format(username)
    try:
        sql = 'select USER_TYPE, USER_LOCK, USER_NAME, USER_PASSWD, USER_SALT, USER_MAIL, SUBMISSION_DATE from {0} where USER_NAME={1};'.format(mysql_table, myname)
        print("refresh_redis", sql)
        cursor.execute(sql)
        result_mysql = cursor.fetchall()
        print("refresh redis from mysql", result_mysql)
        r.delete(username)
        r.hmset(username, {
                "usertype": result_mysql[0][0],
                "userlock": result_mysql[0][1],
                "username": result_mysql[0][2],
                "passwd": result_mysql[0][3],
                "salt": result_mysql[0][4],
                "usermail": result_mysql[0][5],
                "submission": result_mysql[0][6]
        })
        r.expire(username, 60 * 60 * 24 * 6)
        flag = True
        logger.info("%s用户同步到redis刷新成功" % username)
    except Exception as e:
        db.rollback()
        flag = False
        logger.error("%s用户同步到redis刷新失败，原因：%s" % (username, e))
    db.close()
    r.close()
    return flag


# 全部清除redis中缓存数据信息
def redis_clear_all():
    """ 清除所有的redis 0号数据库内存中数据.谨慎操作

    :return: bool
    """
    r = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, password=redis_passwd)
    r = redis.Redis(connection_pool=redis_pool)
    r.flushall()


# 判断本地是否有同名用户名或邮箱
def exist_UserName_email(username: str, email: str):
    """ 判断用户名或者邮箱是否存在，有一个存在就返回True,都不存在返回False
    本地数据库已经修改username，email字段为unique类型,保证唯一

    :param username: 需要查询的用户名
    :param email: 需要查询的邮箱
    :return: bool
    """
    db = pymysql.Connect('localhost', 'root', mysql_passwd, mysql_base, charset='utf8')
    cursor = db.cursor()
    flag = True
    sql = 'select USER_NAME,USER_MAIL from {} where (USER_NAME=%s) or (USER_MAIL=%s);'.format(mysql_table)
    try:
        cursor.execute(sql, (username, email))
        result_mysql = cursor.fetchall()
        # 查询到本地数据库存在该数据的时候
        if result_mysql:
            flag = True
            logger.warning("查询%s用户或%s邮箱本地信息存在" % (username, email))
        # 本地没有任何同名用户名和email
        else:
            flag = False
    except Exception as e:
        print("查询用户%s失败" % username)
        logger.error("查询%s用户和%s邮箱信息失败,原因是: %s" % (username, email, e))
        db.rollback()
    db.close()
    return flag


# Redis保存十分钟邮箱验证码
def create_redis_Capture(email: str, capturecode: str):
    """用redis保存十分钟时长的用户验证码,返回插入成功或者失败

    :param email: 用户邮箱
    :param capturecode: 已发送的用户验证码
    :return: bool
    """
    redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, password=redis_passwd)
    r = redis.Redis(connection_pool=redis_pool)
    isRedis = False
    # 十分钟内再次请求需要删除之前的验证码
    pre_result = r.hgetall(email)
    if pre_result:
        r.delete(email)
    try:
        r.hset(email, email, capturecode)
        r.expire(name=email, time=max_EmailCodeTime)
        isRedis = True
        logger.info("redis保存%s邮箱的十分钟验证码%s成功" % (email, capturecode))
    except:
        isRedis = False
        print("redis保存十分钟验证码失败")
        logger.info("redis保存%s邮箱的十分钟验证码%s失败" % (email, capturecode))
    r.close()
    return isRedis


# 根据邮箱查询验证码
def query_redis_Capture(email: str):
    """根据返回的email字段查询是否有验证码，有返回，无返回None

    :param email:
    :return: 验证码字符串类型
    """
    redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, password=redis_passwd)
    r = redis.Redis(connection_pool=redis_pool)
    result_redis = r.hgetall(email)
    print(result_redis)
    if not result_redis:
        return None
    else:
        # 因为redis保存的键是utf-8的byte类型
        return (result_redis[bytes(email,'utf-8')]).decode('utf-8')


# 根据email查询是否有与用户一致
def is_consistent(email: str, username: str):
    """根据email查询是否有该用户

    :param email: 前端传来的需要查询的email
    :param username: 根据email需要核实的用户名
    :return: bool
    """
    email = "\'{}\'".format(email)
    db = pymysql.Connect('localhost', 'root', mysql_passwd, mysql_base, charset='utf8')
    cursor = db.cursor()
    flag = True
    sql = 'select USER_NAME from {0} where USER_MAIL={1};'.format(mysql_table, email)
    try:
        cursor.execute(sql)
        result_mysql = cursor.fetchall()
        # 查询到本地数据库存在该数据的时候
        if result_mysql and result_mysql[0][0] == username:
            flag = True
            logger.info("email:%s和用户名:%s一致" % (email, username))
        # 该email未注册用户，查不到数据
        else:
            print("查询email{0}和用户名{1}的结果为:{1}".format(email, username, result_mysql[0][0]))
            flag = False
            logger.waring("email:%s和用户名:%s不一致" % (email, username))
    except:
        print("查询email{0}和用户名{1}的结果为:{1}".format(email, username, result_mysql[0][0]))
        db.rollback()
    db.close()
    return flag


if __name__ == "__main__":
    redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, password=redis_passwd)
    r = redis.Redis(connection_pool=redis_pool)
    # r.hset(name="1416825008@qq.com", key="1416825008@qq.com", value="98756432")
    # r.expire(name="1416825008@qq.com", time=30)
    # result = r.hgetall(name="1416825008@qq.com")
    # if result:
    #     print("ok")
    # else:
    #     print("yes")
    # print(result)
    r.flushall()
    print('redis缓存清除成功')

# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
# 初始化数据库代码
# 首先 mysql -u root -p 输入密码
# 然后 source  /绝对路径下的/Mysql_Init_Script.sql
'''
CREATE DATABASE  if NOT EXISTS spider;
use spider;
CREATE TABLE IF NOT EXISTS userinfo (
    USER_TYPE VARCHAR(10) DEFAULT 'user',
    USER_LOCK VARCHAR(10) DEFAULT '0',
    USER_NAME VARCHAR(40) NOT NULL unique,
    USER_PASSWD VARCHAR(100) NOT NULL,
    USER_SALT VARCHAR(80) NOT NULL,
    USER_MAIL VARCHAR(40) NOT NULL unique,
    SUBMISSION_DATE VARCHAR(40),
    PRIMARY KEY (USER_MAIL)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8;
'''
