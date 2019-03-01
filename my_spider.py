from lxml import etree
import requests     # 网络请求
import random
import bs4
import time
# urls = 'https://dyn.ithome.com/comment/411836'    # 仅独立的评论页面

'''
    https://dyn.ithome.com/ithome/getajaxdata.aspx 通过 ajax 来动态加载内容
    肯定文章 url 不变，getajaxdata.aspx 用来获取评论的，因而内部指向了 Referer: https://dyn.ithome.com/comment/411836
    通过多个 getajaxdata.aspx 的 From Data 可看到请求页面page=1,2,...
    总评论数正文下方有 //*[@id="commentcount"]
    某条的评论内容 //*[@id="ulcommentlist"]/div[1]/li[1]/div[2]/div[2]/p/text()   xpath路径   
    
'''

url = "https://www.ithome.com/0/411/836.htm"
news_id = url[24:-4].replace('/', '')
print(news_id)

page_start = 1
user_agent_list = [
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    ]
ua = random.choice(user_agent_list)    # 随机从代理池选择
data = {
    'hash': '62DB0D67CE5B027D',
    'type': 'commentpage',
    'page': '1',
    'newsID': '411836',
    'User-agent': ua
}       # 构造data

for page in range(page_start, page_start + 11):
    data['page'] = str(page)
    try:
        r = requests.post('https://dyn.ithome.com/ithome/getajaxdata.aspx', data=data)
        print(r)
        r.encoding = r.apparent_encoding

        # ?????

    except:
        print("Post请求失败！")
        exit()
    time.sleep(1)
print(r)
# response = requests.get(urls)
# print(response.status_code)
# print(response.content)
print("ok")
