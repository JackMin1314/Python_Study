# -*- coding: utf-8 -*-
# @Time    : 2019/5/3
# @Author  : 陈王
# @FileName: my_spider.py
# @Software: windows、Pycharm、Python3
# 转载请注明出处 @blog    : https://github.com/JackMin1314/Python_Study

import requests
import random
from bs4 import BeautifulSoup
import time
import datetime
import json


def it_urlneat(url):
    url= url
    if(url[8]=='m'):        # 解决手机it之家链接问题
        id=url[url.find('/html')+6:-4]
        url1=id[0:3]
        url2=id[3:]
        url='https://www.ithome.com/0/{}/{}.htm'.format(url1, url2)
    else:
        url=url
    commentlist.append(url)
    return url

def it_details(url):
    user_agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    ]
    ua = random.choice(user_agent_list)    # 随机从代理池选择
    headers = {'User-agent': ua}        # 构造headers,代理
    result = requests.post(url=url, headers=headers)
    result_str = str(result.content)  # 直接强制类型转换为str，方便提取
    comment_num = result_str[result_str.find('iframe align="middle" data=') + 28:result_str.find('datalapin ="0" scrolling="no"') - 2]

    cookies = str(result.cookies)  # 当使用post方法的时候cookies才能获得，改个headers就行
    asp_net_sessionid = cookies[cookies.find('ASP.NET_SessionId='):cookies.find(' for')]
    BEC = cookies[cookies.find('BEC='):cookies.find('/>]') - 19]
    cookies = asp_net_sessionid + ';' + BEC  # 这里的cookies必须要严格构造
    return headers, comment_num, cookies

def crazy_spider(news_id,ajax_url,headers,myhash,page):
    ajax_data = {
        'newsID': news_id,
        'hash': myhash,  #
        'type': 'commentpage',
        'page': page,  #
        'order': 'false'
    }
    ajax_result = requests.post(url=ajax_url, headers=headers, data=ajax_data)
    print("当前链接状态：{}".format(ajax_result.status_code))
    soup = BeautifulSoup(ajax_result.content, 'html.parser')  # xpath拿不到数据？因为返回的格式是json！(ajax不能使用xpath直接拿标签)
    li_list = soup.find_all('li', class_='entry')
    # print(len(li_list))   查看目前it_home评论一页50个
    # response.text用json.loads()格式化，并取出html，最后再用BeautifulSoup()格式化一下，评论的各个数据就很容易取出来
    if len(ajax_result.content)==0:
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
            if mystr.find(i) != -1 or len(mystr)>80:     #   长度？
                flag = 0
                print("【过滤关键字为：%s】" % i)
                break
            else:
                flag = 1
                continue
        if(flag==1):
            print(mystr)
            commentlist.append(mystr)

def it_save(commentlist):
    file=open('ithome_data.txt', 'w', encoding="utf-8")        # 打开格式为utf-8.垃圾Windows默认打开gbk格式。
    for line in commentlist:
        file.write(line+'\n')
    file.close()

def ctl_spider(page_start,url,cookies,comment_url,ajax_url, headers):
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    ]
    ua = random.choice(user_agent_list)  # 随机从代理池选择
    news_id = url[24:-4].replace('/', '')  # 从url构造获取NewsId
    comment_data = {
        'Cookie': cookies,
        # 'ASP.NET_SessionId=shkniyq40o5h45rvvwd1vnqt; BEC=228f7aa5e3abfee5d059195ad34b4137|1556702302|1556702302',#直接添加也可以
        'Host': 'dyn.ithome.com',
        'Referer': url,
        'Upgrade-Insecure-Requests': 1,
        'User-Agent': ua
    }  # 构造comment_data
    comment_result = requests.post(url=comment_url, data=comment_data)
    comment_result_str = str(comment_result.content)
    comment_result_str.find('var pagetype = \\')
    temp = comment_result_str[comment_result_str.find('var pagetype = \\'):]
    myhash = temp[temp.find('\\\'') + 2:temp.find(';') - 2]

    t = 0
    for page in range(page_start, page_start + 3):
        # 这里可以控制爬多少。js前端用字符串？
        try:
            t1 = crazy_spider(news_id, ajax_url, headers, myhash, page)
            if (t1 == 2):
                t = 2
        except:
            print("Post请求失败！")
            t = t + 1
        if (t == 2):  # 超时结束或者评论爬取完毕
            break
        time.sleep(random.randint(3, 5))  # 控制爬取间隔时间，反爬

