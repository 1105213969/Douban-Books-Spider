import os
import re
import datetime
import requests
from bs4 import BeautifulSoup
import tkinter
import tkinter.messagebox

#书名和评分抽象成一个类
class BookNode:
    def __init__(self, name, rank):
        self.name = name
        self.rank = rank

#爬虫主程序
class Reptile:
    def __init__(self, tag):
        if os.path.exists("./豆瓣读书."+tag) == False:
            os.makedirs("./豆瓣读书."+tag)
        self.__tag = tag  # 搜索的内容
        self.__fp = open('./豆瓣读书.' + self.__tag + "/" + self.__tag + '.txt', 'w', encoding='utf-8') #保存信息的文本
        self.No = 1#书的标号
        self.__BookNodeList = []#保存书的名字和对应评分

    def openUrl(self, url):#打开一个链接，获取返回的html
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
                ,'Cookie':'bid=ruYLMybnZUc; ap_v=0,6.0; _pk_ses.100001.3ac3=*; __utma=30149280.1100659899.1558150724.1558150724.1558150724.1; _'
                          '_utmc=30149280; __utmz=30149280.1558150724.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt_douban=1; _'
                          '_utma=81379588.317660278.1558150724.1558150724.1558150724.1; __utmc=81379588; __'
                          'utmz=81379588.1558150724.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; _'
                          'pk_id.100001.3ac3=680b5c32a6d4e99d.1558150724.1.1558150759.1558150724.; __utmb=30149280.2.10.1558150724; __'
                          'utmb=81379588.2.10.1558150724'
            }#cookie可从本地浏览器获取
            r = requests.get(url, headers=headers)
            print(r)
        except Exception:
            print("错误的URL，无法链接")
        demo = r.text
        return demo

    def getPageNum(self, page):#获取页数
        pageNumsList = re.findall('<a href=\"/tag/' + self.__tag + '\?start=\d+&amp;type=T" >\d+</a>', page)
        if pageNumsList != []:
            pageNum = re.findall('type=T\" >(.*)</a>', pageNumsList[len(pageNumsList) - 1])
            return pageNum[0]
        else:
            return 1

    def download(self, url):
        demo = self.openUrl(url)
        soup = BeautifulSoup(demo, "html.parser")
        soup = soup.find_all('li', 'subject-item')
        for it in soup:
            self.__fp.write("No." + str(self.No) + "\n")

            name = re.findall('title=\"(.*)\"', str(it))  # 获取书名
            if name != []:
                print(name[0])
                self.__fp.write("书名：")
                self.__fp.write(name[0] + "\n")

            author = it.find_all('div', 'pub')#获取作者名、出版信息、出版时间、售价
            if author != []:
                print(author[0].string)
                self.__fp.write("作者/出版信息/出版时间/售价：")
                self.__fp.write(str(author[0].string).strip() + "\n")

            #获取书的简介
            bookLink = re.findall('href="(.*)" ', str(it))#获取到书的具体信息的链接--bookLink[0]
            concretBookInfoHtml = self.openUrl(bookLink[0])#打开链接，获取新的页面代码
            concretBookInfo = BeautifulSoup(concretBookInfoHtml, 'html.parser')#解析页面
            divList = concretBookInfo.find_all('div', 'intro')
            if divList != []:
                info = divList[0].find_all('p')#内容简介位于p标签中
                if info != []:
                    self.__fp.write("内容简介：")
                    for p in info:
                        self.__fp.write( str(p.string) + "\n")#保存标签内容到文本中

            rank = it.find_all('span', 'rating_nums')  # 获取书的豆瓣评分
            if rank != []:
                print(rank[0].string)
                self.__fp.write("豆瓣评分：")
                self.__fp.write(str(rank[0].string) + "\n")

            imgUrl = re.findall('src=\"(.*)\" ', str(it))  # 获取封面url
            if imgUrl != [] and name != []:
                print(imgUrl[0])
                self.__fp.write("书的封面：")
                self.__fp.write(imgUrl[0] + "\n")
                self.downloadBookImg(imgUrl[0], name[0])
            self.__fp.write("**********************************************\n")

            if name != [] and rank != [] and rank[0].string != None:
                self.__BookNodeList.append(BookNode(name[0], float(rank[0].string)))

    pic = None
    def downloadBookImg(self, url, name):  # 下载书的封面图片
        global pic
        try:
            pic = requests.get(url, timeout=20)  # 超时异常判断 20秒超时
        except requests.exceptions.ConnectionError:
            print('当前图片无法下载')
        fp = open("./豆瓣读书." + self.__tag + "/" + "No." + str(self.No)
                  + " " + name.replace('/', '').replace('?', '') + ".jpg", "wb")
        self.No += 1
        # 当书的名字一样时新下载的图片会覆盖掉原来的图片，所以给图片名字前加上标号
        # 有时候书的名字中带有'/'这样会使创建文件失败，所以会将名字中带有'/'的字符换成''
        fp.write(pic.content)
        fp.close()

    def downloadBooksInfo(self):
        startTime = datetime.datetime.now()#程序开始时间
        url = "https://book.douban.com/tag/" + self.__tag #初始url
        demo = self.openUrl(url)

        # 获取页数
        pageNum = self.getPageNum(demo)
        print(pageNum)
        if pageNum == 1:
            self.download(url)
        else:
            s = 0  # 每次翻页，s加20
            i = 1
            while i <= int(pageNum):
                url = "https://book.douban.com/tag/" + self.__tag + "?start=" + str(s) + "&type=T"
                self.download(url)
                i += 1
                s += 20  # 翻页
        endTime = datetime.datetime.now()#程序结束时间
        totalTime = endTime - startTime#程序执行所用时间
        tkinter.messagebox.showinfo('下载完成',self.__tag + '资源已下载完毕，正在分析生成数据报告，请稍等。。。')
        self.dataAnalysis(self.No - 1, totalTime, self.__BookNodeList)

    def dataAnalysis(self, No, time, list):#开一个窗口生成数据报告
        try:
            window = tkinter.Toplevel()  # 只能有一个tk
            window.title('分析报告')
            window.geometry('500x500+300+100')

            text = tkinter.Text(window, width=60, height=30)
            txt = '本次一共搜索到' + str(No) + '本图书\r\n'
            txt += '*****************************************\r\n'
            txt += '所用时间为：' + str(time) + '\r\n'
            txt += '*****************************************\r\n'
            list = sorted(list, key=lambda BookNode: BookNode.rank, reverse=True)  # 降序
            if len(list) < 10:
                txt += '书的数目不足10本\r\n'
            else:
                txt += '豆瓣评分最高Top10:\r\n'
                for i in range(0, 10):
                    txt += str(list[i].name) + '' + str(list[i].rank) + '\r\n'
                txt += '*****************************************\r\n'
                txt += '豆瓣评分最低Top10:\r\n'
                for i in range(len(list) - 11, len(list) - 1):
                    txt += str(list[i].name) + '' + str(list[i].rank) + '\r\n'

            text.insert('insert', txt)
            text.place(x=10, y=10)
            window.mainloop()
        except Exception:
            pass

    def exitReptile(self):#退出爬虫程序
        self.__fp.close()#关闭文件
