from threading import Timer


def hello():
     print ("hello, world")


class RepeatingTimer(Timer): 
    def run(self):
        while not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
            self.finished.wait(self.interval)

t = RepeatingTimer(1, hello)
t.start()
import time
time.sleep(5)
t.cancel()
"""
作者：前面等你
链接：https://juejin.im/post/6844903796254965768
来源：掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""
