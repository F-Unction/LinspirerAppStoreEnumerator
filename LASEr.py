import os
import datetime
import requests
import _thread

writing = []
nowDownloading = 0


def log(threadNum, id, message):
    print("["+datetime.datetime.now().strftime("%H:%M:%S")+"]" +
          "["+str(threadNum)+"]"+"["+str(id)+"]:", message)


def output(id, package):
    global writing
    writing.append([id, package])


def download(id, threadNum):
    global nowDownloading

    log(threadNum, id, "downloading")
    url = "http://cloud.linspirer.com:880/download?appid="+str(id)+"&swdid=1"
    res = requests.get(url)

    if len(res.content) < 100:
        log(threadNum, id, "is not an apk")
        output(str(id), "NULL")
        nowDownloading = nowDownloading-1
        return
    else:
        log(threadNum, id, "is an apk, writing")

    with open("./packages/"+str(id)+".apk", "wb") as f:
        f.write(res.content)

    log(threadNum, id, "wrote, analyzing")

    text = os.popen("java -jar GetAPKInfo.jar ./packages/" +
                    str(id)+".apk").read()
    packageName = text[text.find(
        "包名: ")+4:text.find("\n", text.find("包名: ")+4)]

    log(threadNum, id, "analyzed, package name "+packageName)
    f.close()
    output(str(id), packageName)

    os.system("rm ./packages/"+str(id)+".apk")

    nowDownloading = nowDownloading-1


if __name__ == "__main__":
    beg = int(input("begin with\t>"))
    end = int(input("end with\t>"))
    threads = int(input("thread number\t>"))
    now = beg-1

    if not os.path.exists("./packages"):
        os.mkdir("./packages")

    while now < end:
        if nowDownloading < threads:
            _thread.start_new_thread(download, (now+1, nowDownloading+1))

            nowDownloading = nowDownloading+1
            now = now+1

        if len(writing):
            f = open("./result.txt", "a")
            f.write("http://cloud.linspirer.com:880/download?appid=" +
                    writing[0][0]+"&swdid=1 \t"+writing[0][1]+"\n")
            writing.pop(0)
            f.close()

    while nowDownloading!=0:
        pass
