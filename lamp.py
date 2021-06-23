# -*- coding: utf-8 -*-
import os
import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
from tkinter import Tk
from tkinter import ttk
from tkinter import font
from tkinter import LabelFrame
from tkinter import Label
from tkinter import Menu
from tkinter import StringVar
from tkinter import DoubleVar
from tkinter import IntVar 
from tkinter import Entry
from tkinter import END
from tkinter import Button
from tkinter import Checkbutton
from tkinter.ttk import Combobox 
from tkinter import Frame
from tkinter import RIGHT
from tkinter import NSEW
from tkinter import NS
from tkinter import NW
from tkinter import N 
from tkinter import Y 
from tkinter import DISABLED
from tkinter import NORMAL
from tkinter import Toplevel 
import csv
from socket import *
import sys
from threading import Thread
import time
import pickle
import re
from configparser import ConfigParser


# 读取配置文件
cfg = ConfigParser()
cfg.read('config.ini')
macroFile = (cfg.get('MacroFile','macrofile'))
macroCopy = (cfg.get('MacroFile','macroCopy'))
color = (cfg.get('LED','color'))
timeSleep = (cfg.getint('LED','timeSleep'))
ledCount = (cfg.getint('LED','ledCount'))


ips = cfg.items('IP')

# 全局变量定义
timeSave = os.path.getmtime(macroFile)
runningFlg = True


def thread_it (func,*args):
    '''
    将函数打包进程
    '''
    # 创建进程
    t = Thread(target=func,args=args)
    # 守护
    # t.setDaemon(True)
    # 启动
    t.start()
    

def handlerAdaptor(fun,**kwds):
    '''事件处理函数的适配器，相当于中介。'''
    return lambda event, fun=fun,kwds=kwds: fun(event,**kwds)


