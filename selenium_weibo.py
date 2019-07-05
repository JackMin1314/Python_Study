'''
#!/usr/bin/env python
# -*- encoding: utf-8 -*-

@FileName  :   selenium_weibo.py
@Author    :   Chen Wang
@Version   :   Python3.X 
@Decription:   selenium学习，另一种方式爬取微博.
需要将webdriver.exe添加到python安装根目录下
@Time      :   6/4/2019 08:19
@Contact   :   QQ:1416825008
@Blog      :   https://github.com/JackMin1314/Python_Study
代 码 仅 限 学 习 ，转 载 请 注 明 出 处

'''
# import lib
# coding = utf-8
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import random
import time
import re
import json
# from mitmproxy import ctx
# from bs4 import BeautifulSoup

user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]
ua = random.choice(user_agent_list)

TIME_TIMEOUT = 10
# 创建chrome启动选项
chrome_options = webdriver.ChromeOptions()
# chrome_options.set_headless()
chrome_options.add_argument('--user-agent=%s' % ua)
chrome_options.add_argument('lang=zh_CN.UTF-8')
# 关闭提示（浏览器正在被自动化程序控制）但是会有提示框
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

# 指定chrome启动类型为headless 并且禁用gpu（无启动页面）
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# 调用环境变量指定的chrome浏览器创建浏览器对象
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.implicitly_wait(6)  # seconds
driver.get("http://www.baidu.com")
# assert断言语句用来声明某个条件是真的，
# 其作用是测试一个条件(condition)是否成立，如果不成立，则抛出异常
assert "No results found." not in driver.page_source
# 需要爬取的页面微博地址
url1 = "https://m.weibo.cn/detail/4379722387261630"
# 预先访问一下微博页面
url2 = "https://m.weibo.com"
driver.get(url2)
time.sleep(2)
url_login = "https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349"
driver.get(url_login)
# 微博通过navigator判断是否selenium，这里设置很重要！！！
driver.execute_script("Object.defineProperties(navigator,{webdriver:{get:() => false}})")
# 用户名和密码，需要关闭手机上的二次验证
username = "17718261816"
password = "5201020lovemin"
time.sleep(2)
# 采用xpath找页面元素并自动输入
driver.find_element_by_xpath('//form/section[@class="box"]/div[@class="input-wrapper"]/p[@class="input-box"]/input[@type="text"]').click()
driver.find_element_by_xpath('//form/section[@class="box"]/div[@class="input-wrapper"]/p[@class="input-box"]/input[@type="text"]').send_keys(username)
# 反爬
time.sleep(2)
driver.find_element_by_xpath('//form/section[@class="box"]/div[@class="input-wrapper"]/p[@class="input-box"]/input[@type="password"]').click()
driver.find_element_by_xpath('//form/section[@class="box"]/div[@class="input-wrapper"]/p[@class="input-box"]/input[@type="password"]').send_keys(password)
time.sleep(1.5)
driver.find_element_by_id("loginAction").click()
time.sleep(3)
# email = WebDriverWait(driver, TIME_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//*[@id='loginName']")))
# driver.back()
print("登录成功，请点击按钮")
# selenium获取到的cookies是一个列表，内嵌字典格式！改为后面requests模块需要的cookies（浏览器看到的样式）
list_cks = {}
cookie = driver.get_cookies()
for cks in cookie:
    name = cks['name']
    value = cks['value']
    list_cks[name] = value
print("当前的cookies：", list_cks)
flag = 0
re_login = 0
# 登录成功后会有验证，错误次数过多会有geetest极验 滑块或者识别图文字
# 若出现重新运行程序或者重新登陆，也推荐手工解决，理论上可以不通过selenium解决，但是成本较高，劳力伤财
try:
    geetest_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_wait')))
    print("geetest_btn is existent")
    time.sleep(1)
    # ???????????????????????????????????????????????
    driver.find_element_by_class_name("geetest_btn").click()
# 判断是否有验证出现
    if EC.presence_of_element_located((By.CLASS_NAME, "geetest_wrap")):
        print("有验证,请手工解决!!!")
        time.sleep(7)
        flag = 1

finally:
    print("flag:%s" % flag)  # 后期这里注释掉
    if flag == 0:
        print("未找到相关验证,页面跳转主页面")
    # driver.quit()
# 等待页面加载（有页面跳转，所以时间长一点）

