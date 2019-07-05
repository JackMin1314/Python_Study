#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@FileName  :   微博评论自动化爬取.py    
@Author    :   Chen Wang
@Version   :   Python3.X 、Windows or Linux
@Decription:   使用selenium登录获取cookies，然后结合requests爬取评论
@Time      :   7/5/2019 11:30
@Contact   :   QQ:1416825008
@Blog      :   https://github.com/JackMin1314/Python_Study
代 码 仅 限 学 习 ，严 禁 商 业 用 途，转 载 请 注 明 出 处

'''
# import lib
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

username = "17718261816"
password = "5201020lovemin"
url1 = "https://m.weibo.cn/detail/4379722387261630"
url2 = "https://m.weibo.com"
url_login = "https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349"
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
# 保存cookies
list_cks = {}
# 保存评论
comment_list = {}
# 关键字过滤
hideword = ['嫖娼',  '强奸', '第一', '第二', '第三', '政府', '特朗普', '上车', '股票', '沙发', '楼',  'www', ]
class weibo_spider():
    def __init__(self):
        self.username = username
        self.password = password
        self.ua = ua
        self.browser_setting()

    def browser_setting(self):
        # 创建chrome启动选项
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--user-agent=%s' % self.ua)
        self.chrome_options.add_argument('lang=zh_CN.UTF-8')
        # 关闭提示（浏览器正在被自动化程序控制）但是会有提示框
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 指定chrome启动类型为headless 并且禁用gpu（无启动页面）
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # 调用环境变量指定的chrome浏览器创建浏览器对象
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
        # 微博通过navigator判断是否selenium，这里设置很重要！！！
        self.driver.execute_script("Object.defineProperties(navigator,{webdriver:{get:() => false}})")

    def wb_urlneat(self, url):
        url = url  # 【添加手机上要爬取的微博正文】
        endstr = len(url)
        pattern = re.compile(r'\d+')
        try:
            m = pattern.match(url, 19, endstr)
            print(m)
            sub = m.group()
            print(m.group())
            newstr = url.replace(sub, 'status')
        except:
            newstr = url
        url = newstr
        detail_id = url[26:]
        print('detail_id: ', detail_id)
        self.url2 = url2
        self.url_login = url_login
        self.ua = ua
        self.list_cks = list_cks
        self.hideword = hideword
        self.comment_list = comment_list
        self.max_id = 0
        return url, detail_id

    def login_in(self):
        self.driver.implicitly_wait(6)  # seconds
        self.driver.get("http://www.baidu.com")
        self.driver.get(self.url1)
        time.sleep(2)
        self.driver.get(self.url2)
        self.driver.get(self.url_login)
        cookies = self.driver.get_cookies()
        self.list_cks = self.get_cks(cookies)
        print('url_login_cookies:', self.list_cks)
        # 采用xpath找页面元素并自动输入
        self.driver.find_element_by_xpath(
            '//form/section[@class="box"]/div[@class="input-wrapper"]/p[@class="input-box"]/input[@type="text"]').click()
        self.driver.find_element_by_xpath(
            '//form/section[@class="box"]/div[@class="input-wrapper"]/p[@class="input-box"]/input[@type="text"]').send_keys(
            self.username)
        # 反爬
        time.sleep(1)
        self.driver.find_element_by_xpath(
            '//form/section[@class="box"]/div[@class="input-wrapper"]/p[@class="input-box"]/input[@type="password"]').click()
        self.driver.find_element_by_xpath(
            '//form/section[@class="box"]/div[@class="input-wrapper"]/p[@class="input-box"]/input[@type="password"]').send_keys(
            self.password)
        time.sleep(1.5)
        self.driver.find_element_by_id("loginAction").click()
        time.sleep(3)
        print("登录成功，请点击按钮")
        try:
            self.geetest_btn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'geetest_wait')))
            print("geetest_btn is existent")
            time.sleep(1)
            # 这里可以通过模拟用户悬停移动点击按钮动作，减少验证（因为时间原因没有编写）
            self.driver.find_element_by_class_name("geetest_btn").click()
            # 判断是否有验证出现
            if EC.presence_of_element_located((By.CLASS_NAME, "geetest_wrap")):
                print("有验证,请手工解决!!!")
                time.sleep(10)
                flag = 1
        finally:
            if flag == 0:
                print("未找到相关验证,页面跳转主页面")
            # driver.quit()
        # 等待页面加载（有页面跳转，所以时间长一点）
        time.sleep(5)

    def after_login(self, url1):
        print("登录成功！访问url:%s" % url1)
        # 访问所给的爬取页面
        self.driver.get(url1)
        # 浏览器加载页面并渲染需要时间
        time.sleep(5)
        # 访问该页面的评论页面（返回的是json数据格式），下一页评论参数由当前页最后max_id决定
        if self.max_id == 0:
            self.driver.get("https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0".format(self.detail_id, self.detail_id))
        else:
            self.driver.get("https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id={}&max_id_type=0".format(self.detail_id, self.detail_id, self.max_id))
        cookies = self.driver.get_cookies()
        self.list_cks = self.get_cks(cookies)
        X_token = self.list_cks['XSRF-TOKEN']
        print(X_token)
        # 这个cookies才是最后requests需要的
        print('访问评论页面得cookies:', self.list_cks)
        # 获取当前网页源码
        str = self.driver.page_source
        # 返回源码带了html的标签，我们只要中间的json数据，采用字符串切片
        str = str[84:-20]
        # json.loads() 将已编码的 JSON 字符串解码为 Python 对象
        # json.dumps() 将 Python 对象编码成 JSON 字符串格式
        html = json.loads(str)
        # 在返回的json后面找下一页的参数max_id
        # 已缓存的数据再次访问(浏览器或者程序)会返回{'OK':0}
        if html['ok'] == 0:
            print('数据已缓存')
            self.max_id = 0
        else:
            self.max_id = html['data']['max_id']  # 获取到max_id
            print("*" * 15)
            print("下一页max_id是：", html['data']['max_id'])
        return X_token

    def get_cks(self, cookies):
        # selenium获取到的cookies是一个列表，内嵌字典格式！
        self.list_cks = {}
        self.cookie = cookies
        for cks in self.cookie:
            name = cks['name']
            value = cks['value']
            self.list_cks[name] = value
        print("当前的cookies：", self.list_cks)
        return self.list_cks

    def comment_spider(self):
        self.comment_url = "https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id={}&max_id_type=0".format(self.detail_id, self.detail_id, self.max_id)
        self.header = {'User-agent': self.ua}
        self.data = {
            'id:': self.detail_id,
            'mid:': self.detail_id,
            'max_id:': self.max_id,
            'max_id_type:': '0',
            'X-XSRF-TOKEN:':self.token}
        self.session = requests.session()
        self.comment_response = self.session.post(url=self.comment_url, headers=self.header, data=self.data)
        print('当前的comment_url的状态:', self.comment_response.status_code)

        # ???????要加cookies！！！！！

        print(self.comment_response.content)
        html = json.loads(self.comment_response.content)
        # print(html)
        if (html['ok'] != 0):
            self.max_id = html['data']['max_id']  # 获取到max_id
            print("*" * 15)
            print("下一页max_id是：", html['data']['max_id'])
            try:
                for i in range(20):
                    str = html['data']['data'][i]['text']
                    p = re.compile('<[^>]+>')
                    str1 = p.sub("", str)
                    newflag = 1
                    for j in self.hideword:
                        if str1.find(j) != -1 or len(str1) > 80:
                            newflag = 0
                            print("【过滤关键字为：%s】" % j)
                            break
                        else:
                            newflag = 1
                            continue
                    if (newflag == 1):
                        print(str1)
                        self.comment_list.append(str1 + '\n')
            except:
                print("本页评论少于20条,爬取完毕")
        else:
            print("数据已缓存")


    def run(self):

        self.url1, self.detail_id = self.wb_urlneat(url1)
        self.login_in()
        self.token = self.after_login(self.url1)
        # 到此步骤，相应的cookies和max_id都有了，下面可以继续用selenium通过翻页获取评论
        # 或者采用用requests爬取（效率更高）访问新的爬取页面也是可以的不用在重新登录
        for i in range(5):
            self.comment_spider()
        input("please input anykey to continue...")
        self.driver.quit()

if __name__ =='__main__':
    spider = weibo_spider()
    spider.run()
