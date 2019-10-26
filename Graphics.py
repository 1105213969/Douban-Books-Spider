import tkinter
import tkinter.messagebox
import DownloadThread

inputEntry = ""#搜索框

#主程序窗口
class MainWindow:
    def __init__(self):
        self.__window = tkinter.Tk()
        self.__window.title('豆瓣读书爬虫')
        self.__window.geometry('500x500+300+100')

    def run(self):
        global inputEntry
        bg = tkinter.PhotoImage(file="bg.gif")#这里的图片格式必须是.gif
        bgLabel = tkinter.Label(self.__window, image=bg)
        bgLabel.pack()

        label = tkinter.Label(self.__window, text='Please enter a keyword')#创建标签
        label.place(x=150,y=200)

        frmame = tkinter.Frame()#设置一个面板，在面版中放入搜索框和按钮，搜索框和按钮设置在面版的左右两边
        inputEntry = tkinter.Entry(frmame, bg="white")#创建一个文本输入框
        inputEntry.pack(side='left')

        btn = tkinter.Button(frmame, text="search", bg="red", command=btnFun)#创建搜索按钮
        btn.pack(side='right')
        frmame.place(x=150, y=220)#将面版放到窗口中
        self.__window.mainloop()

def btnFun():#按钮触发事件
    global inputEntry
    tag = inputEntry.get()
    DownloadThread.Task(tag).start()#开启线程
    tkinter.messagebox.showinfo('正在下载。。。', '请稍等片刻。。。下载的资源请在D://豆瓣读书.' + tag + '/下查看')

if __name__ == '__main__':#程序入口
    reptile = MainWindow()
    reptile.run()
