import os
import datetime
import requests
import threading
import platform
writing = []
sys = platform.system()
mac=""

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
    url = "http://cloud.linspirer.com:880/download?appid=" + \
        str(id)+"&swdid="+mac
    res = requests.get(url,timeout=None)

    if len(res.content) < 100:
        return
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
        os.system("del packages\\"+str(id)+".apk")
    else :
        os.system("rm ./packages/"+str(id)+".apk")

def log(id, message):
    print("["+datetime.datetime.now().strftime("%H:%M:%S")+"]" +
          "["+str(id)+"]:", message)


def output(id, package):
    global writing
    writing.append([id, package])


if __name__ == "__main__":
    beg = int(input("begin with\t>"))
    end = int(input("end with\t>"))
    threads = int(input("thread number\t>"))
    now = beg-1

    if not os.path.exists("./packages"):
        os.mkdir("./packages")

    while now < end:
        if threading.activeCount() <= threads:
            downloadThread(now+1).start()
            now = now+1

        if len(writing):
            f = open("./result.txt", "a")
            f.write("http://cloud.linspirer.com:880/download?appid=" +
                    writing[0][0]+"&swdid="+mac+" \t"+writing[0][1]+"\n")
            writing.pop(0)
            f.close()

    while threading.activeCount() != 0:
        pass
