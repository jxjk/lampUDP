import threading
import time


def cancelTimer():
    global t
    print('end')
    t.cancel()


def func1(a):
    global t
    #Do something
    print('Do something')
    a+=1
    print(a)
    print('当前线程数为{}'.format(threading.activeCount()))
    t=threading.Timer(3,func1,(a,))
    t.start()

t = threading.Timer(2,func1,(0,))
while 1:
    a=int(input('a=:'))
    if a == 0:
        print('0')
        t.cancel()
    elif a == 1:
        t.start()
        print('??')
    else :
        break
# time.sleep(10)
# cancelTimer()
