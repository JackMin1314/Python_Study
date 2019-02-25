from selenium import webdriver
import datetime

# print("hello"),注释要加‘#’并且后添加空格
starttime = datetime.datetime.now()# 获取当前时间

browser = webdriver.Chrome(executable_path = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')# 启动指定目录下的Chrome的驱动程序（版本要对应）
browser.get("http://www.baidu.com")# 访问某个网站

endtime = datetime.datetime.now()# 获取当前时间
alter = starttime-endtime
print(alter.total_seconds())# 启动并访问用时（秒）
