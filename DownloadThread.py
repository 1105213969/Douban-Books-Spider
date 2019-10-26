import threading
import DoubanBookReptile

#用来下载资源的线程
class Task(threading.Thread):
    def __init__(self, tag):
        threading.Thread.__init__(self)
        self.__tag = tag
    def run(self):
        reptile = DoubanBookReptile.Reptile(self.__tag)
        reptile.downloadBooksInfo()
        reptile.exitReptile()
