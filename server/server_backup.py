import threading
import socket
import pickle
import time

from system import *
from communicator import *
from const import *

class Waiter(threading.Thread):
    def __init__(self, client_holder):
        threading.Thread.__init__(self)
        self.client_holder = client_holder
        self.waiting = False
        self.start()

    def run(self):
        print("Thread Started")
        while self.waiting:
            time.sleep(0.2)
            self.waiting = False
            if len(self.client_holder.messages) > 0:
                print("Waiter Flush")
                self.client_holder.flush()
                self.waiting = True
        print("Thread Stoped")
        self.client_holder.waiter = None

class Client_holder(threading.Thread):
    def __init__(self, server, socket, address):
        threading.Thread.__init__(self)
        self.server = server
        self.socket = socket
        self.address = address
        self.exist = True
        self.client_name = "UNKNOW"
        self.waiter = None
        self.messages = []

    def run(self):
        while (self.exist):
            data = self.socket.recv(65536 * 8)
            if not data:
                self.exist = False
            else:
                self.receive(data)

    def stop(self):
        self.thread_stop = True

    def receive(self, data):
        obj = pickle.loads(data)
        print("RECEIVED:" + str(obj))
        self.server.receive(obj, self)

    def send(self, message):
        self.messages.append(message)
        if not self.waiter:
            print("Sender Flush")
            self.flush()
            self.waiter = Waiter(self)

    def flush(self):
        self.socket.send(pickle.dumps(self.messages))
        for message in self.messages:
            print("发送了类型为 %d 的信息" % (message.typ))
        self.messages = []

    def setname(self, name):
        self.client_name = name

    def getname(self):
        return self.client_name

class Server(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.client_holders = []

        # 初始化暂停系统
        
        self.paused = False
        self.pause_cond = threading.Condition(threading.Lock())
        self.waiter = -1

    def run(self):
        self.server.listen(2)
        baseinfos = []

        # 获取第一个玩家
        print("正在等待玩家 0 连接")
        socket, address = self.server.accept()
        print("玩家 0 已连接: ",socket.getpeername())
        client_holder = Client_holder(self, socket, address)
        self.client_holders.append(client_holder)
        client_holder.start()

        # 接收第一个玩家的信息
        print("正在等待玩家 0 发送身份")
        self.askfunc(0, MESSAGE_BASE)
        print("玩家 0 已发送身份")
        baseinfos.append(self.lastmessage.content)

        # 获取第二个玩家
        print("正在等待玩家 1 连接")
        socket, address = self.server.accept()
        print("玩家 1 已连接: ",socket.getpeername())
        client_holder = Client_holder(self, socket, address)
        self.client_holders.append(client_holder)
        client_holder.start()

        
        # 接收第二个玩家的信息
        print("正在等待玩家 1 发送身份")
        self.askfunc(1, MESSAGE_BASE)
        print("玩家 1 已发送身份")
        baseinfos.append(self.lastmessage.content)

        # 开始游戏
        self.system = System(self, baseinfos)
        self.system.start()

    # 游戏内交流
    def recfunc(self, message, source):
        if (self.paused) and ((self.waiter < 0) or (self.client_holders[self.waiter] == source)) and (message.typ == self.waittype):
            print("成功接收来自玩家 %d 的信息" % self.waiter)
            self.lastmessage = message
            self.resume()
        else:
            print("收到了来自玩家 %d 的垃圾信息" % self.waiter)

    def askfunc(self, clientindex, waittype):
        self.waiter = clientindex
        self.waittype = waittype
        self.pause()

    def sendfunc(self, message, clientindex):
        #print("向玩家 %d 发送了类型为 %d 的信息" % (clientindex, message.typ))
        self.send(message, self.client_holders[clientindex])

    # 服务器功能
    def receive(self, data, source):
        self.recfunc(data, source)
            
    def send(self, data, target):
        target.send(data)

    def sendall(self, data):
        for client_holder in self.client_holders:
            self.send(data, client_holder)

    # 暂停系统
    
    def pause(self):
        self.paused = True
        
        self.pause_cond.acquire()
        with self.pause_cond:
            while self.paused:
                self.pause_cond.wait()

    def resume(self):
        self.paused = False
        self.pause_cond.notify()
        self.pause_cond.release()

if __name__ == "__main__" :
    
    server = Server("", 51234)
    server.start()
    















        
