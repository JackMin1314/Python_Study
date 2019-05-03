from wxpy import *
import my_spider as it_home
import weibo_spider as weibo
import os
import random
# version2

bot = Bot()
# bot = Bot(console_qr=True, cache_path=True)
print('登录成功!')
# bot.file_helper.send('come back')
my_friends = bot.friends()
print(my_friends)
my_friend = bot.friends().search('TEST')[0]
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
                it_home.hideword = ['it', '王跃', '爱否', '今晚', '封面', 'htm', '赌', '篇', '图片', '第五', '第四', '嫖娼', '单位', '强奸', '起诉',
                '律师', '@', '没人', '信用卡', '股市', '川普', '赌博', '花呗', '套现', '贷款', '税', '青岛', '小便', '贪腐', '上访',
                '贪污', '腐败', '不公平', 'IT', '玄隐', '“', '第一', '第二', '第三', '”', '政府', '特朗普', '上车', '股票', '沙发',
                '马云', '资源', '楼', '铺路', '刺客', '实习', '评论', '热评', '尾巴', '微博', '之家', '小编', '水', '文章', '新闻', '编辑',
                '标题', '价值', '家友', '权利', '权力', '剥削', 'www', '圈子', "打工嫌累"]  # 添加过滤评论关键字例如：hideword = ["傻逼", "sb", "儿子"]
                it_home.item = {}
                it_home.commentlist = []
                it_home.page_start = 1
                it_home.url = msg.text  # 【手机分享要爬取的某个热点话题链接】https://m.ithome.com/html/419302.htm
                it_home.url = it_home.it_urlneat(it_home.url)  # 被别的模块导入的时候再调用
                it_home.news_id = it_home.url[24:-4].replace('/', '')  # 从url构造获取NewsId
                it_home.headers, it_home.comment_num, it_home.cookies = it_home.it_details(it_home.url)
                it_home.comment_url = 'https://dyn.ithome.com/comment/{}'.format(it_home.comment_num)  # 构造评论页面comment_url 得到cookies，headers访问数据页面,获取hash，
                it_home.ajax_url = 'https://dyn.ithome.com/ithome/getajaxdata.aspx'  # 根据对应url获取newsID，再将newsID和type数据post给接口（该url）获取返回的热评数据
                it_home.ctl_spider(it_home.page_start, it_home.url, it_home.cookies, it_home.comment_url, it_home.ajax_url, it_home.headers)
                it_home.it_save(it_home.commentlist)
                my_friend.send_file('ithome_data.txt')

            if('weibo' in msg.text):
                ua = random.choice(weibo_reply_list)
                my_friend.send(ua)
                weibo.username = '********'
                weibo.password = '********'
                weibo.url = msg.text
                weibo.login_url = 'https://passport.weibo.cn/signin/login'  # 登录页面
                weibo.login_goto_url = 'https://passport.weibo.cn/sso/login'  # 使用login_url后获取其cookie。然后在访问http://.../sso/login用post输入用户名，密码明文作为data参数传递
                weibo.url, weibo.detail_id = weibo.wb_urlneat(weibo.url)
                weibo.comment_url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0'.format(weibo.detail_id, weibo.detail_id)
                weibo.hideword = ["半夜", "台湾", "踹你一脚", "纯粹"] # 自己添加关键字
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

'''

两种方法解决unicode编码问题有些json在控制台打印也是这样的结果unicode编码
str1 = '\xe5\xa4\xa7\xe5\x93\xa5\xe8\xbf\x98\xe6\x98\xaf\xe4\xbc\x9a\xe5\x81\x9a\xe4\xba\xba\xe5\x95\x8a'
str1 = str1.encode('raw_unicode_escape')
c1=str1.decode(encoding='utf-8')
print(c1)

str2=b'\xe8\xaf\x84\xe8\xae\xba'
c = str2.decode(encoding='utf-8')
print(c)

'''