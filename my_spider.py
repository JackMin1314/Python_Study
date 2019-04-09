# -*- coding: utf-8 -*-
# @Time    : 2019/3/3
# @Author  : 陈王
# @FileName: my_spider.py
# @Software: windows、Pycharm、Python3
# @blog    : https://github.com/JackMin1314/Python_Study

import requests
import random
from bs4 import BeautifulSoup
import time
import datetime
import json
from docx import Document
from docx.shared import Inches


# import jsonpath
# from lxml import etree      # 使用xpath,后面发现用不了！
# urls = 'https://dyn.ithome.com/comment/411836'    # 仅独立的评论页面
# 感谢https://blog.csdn.net/AmazingUU/article/details/83043592
# https://blog.csdn.net/qq_17271589/article/details/80398283 给予的帮助。

'''
    https://dyn.ithome.com/ithome/getajaxdata.aspx 通过 ajax 来动态加载内容
    肯定文章 url 不变，getajaxdata.aspx 用来获取评论的，因而内部指向了 Referer: https://dyn.ithome.com/comment/411836
    通过多个 getajaxdata.aspx 的 From Data 可看到请求页面page=1,2,...
    总评论数在正文标题下方有 //*[@id="commentcount"]
    某条的评论内容 //*[@id="ulcommentlist"]/div[1]/li[1]/div[2]/div[2]/p/text()   xpath路径   
    //ul[@class="list hot"]//li[@class="entry"]//div[@class="fodiv"]//div//p    chropath自己找的路径
    
'''
url = "https://www.ithome.com/0/418/279.htm"        # 【添加要爬取的某个热点话题链接】
news_id = url[24:-4].replace('/', '')    # 从url构造获取NewsId
url = 'https://dyn.ithome.com/comment/{}'.format(news_id)  # 构造评论页面url
urls = 'https://dyn.ithome.com/ithome/getajaxdata.aspx'    # 根据对应url获取newsID，再将newsID和type数据post给接口（该url）获取返回的热评数据

user_agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    ]

ua = random.choice(user_agent_list)    # 随机从代理池选择
headers = {'User-agent': ua}        # 构造headers,代理
response = requests.post(url)
myhash = response.text[response.text.find('ch11 = '):-1]
myhash = myhash[8: myhash.find(';')-1]      # 从返回的text文本中提取hash
page_start = 1

commentstr=''
hideword = ['耍','厚道','雷老板','牛叉',"打工嫌累","可以", "一楼"]       # 添加过滤关键字例如：hideword = ["傻逼", "sb", "儿子"]
item = {}
commentlist = []
def crazy_spider(url):
    data = {
        'newsID': news_id,
        'hash': myhash,
        'pid': 1,
        'type': 'commentpage',
        'page': str(page),
        'order': 'false'
    }  # 构造data
    response = requests.post(urls, headers=headers, data=data)
    print("当前链接状态：{}".format(response.status_code))
    content = response.text  # content是 str类型

    soup = BeautifulSoup(content, 'html.parser')  # xpath拿不到数据？因为返回的格式是json！(ajax不能使用xpath直接拿标签)
    li_list = soup.find_all('li', class_='entry')
    print(li_list)
    # response.text用json.loads()格式化，并取出html，最后再用BeautifulSoup()格式化一下，评论的各个数据就很容易取出来

    if len(content)==0:
        print('评论已经爬完！')
        return 2
    for li in li_list:
        # 分析html源码，取出热评对应数据
       # item['用户名'] = li.find('span', class_='nick').text
       # item['时间'] = li.find('span', class_='posandtime').text.split('\xa0')[1]
        item['评论'] = li.find('p').text
        mystr = li.find('p').text

        flag = 1
        for i in hideword:
            if mystr.find(i)!=-1:
                flag =0;break;
            else:
                flag=1;continue;
        if(flag==1):
            # commentstr+=mystr
            print(mystr)
            commentlist.append(mystr)


t=0;
for page in range(page_start, page_start + 11):
    # 这里可以控制爬多少。
    # js前端用字符串？
    try:
        t1=crazy_spider(url)
        if(t1==2):
            t=2
    except:
         print("Post请求失败！")
         t=t+1
    time.sleep(random.randint(3, 5))        # 控制爬取间隔时间，反爬
    if(t==2):       # 超时结束或者评论爬取完毕
        break;

print("ok")
print('*'*30)
print(commentlist)

file=open('ithome_data.txt', 'w', encoding="utf-8")        # 打开格式为utf-8.垃圾Windows默认打开gbk格式。
for line in commentlist:
    file.write(line+'\n')
file.close()
