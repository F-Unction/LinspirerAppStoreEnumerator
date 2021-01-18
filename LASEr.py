import os
import queue
import datetime
import requests
import threading

writing = []

class downloadThread (threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id = id

    def run(self):
        try:
            download(self.id)
        except Exception:
            log(id, "ERROR, MESSAGE:"+str(Exception))


def download(id):
    log(id, "downloading")
    url = "http://cloud.linspirer.com:880/download?appid=" + \
        str(id)+"&swdid=1"
    res = requests.get(url)

    if len(res.content) < 100:
        log(id, "is not an apk")
        output(str(id), "NULL")
        return
    else:
        log(id, "is an apk, writing")

    with open("./packages/"+str(id)+".apk", "wb") as f:
        f.write(res.content)

    log(id, "wrote, analyzing")

    text = os.popen("java -jar GetAPKInfo.jar ./packages/" +
                    str(id)+".apk").read()
    packageName = text[text.find(
        "包名: ")+4:text.find("\n", text.find("包名: ")+4)]

    log(id, "analyzed, package name "+packageName)
    f.close()
    output(str(id), packageName)

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
                    writing[0][0]+"&swdid=1 \t"+writing[0][1]+"\n")
            writing.pop(0)
            f.close()

    while threading.activeCount() != 0:
        pass
