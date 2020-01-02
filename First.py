# 这是我第一次打python程序（#要后面加一个空格）
import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

user_agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
]
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

driver.get('https://dyn.ithome.com/comment/55cc349d0155b4c4')
# 微博通过navigator判断是否selenium，这里设置很重要！！！
driver.execute_script("Object.defineProperties(navigator,{webdriver:{get:() => false}})")
#pagetype = driver.find_element_by_xpath(" /html/body/div[@class='post_comment']/div[@class='comm_list']/div[@id='divLatest']/script") # /html/body/div[@class='post_comment']/div[@class='comm_list']/div[@id='divLatest']
#print(pagetype.text)

soup = BeautifulSoup(driver.page_source, 'html.parser')
pagetype = soup.text
pagetype = pagetype[pagetype.find('var pagetype = \'')+16:pagetype.find('lhcl(1)')-2]
print(pagetype)
time.sleep(1)
driver.close()
driver.quit()
