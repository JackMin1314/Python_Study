import sys
import os
import datetime
import time
import importlib

def shutdown(seconds):
    now_time1 = datetime.datetime.now()
    now_time1 = now_time1.replace(microsecond=0)
    print("您的电脑将在: {} 关机".format(now_time1 + datetime.timedelta(seconds=seconds)))   # 时间增量seconds（minute，hour）

    try:
       os.system("shutdown -s -t {}".format(seconds))
    except OSError:
       os.system("shutdown -a")

def main():
    now_time = datetime.datetime.now()
    now_time = now_time.replace(microsecond=0)  # microseconds    用来表示替代原有微妙属性，为0表示微秒是0，不用精确到微秒。
    print("当前的时间是：{}".format(now_time))
    hour = input("输入关机延迟时间（h）：")
    print("您输入的时间是：{}h".format(hour))
    time.sleep(1)   # 等待1秒后运行后面
    shutdown(float(hour)*3600)

if __name__ == '__main__':
    main()


