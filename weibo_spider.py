# -*- coding: utf-8 -*-
# @Time    : 2019/4/10
# @Author  : 陈王
# @FileName: weibo_spider.py
# @Software: windows、Pycharm、Python3
# @blog    : https://github.com/JackMin1314/Python_Study
# 感谢https://blog.csdn.net/xiaopang123__/article/details/79001426;https://blog.csdn.net/rosepicker/article/details/77882154的帮助
import requests
import random
from bs4 import BeautifulSoup
import json
import re
import time


def wb_urlneat(url):
    url = url        # 【添加手机上要爬取的微博正文】
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
    print(detail_id)
    return url, detail_id

def wb_details(comment_url,detail_id,url):
    user_agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    ]
    ua = random.choice(user_agent_list)    # 随机从代理池选择
    header = {'User-agent': ua}        # 构造headers,代理
    # 访问所给链接获取cookie# cookie = response.headers['Set-Cookie']
    response = requests.post(url)  # 先访问下获取cookie
    cookie = response.cookies
    data = {
        'id:': detail_id,
        'mid:': detail_id,
        'max_id_type:': 0,
        'cookie:': cookie,
        'upgrade-insecure-requests:': 1,
        'user-agent:': ua,
        'sudaref': 'm.weibo.cn',
        # 'display': 0,
        # 'retcode': 6102
        }  # 构造data
    session = requests.session()        # 局部变量？函数调用结束，会导致回话结束吗？
    response = requests.post(url=url, headers=header, data=data)        # 模拟访问url
    soup = BeautifulSoup(response.text, 'html.parser')
    # li_list = soup.find_all('li', class_='entry')
    script_list = soup.find_all('script')  # class beautiful4 Resultset字典外套了列表
    str = script_list[1]
    mid = str.text[341:357]
    id = mid
    # print('id=mid:'+mid)
    index1 = str.text.find('"reposts_count"')
    index3 = str.text.find('"attitudes_count"')
    index2 = str.text.find('"comments_count"')
    index4 = str.text.find('"pending_approval_count"') - 10
    # print(str.text[index1:index4])
    reposts_count = '转发量：' + str.text[index1 + 16:index2 - 10] + '    '  # 转发量
    comments_count = '评论量：' + str.text[index2 + 17:index3 - 10] + '   '  # 评论量
    attitudes_count = '点赞数：' + str.text[index3 + 18:index4] + '   '  # 点赞数
    total = reposts_count+comments_count+attitudes_count
    commentlist.append(total+'\n')
    print(reposts_count, comments_count, attitudes_count)
    result = session.get(url=comment_url, headers=header, data=data) # 获取到max_id
    html = json.loads(result.text)
    print(html)
    max_id=html['data']['max_id']       # 获取到max_id
    print(html['data']['max_id'])
    if (html['ok'] != 0):
        try:
            for i in range(20):
                print(html['data']['data'][i]['text'])
                str=html['data']['data'][i]['text']
                str = str[0:(str.find('<span'))]
                commentlist.append(str + '\n')
        except:
            print("本页评论少于20条")
    else:
        print("数据已缓存")
    return session, cookie, max_id

def wb_spider(detail_id, newcomment_url, username, password):
    comment_url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0'.format(detail_id, detail_id) # 为了login_goto_data
    # newcomment_url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id={}&max_id_type=0'.format(detail_id, detail_id, max_id)# 已缓存的数据再次访问(浏览器或者程序)会返回{'OK':0}
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    ]
    ua = random.choice(user_agent_list)  # 随机从代理池选择
    header = {'User-agent': ua}

    data = {
        'id:': detail_id,
        'mid:': detail_id,
        'max_id_type:': 0,
        # 'cookie:': cookie,
        'upgrade-insecure-requests:': 1,
        'user-agent:': ua,
        'sudaref': 'm.weibo.cn',
        # 'display': 0,
        # 'retcode': 6102
    }  # 构造data
    login_goto_data = {
    'username': username,
    'password': password,
    'savestate': '1',
    'r': comment_url,
    'ec': '0',
    'pagerefer': '',
    'entry': 'mweibo',
    'wentry': '',
    'loginfrom': '',
    'client_id': '',
    'code': '',
    'qq': '',
    'mainpageflag': '1',
    'hff': '',
    'hfp': ''
    }
    login_goto_headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
            'Accept':'text/html;q=0.9,*/*;q=0.8',
            'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Connection':'close',
            'Referer':'https://passport.weibo.cn/signin/login',
            'Host':'passport.weibo.cn'
                }
    session = requests.session()
    login_goto_response = session.post(url=login_goto_url, headers=login_goto_headers, data=login_goto_data)       # 模拟登录成功页面,局部变量？函数调用结束，会导致回话结束吗？
    result = session.get(url=newcomment_url, headers=header, data=data)
    # print(result.url)
    # print(result)
    print(result.text)
    html = json.loads(result.text)
    print(html)
    t=0
    if html['ok']==0:
        print('数据已缓存')
        max_id=0
    else:
        max_id=html['data']['max_id']       # 获取到max_id
        print(html['data']['max_id'])
    if(html['ok']!=0):
        try:
            for i in range(20):
                str = html['data']['data'][i]['text']
                str1 = str[0:(str.find('<span'))]
                flag = 1
                for j in hideword:
                    if str1.find(j) != -1:
                        flag = 0;
                        break;
                    else:
                        flag = 1;
                        continue;
                if (flag == 1):
                    str1 = str1[0:(str.find('<a'))]
                    print(str1)
                    commentlist.append(str1+'\n')

        except:
            t=2
            print("本页评论少于20条,爬取完毕")
    else:
        print("数据已缓存")
    return max_id, t

def ctl_wb_spider(page_start,page_end,detail_id,max_id1,username, password):
    t=0;
    max_id=max_id1
    for page in range(page_start, page_end):
        # 这里可以控制爬多少。js前端用字符串？
        newcomment_url='https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id={}&max_id_type=0'.format(detail_id, detail_id,max_id)
        try:
            md,t1 = wb_spider(detail_id, newcomment_url, username, password)
            if (t1 == 2):
                t = 2
        except:
            print("Post请求失败！")
            t = t + 1
        max_id = md
        if (t == 2):  # 超时结束或者评论爬取完毕
            break;
        time.sleep(random.randint(2, 4))  # 控制爬取间隔时间，反爬

def wb_save(commentlist):
    file=open('weibo_data.txt', 'w', encoding="utf-8")        # 打开格式为utf-8.垃圾Windows默认打开gbk格式。
    for line in commentlist:
        line =line.strip()
        if line:
            line = line+'\n'
        file.write(line)
    file.close()

if __name__=='__main__':
    username = '******'
    password = '********'
    url = "https://m.weibo.cn/7071727554/4359821799321366"
    login_url = 'https://passport.weibo.cn/signin/login'  # 登录页面
    login_goto_url = 'https://passport.weibo.cn/sso/login'  # 使用login_url后获取其cookie。然后在访问http://.../sso/login用post输入用户名，密码明文作为data参数传递
    url, detail_id = wb_urlneat(url)
    comment_url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0'.format(detail_id, detail_id)
    hideword=["半夜", '台湾', '踹你一脚', '纯粹']
    commentlist = []
    page_start=1        # 爬取第一个页面
    page_end=5          # 爬取最后一个页面（由总评论可以计算，为了方便人为规定）
    max_id1=0
    session,cookies,max_id1=wb_details(comment_url,detail_id, url)
    ctl_wb_spider(page_start,page_end+1,detail_id,max_id1,username, password)
    wb_save(commentlist)