time.sleep(5)
print("成功验证！")
print("尝试访问url:%s" % url1)
# 访问所给的爬取页面
driver.get(url1)
# 浏览器加载页面并渲染需要时间
time.sleep(5)
cookies = driver.get_cookies()
print("访问url后的cookies", cookies)
# selenium获取到的cookies是一个列表，内嵌字典格式！（这是第二种方法了，利用列表添加元素的append方法）
driver.refresh()
cookie_list = []
for dict in cookies:
    cookie = dict['name'] + '=' + dict['value']
    cookie_list.append(cookie)
    cookie = ';'.join(cookie_list)
print(cookie_list)
time.sleep(1)

# 访问该页面的评论页面（返回的是json数据格式），下一页评论参数由当前页最后max_id决定
driver.get("https://m.weibo.cn/comments/hotflow?id=4379722387261630&mid=4379722387261630&max_id_type=0")
# 这里也是获取cookies看看，使用append追加方法，因而不会覆盖上一个访问url1的cookies内容
cookies2 = driver.get_cookies()
for dict in cookies2:
    cookie = dict['name'] + '=' + dict['value']
    cookie_list.append(cookie)
    cookie = ';'.join(cookie_list)
print(cookie_list)
# 获取当前网页源码
str = driver.page_source
# 返回源码带了html的标签，我们只要中间的json数据，采用字符串切片
str = str[84:-20]
# json.loads() 将已编码的 JSON 字符串解码为 Python 对象
# json.dumps() 将 Python 对象编码成 JSON 字符串格式
html = json.loads(str)
# 在返回的json后面找下一页的参数max_id
# 已缓存的数据再次访问(浏览器或者程序)会返回{'OK':0}
if html['ok'] == 0:
    print('数据已缓存')
    max_id = 0
else:
    max_id = html['data']['max_id']       # 获取到max_id
    print("*"*15)
    print("下一页max_id是：", html['data']['max_id'])
# 尝试打印当前页面的评论,微博每页评论一次20个
print('Here are some comments:')
for li in range(0, 20):
    str = html['data']['data'][li]["text"]
    # 正则表达式去标签（注意：对于@xxx 在前面会丢掉该评论；emoji表情自动丢弃）
    p = re.compile('<[^>]+>')
    str1 = p.sub("", str)
    print(str1[:str1.find("&lt")])
# 后退页面，即返回到原先爬去微博的页面
driver.back()
# 等待加载
time.sleep(3)
# 获取当前运行浏览器的高度
hight_dic = driver.get_window_size()['height']
print("当前的浏览器的高度为：", hight_dic)
# 将滚动条移动到页面的底端
hight = 0
while(True):
    hight += random.choice([1, 2, 4, 3])*80
    try:
        js = "var q=document.documentElement.scrollTop={}".format(hight)
        driver.execute_script(js)
        print("当前的滑动的高度为：", hight)
    except:
        if hight == 0:
            print("执行JS失败")
            break
        elif hight >= hight_dic:
            print("页面到底部或跳转到登陆页面")
            break
    finally:
        if hight == 0:
            break
        if hight >4000:
            print("重新登录")
            re_login = 1
            break
    time.sleep(random.choice([1, 0.5, 2, 0.7, 1.5]))

if re_login == 0:
    driver.find_element_by_xpath(
        '//form/section[@class="box"]/div[@class="input-wrapper"]/p[@class="input-box"]/input[@type="text"]').click()
    driver.find_element_by_xpath(
        '//form/section[@class="box"]/div[@class="input-wrapper"]/p[@class="input-box"]/input[@type="text"]').send_keys(
        username)
    # 反爬
    time.sleep(2)
    driver.find_element_by_xpath(
        '//form/section[@class="box"]/div[@class="input-wrapper"]/p[@class="input-box"]/input[@type="password"]').click()
    driver.find_element_by_xpath(
        '//form/section[@class="box"]/div[@class="input-wrapper"]/p[@class="input-box"]/input[@type="password"]').send_keys(
        password)
    time.sleep(1.5)
    driver.find_element_by_id("loginAction").click()
    time.sleep(3)
    geetest_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_wait')))
    print("geetest_btn is existent")
    # ???????????????????????????????????????????????
    driver.find_element_by_class_name("geetest_btn").click()
    time.sleep(5)
input("please input anykey to continue...")
driver.quit()


'''
事先访问了
driver.forward().前进页面
driver.back() 后退页面
driver.refresh() 刷新页面
'''

