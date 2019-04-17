from wxpy import *
import my_spider as it_home
import weibo_spider as weibo
import os
import random

bot = Bot(cache_path=True)
# bot = Bot(console_qr=True, cache_path=True)
print('登录成功!')
# bot.file_helper.send('come back')
my_friends = bot.friends()
print(my_friends)
my_friend = bot.friends().search('null')[0]
print(my_friend)



@bot.register(my_friend)
def reply_myfriend(msg):

    it_reply_list=['识别为it之家的链接，正在爬取请稍等','小的看是it之家的链接，先去了','it，it，go,go!','it,wait,wait,wait','Found it_home!莫急','it之家吗?我去找了...']
    weibo_reply_list = ['识别为weibo的链接，正在爬取请稍等', '小的看是weibo的链接，先去了', 'weibo，weibo，go,go!', 'weibo,wait,wait,wait', 'Found weibo!莫急', 'weibo吗?我去找了...']

    try:
        if msg.type=='Text':
            my_friend.send('收到内容：{}'.format(msg.text))
            if('ithome' in msg.text):
                ua = random.choice(it_reply_list)
                my_friend.send(ua)
                it_home.hideword = ['耍', '厚道', '雷老板', '牛叉', "打工嫌累", "可以", "一楼"]  # 添加过滤评论关键字例如：hideword = ["傻逼", "sb", "儿子"]
                it_home.item = {}
                it_home.commentlist = []
                it_home.page_start = 1
                it_home.url = msg.text  # 【手机分享要爬取的某个热点话题链接】https://m.ithome.com/html/419302.htm
                it_home.url = it_home.it_urlneat(it_home.url)  # 被别的模块导入的时候再调用
                it_home.news_id = it_home.url[24:-4].replace('/', '')  # 从url构造获取NewsId
                it_home.url = 'https://dyn.ithome.com/comment/{}'.format(it_home.news_id)  # 构造评论页面url
                it_home.urls = 'https://dyn.ithome.com/ithome/getajaxdata.aspx'  # 根据对应url获取newsID，再将newsID和type数据post给接口（该url）获取返回的热评数据
                it_home.headers, it_home.myhash = it_home.it_details(it_home.url)
                it_home.ctl_spider(it_home.page_start, it_home.urls, it_home.headers, it_home.myhash)
                it_home.it_save(it_home.commentlist)
                my_friend.send_file('ithome_data.txt')

            if('weibo' in msg.text):
                ua = random.choice(weibo_reply_list)
                my_friend.send(ua)
                weibo.username = '********'
                weibo.password = '*******'
                weibo.url = "https://m.weibo.cn/7071727554/4359821799321366"
                weibo.login_url = 'https://passport.weibo.cn/signin/login'  # 登录页面
                weibo.login_goto_url = 'https://passport.weibo.cn/sso/login'  # 使用login_url后获取其cookie。然后在访问http://.../sso/login用post输入用户名，密码明文作为data参数传递
                weibo.url, weibo.detail_id = weibo.wb_urlneat(weibo.url)
                weibo.comment_url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0'.format(weibo.detail_id, weibo.detail_id)
                weibo.hideword = ["半夜", "台湾", "踹你一脚", "纯粹"]
                weibo.commentlist = []
                weibo.page_start = 1  # 爬取第一个页面
                weibo.page_end = 5  # 爬取最后一个页面（由总评论可以计算，为了方便人为规定）
                weibo.max_id1 = 0
                weibo.session, weibo.cookies, weibo.max_id1 = weibo.wb_details(weibo.comment_url, weibo.detail_id, weibo.url)
                weibo.ctl_wb_spider(weibo.page_start, weibo.page_end + 1, weibo.detail_id, weibo.max_id1, weibo.username, weibo.password)
                weibo.wb_save(weibo.commentlist)
                my_friend.send_file('weibo_data.txt')

        if('退出' in msg.text):
            return '手动关闭服务器程序或者Android客户端！'
    except:
        return '链接错误,请检查重发正确链接!'

embed()
