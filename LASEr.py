#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import datetime
import time
import requests
import threading
import platform
import argparse
import random

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
    url = "https://cloud.linspirer.com:883/download.php?email="+email+"&appid="+str(id)+"&swdid="+mac+"&version="+str(random.randint(1,9000000))
    realurl="Null"
    res = requests.head(url, stream=True,headers=header)
    try:
        url=res.headers['Location']
        print(url) 
        realurl=url
    except:
        print("id:",str(id),"null")
        return
    res = requests.get(url,timeout=None)
    with open("./packages/"+str(id)+".apk", "wb") as f:
        f.write(res.content)

    text = os.popen("java -jar GetAPKInfo_EN.jar ./packages/" +
                    str(id)+".apk").read()
    packageName = text[text.find(
        "PackageName: ")+13:text.find("\n", text.find("PackageName: ")+13)]
    versionName = text[text.find(
        "Version: ")+8:text.find("\n", text.find("Version: ")+8)]
    
    log(id, "PackageName "+packageName+' '+versionName)
    
    f.close()
    output(str(id), realurl ,packageName+','+versionName[1:])
    if sys == "Windows":
        os.system("del packages\\"+str(id)+".apk")
    else :
        os.system("rm ./packages/"+str(id)+".apk")

def log(id, message):
    print("["+datetime.datetime.now().strftime("%H:%M:%S")+"]" +
          "["+str(id)+"]:", message)

def output(id, link,package):
    global writing
    writing.append([id,link, package])
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Please run with at least 3 integers.')
    parser.add_argument('begin_id', type=int, help='Start_id')
    parser.add_argument('end_id', type=int, help='End_id')
    parser.add_argument('threads', type=int, help='Threads Count')
    parser.add_argument('run_time', nargs='?', type=int, help='Run_Time (sec)',default=None)
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
            f = open("./result.csv", "a")            
            f.write(writing[0][0]+","+writing[0][1]+","+writing[0][2]+"\n")
            writing.pop(0)
            f.close()
    if run_time is None:
        while threading.activeCount() != 0:
            pass
    else:
        time.sleep(run_time)
        exit(0)