class GuiPart():  
    def __init__(self,):  
        self.checkLedFlg = False
        thread_it(self.readMacro,)


    def findLED(self,huoJiaId):
        csvFile = open('master.csv','r')
        reader = csv.reader(csvFile)
        try:
            result = {}
            for item in reader:
                if reader.line_num == 1:
                    continue
                result[item[0]] = [item[0],item[1],item[2],item[3]]
            csvFile.close()
            huiJiaId = (result[huoJiaId][0])
            start = result[huoJiaId][1]
            number = result[huoJiaId][2]
            ip = result[huoJiaId][3]

            return (huoJiaId,start,number,ip)
        except:
            return -1


    def send(self,start=0,number=0,ip='10.3.22.188',cmd=None):
        try:
            serverName = ip #'169.254.35.198'#'10.3.22.23'
            serverPort = 50007
            clientSocket = socket(AF_INET,SOCK_STREAM)
            clientSocket.connect((serverName,serverPort))
            # sentence = input('Input lowercase sentence:')
            if cmd == None:
                sentence =  start + ',' + number + ',' + color
            else:
                sentence = cmd
            print('sentence: ',sentence)
            clientSocket.send(sentence.encode())
            modifiedSentence = clientSocket.recv(1024)
            print('From Server: ',modifiedSentence.decode())
            """# 取消延时关闭LED
            time.sleep(timeSleep)
            sentence = b'C'
            clientSocket.send(sentence)
            modifiedSentence = clientSocket.recv(1024)
            print('From Server: ',modifiedSentence.decode())
            """
            clientSocket.close()
        except:
            print('send lost: ',ip)

    
    def checkLedStop(self):
        self.checkLedFlg = False
        t = Thread(target=self.clearLed)
        t.start()


    def clearLed(self):
        for _,ip in ips:
            self.send(ip=ip,cmd='C')
            time.sleep(0.3)
        # self.varHuoJiaId.set('LED清除完成')

    
    def checkLedStart(self):
        self.checkLedFlg = True
        t = Thread(target=self.checkLed)
        t.start()


    def checkLed(self):
        print('checkLed')
        self.varHuoJiaId.set('LED检查开始')
        threads = []
        for _,ip in ips:
            for start in range(0,ledCount,56):
                print(start,ip)
                if not self.checkLedFlg:
                    self.send(ip=ip,cmd='C')
                    self.varHuoJiaId.set('LED检查终止')
                    return 0 
                self.send(str(start),'57',ip)
                time.sleep(0.5)
        self.varHuoJiaId.set('LED检查完成')

    def readMacro(self):
        global timeSave
        while runningFlg :
            # 读取tool_n、gear_n 数据源：macro.txt
            timeLast = os.path.getmtime(macroFile)
            if timeLast > timeSave:
                timeSave = timeLast
                os.system(r'copy %s %s'%(macroFile,macroCopy)) 
                f = open (macroCopy,'r')
                fileLines = f.readlines()
                f.close()
                print(fileLines)

                if len(fileLines) != 0:
                    print('len(fileLines != 0)')
                    self.closeLed()
                    time.sleep(0.1)
                    info = ''
                    # 读取数据
                    for item in fileLines:
                        item = item.replace('\n','')
                        try:
                            _,start,number,ip =self.findLED(item)
                            print(_,start,number,ip)
                            info = info + '\n' + item 
                            # self.varHuoJiaId.set(_)
                            # self.varIp.set(ip)
                            # self.varStart.set(start)
                            # self.varNumber.set(number)
                            t= Thread(target=self.send,args=(start,number,ip,))
                            t.start()
                        except:
                            if item == "":
                                info = info
                            else:
                                info = info + '\n'+ item + ' 货架错误'
                            """
                            print('-C')
                            # self.varHuoJiaId.set('')
                            # self.varIp.set('')
                            # self.varStart.set('')
                            # self.varNumber.set('')
                            threads = []
                            print(ips)
                            for _,ip in ips:
                                t= Thread(target=self.send,args=(0,0,ip,'C',))
                                print(ip)
                                threads.append(t)
                            for t in threads:
                                t.start()
                            """
                    self.varHuoJiaId.set(info)
                else:
                    print('len(fileLines = 0)')
                    self.varHuoJiaId.set("")
                    self.closeLed()
            else:
                pass
            time.sleep(1)

    def closeLed(self):
        print('len(fileLines = 0)')
        threads = []
        for _,ip in ips:
            t= Thread(target=self.send,args=(0,0,ip,'C',))
            print(ip)
            threads.append(t)
        for t in threads:
            t.start()

    # 调整屏幕
    def center_window(self, root, w , h):
        """
        窗口居于屏幕中央
        :param root: root
        :param w: 窗口宽度
        :param h: 窗口高度
        :return:
        """
        # 获取屏幕 宽、 高
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        # 计算 x， y 位置
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        root.geometry('%dx%d+%d+%d' % (w, h, x , y))


    # 定义Gui界面
    def guiProcess(self):
        '''
        GUI主界面
        :param
        :return
        '''
        root = Tk()
        self.root = root
        # 设置窗口位置
        root.title("lamp库位指示系统")
        self.center_window(root,400,248)
        root.resizable(0,0)# 窗体大小可调整，分别表示x,y方向的可变性
        # 设置菜单栏
        menubar = Menu(self.root)
        self.menubar = menubar
        helpmenu = Menu(menubar,tearoff=0)
        self.helpmenu = helpmenu
        self.menubar.add_cascade(label='帮助',menu=self.helpmenu)
        self.helpmenu.add_command(label="帮助",command = lambda : os.popen('.\help.pdf'))
        self.root.config(menu=self.menubar)

        # 定义子窗口
        # self.window1 = IntVar(self.root,value=0)
        
        # 容器控件
        labelframe_l = LabelFrame(root,width=390,height=238,text= "")
        labelframe_l . place(x=5,y=5)
        self.labelframe_l = labelframe_l


        ############
        # 信息面板 #
        ############

        ### 定义 工件 信息 ###
        ft = font.Font(size=15)
        # 定义 货架ID
        self.varHuoJiaId = StringVar()
        huoJiaId = Label(labelframe_l,width=26,textvariable=self.varHuoJiaId,font=ft)
        huoJiaId . place(x=5,y=5)
        self.huoJiaId = huoJiaId 
        
        """
        # 定义 ip
        self.varIp= StringVar()
        ipAddres = Label(labelframe_l,width=16,textvariable=self.varIp,font=ft)
        ipAddres . place(x=180,y=5)
        self.ipAddres = ipAddres 
        
        # 定义 start
        self.varStart = DoubleVar()
        start = Label(labelframe_l,width=16,textvariable=self.varStart,font=ft)
        start . place(x=5,y=35)
        self.start = start 
        
        # 定义 number
        self.varNumber= DoubleVar()
        number = Label(labelframe_l,width=16,textvariable=self.varNumber,font=ft)
        number . place(x=180,y=35)
        self.number = number 
        """

        B_checkLedStart = Button(labelframe_l,text='开始检查LED',font=ft,width=15)
        B_checkLedStart . place(x=20,y=180)
        self.B_checkLedStart = B_checkLedStart

        B_checkLedStop = Button(labelframe_l,text='清除LED',font=ft,width=15)
        B_checkLedStop . place(x=200,y=180)
        self.B_checkLedStop = B_checkLedStop


        # 定义事件响应
        B_checkLedStart.configure(command=self.checkLedStart) # 开始扫描文件
        B_checkLedStop.configure(command=self.checkLedStop) # 开始扫描文件

        root.mainloop()
        runningFlg = False

if __name__ == '__main__':
    ui=GuiPart()
    ui.guiProcess()
