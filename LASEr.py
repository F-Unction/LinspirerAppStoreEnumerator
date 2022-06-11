#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import datetime
import time
import requests
import threading
import platform
import argparse

writing = []
sys = platform.system()
mac="4a"
email='null'
header={
		'Range': 'bytes=0-0',
        'user-agent': "okhttp/3.10.0"
		}
class downloadThread (threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id = id
    def run(self):
        try:
            download(self.id)
        except Exception:
            log(self.id, "ERROR")
            raise Exception
            
def download(id):
    url = "https://cloud.linspirer.com:883/download.php?email="+email+"&appid="+str(id)+"&swdid="+mac+"&version=140"
    res = requests.head(url, stream=True,headers=header)
    try:
        url=res.headers['Location']
        print(url) 
    except:
        print("id:",str(id),"null")
        return
    res = requests.get(url,timeout=None)
    with open("./packages/"+str(id)+".apk", "wb") as f:
        f.write(res.content)

    text = os.popen("java -jar GetAPKInfo.jar ./packages/" +
                    str(id)+".apk").read()
    packageName = text[text.find(
        "包名: ")+4:text.find("\n", text.find("包名: ")+4)]
    versionName = text[text.find(
        "版本名: ")+4:text.find("\n", text.find("版本名: ")+4)]
    
    log(id, "package name "+packageName+' '+versionName)
    
    f.close()
    output(str(id), packageName+' '+versionName)
    if sys == "Windows":
        pass
        #os.system("del packages\\"+str(id)+".apk")
    else :
        os.system("rm ./packages/"+str(id)+".apk")

def log(id, message):
    print("["+datetime.datetime.now().strftime("%H:%M:%S")+"]" +
          "["+str(id)+"]:", message)


def output(id, package):
    global writing
    writing.append([id, package])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='请传入三个整数')
    parser.add_argument('begin_id', type=int, help='起始id')
    parser.add_argument('end_id', type=int, help='结束id')
    parser.add_argument('threads', type=int, help='线程数')
    parser.add_argument('run_time', nargs='?', type=int, help='运行时间(秒 可不填)',default=None)
    args = parser.parse_args()

    beg = args.begin_id
    end = args.end_id
    threads = args.threads
    now = beg-1
    run_time = args.run_time

    if not os.path.exists("./packages"):
        os.mkdir("./packages")

    while now < end:
        if threading.activeCount() <= threads:
            downloadThread(now+1).start()
            now = now+1

        if len(writing):
            f = open("./result.txt", "a")
            f.write(writing[0][0]+" \t"+writing[0][1]+"\n")
            writing.pop(0)
            f.close()
    if run_time is None:
        while threading.activeCount() != 0:
            pass
    else:
        time.sleep(run_time)
        exit(0)