if __name__ == '__main__':
    # commentstr = ''
    hideword = ['it', '王跃', '爱否', '今晚', '封面', 'htm', '赌', '篇', '图片', '第五', '第四', '嫖娼', '单位', '强奸', '起诉',
                '律师', '@', '没人', '信用卡', '股市', '川普', '赌博', '花呗', '套现', '贷款', '税', '青岛', '小便', '贪腐', '上访',
                '贪污', '腐败', '不公平', 'IT', '玄隐', '“', '第一', '第二', '第三', '”', '政府', '特朗普', '上车', '股票', '沙发',
                '马云', '资源', '楼', '铺路', '刺客', '实习', '评论', '热评', '尾巴', '微博', '之家', '小编', '水', '文章', '新闻', '编辑',
                '标题', '价值', '家友', '权利', '权力', '剥削', 'www', '圈子', "打工嫌累"]  # 添加过滤关键字例如：hideword = ["傻逼", "sb", "儿子"]
    item = {}
    commentlist = []
    page_start = 1
    url = "https://www.ithome.com/0/421/049.htm"  #   能找到 iframe align="middle" data=； 324f9add8e997e46，但是#document（包括评论页面参数，hash）以及评论链接不在返回数据里
    url = it_urlneat(url)
    news_id = url[24:-4].replace('/', '')  # 从url构造获取NewsId
    headers, comment_num, cookies = it_details(url)
    comment_url = 'https://dyn.ithome.com/comment/{}'.format(comment_num) # 构造评论页面comment_url 得到cookies，headers访问数据页面,获取hash，
    ajax_url = 'https://dyn.ithome.com/ithome/getajaxdata.aspx'  # 根据对应url获取newsID，再将newsID和type数据post给接口（该url）获取返回的热评数据
    ctl_spider(page_start, url, cookies, comment_url, ajax_url, headers)
    it_save(commentlist)


# 下面注释不要删除！这里跟__name__=='__main__'内容一致，本程序单独运行时不用考虑main，作为模块被别人使用时，main内部内容不被执行,故将下面注释去掉即可
hideword = ['it', '王跃', '爱否', '今晚', '封面', 'htm', '赌', '篇', '图片', '第五', '第四', '嫖娼', '单位', '强奸', '起诉',
                '律师', '@', '没人', '信用卡', '股市', '川普', '赌博', '花呗', '套现', '贷款', '税', '青岛', '小便', '贪腐', '上访',
                '贪污', '腐败', '不公平', 'IT', '玄隐', '“', '第一', '第二', '第三', '”', '政府', '特朗普', '上车', '股票', '沙发',
                '马云', '资源', '楼', '铺路', '刺客', '实习', '评论', '热评', '尾巴', '微博', '之家', '小编', '水', '文章', '新闻', '编辑',
                '标题', '价值', '家友', '权利', '权力', '剥削', 'www', '圈子', "打工嫌累"]  # 添加过滤关键字例如：hideword = ["傻逼", "sb", "儿子"]
item = {}
commentlist = []
page_start = 1
url = "https://www.ithome.com/0/421/049.htm"  #   能找到 iframe align="middle" data=； 324f9add8e997e46，但是#document（包括评论页面参数，hash）以及评论链接不在返回数据里
# url=it_urlneat(url)       # 被别的模块导入的时候再调用
news_id = url[24:-4].replace('/', '')  # 从url构造获取NewsId
# headers, comment_num, cookies = it_details(url)
# comment_url = 'https://dyn.ithome.com/comment/{}'.format(comment_num) # 构造评论页面comment_url 得到cookies，headers访问数据页面,获取hash，
ajax_url = 'https://dyn.ithome.com/ithome/getajaxdata.aspx'  # 根据对应url获取newsID，再将newsID和type数据post给接口（该url）获取返回的热评数据
# ctl_spider(page_start, url, cookies, comment_url, ajax_url, headers)
# it_save(commentlist)



