'''
@FileName   :  微信公众号爬虫.py
@Author     : Chen Wang
@Version    : Python3.X 、Windows or Linux
@Description:  利用搜狗的接口爬取指定微信公众号
@Time       : 2019/7/19 21:53
@Software   : PyCharm
@Contact    : 1416825008@qq.com
@Blog       : https://github.com/JackMin1314/Python_Study
代 码 仅 限 学 习 ，严 禁 商 业 用 途，转 载 请 注 明 出 处

'''
# import lib
import requests
import time
import random
import pymysql
# pip install PyExecJS
# import execjs
import math
from lxml import etree

# 存微信号
Titles = []
# 存微信认证
WeixinAuthority = []
# 存最近文章
SoonArticle = []
# 保存全部的信息
power = []
UserAgentList = [
    "Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)", ]
ua = random.choice(UserAgentList)


class SoGouWeiXin():
    # 初始化相关参数
    def __init__(self):
        self.KeyWords = input("请输入要爬取公众号的关键字: ")
        self.sut = ""
        self.sst0 = ""
        # 生成13位时间戳
        self.sst0 = time.time() * 1000
        # 首次访问的url跟后面的不一样,为了获取页脚
        self.url = "https://weixin.sogou.com/weixin?type=2&s_from=input&query={}&ie=utf8&_sug_=n&_sug_type_=".format(
            self.KeyWords)

    # 构造修改data,header,需要self.page
    def myDetails(self):
        self.headers = {
            "Connection": "keep-alive",
            "Host": "weixin.sogou.com",
            "Referer": self.url,
            "User-Agent": ua,
            "Upgrade-Insecure-Requests": "1", }
        self.data = {
            "type": "1",
            "s_from": "input",
            "query": self.KeyWords,
            "ie": "utf8",
            # "_sug_": "n",
            "_sug_type_": "",
        }
        # 传过来是后面的页面url,修改header和data
        if "page" in self.url:
            # 有则不改动,无则添加;都需要返回值
            a = self.data.setdefault("page", str(2))
            self.data["page"] = str(self.page)
            a = self.data.setdefault("dr", "1")

    # 一个页面的请求构造
    def spider(self):
        # proxy = {'https':'https://163.204.240.217:9999','http':'http://163.204.240.217:9999',
        #          # 'http':'27.43.185.209:9999','https':'27.43.185.209:9999'
        #          }
        # pxy = {'https':'https://27.43.185.209'}
        self.session = requests.Session()
        self.session.post(url="https://weixin.sogou.com/new/pc/images/sousuo01_2.png", headers=self.headers,
                          data=self.data)
        # print("当前请求的状态为:%s" % result)
        self.session.get(url="https://news.sogou.com/news?ie=utf8&p=40230447", headers=self.headers, data=self.data)
        self.result = self.session.post(url=self.url, headers=self.headers, data=self.data)
        print('URL:' + self.result.url)
        print("当前URL请求的状态为:%s" % self.result)
        print(self.result.content)
        self.content = etree.HTML(self.result.content)
        # 第一个页面跟后面的url不一样，后面的才需要调用处理函数
        if 'page' in self.url:
            self.DealWithContent()

    # 一个页面的爬取
    def DealWithContent(self):
        # 页数
        self.pageFoot = len(self.content.xpath('//*[@id="pagebar_container"]/a/text()'))
        print('页数:%s' % self.pageFoot)
        # 获取公众号列表每次最多10个,不足列表空
        # 可以在下面添加需要爬去的其他数据
        for li in range(10):
            # 微信号
            self.weixinNum = self.content.xpath(
                '//*[@id="sogou_vr_11002301_box_{}"]/div/div[2]/p[2]/label[@name="em_weixinhao"]/text()'.format(li))
            # 最近文章
            self.soonArticle = self.content.xpath('//*[@id="sogou_vr_11002301_box_{}"]/dl[3]/dd/a/text()'.format(li))
            if self.soonArticle==[]:
                self.soonArticle = self.content.xpath('//*[@id="sogou_vr_11002301_box_{}"]/dl[2]/dd/a/text()'.format(li))
            print('最近文章%s'% self.soonArticle)
            #//*[@id="sogou_vr_11002301_box_4"]/dl[2]/dd/a
            #//*[@id="sogou_vr_11002301_box_6"]/dl[2]/dd/a
            # 微信认证
            self.weixinAuthority = self.content.xpath('//*[@id="sogou_vr_11002301_box_{}"]/dl[2]/dd/text()'.format(li))

            # 添加到list
            Titles.extend(self.weixinNum)
            SoonArticle.extend(self.soonArticle)
            WeixinAuthority.extend(self.weixinAuthority)
            total_str = '微信号:{str1:<{len}}\t最近文章:{str2:<{len2}}\t微信认证:{str3}'.format(str1=str(self.weixinNum), len=22, str2=str(self.soonArticle),len2=50,str3=str(self.weixinAuthority) + '\n')
            power.append(total_str)

    # 保存为txt文件
    def save_wxgzh(self):
        with open('wx_gzh_{}'.format(self.KeyWords), mode='w', encoding='utf-8') as f:
            for li in power:
                f.write(li)
                print(li)
            f.close()

    # 调度台控制整个过程
    def run(self):
        # 控制循环次数
        for self.page in range(10):
            if self.page == 0:
                self.url = self.url
                print(self.url)
            else:
                self.url = "https://weixin.sogou.com/weixin?query={}&_sug_type_=&s_from=input&_sug_=n&type=1&page={}&ie=utf8".format(
                     self.KeyWords, self.page)
            time.sleep(random.choice([2, 3, 4]))
            self.myDetails()
            self.spider()
            time.sleep(random.choice([2, 5, 3, 4, 5]))
        self.save_wxgzh()


if __name__ == "__main__":
    sp = SoGouWeiXin()
    sp.run()
