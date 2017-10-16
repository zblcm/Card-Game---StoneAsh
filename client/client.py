import threading
import socket
import pickle

class Server_holder(threading.Thread):
    def __init__(self, client, socket):
        threading.Thread.__init__(self)
        self.socket = socket
        self.client = client
        self.exist = True

    def run(self):
        while (self.exist):
            data = self.socket.recv(65536 * 8)
            if not data:
                self.exist = False
            else:
                self.receive(data)

    def receive(self, data):
        obj = pickle.loads(data)
        self.client.receive(obj, self)

    def send(self, data):
        self.socket.send(pickle.dumps(data))
        
class Client(threading.Thread):
    def __init__(self, system, host, port):
        threading.Thread.__init__(self)
        self.system = system
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def run(self):
        print("搜索服务器中 ...")
        self.socket.connect((self.host, self.port))
        print("已连接到服务器")
        self.server_holder = Server_holder(self, self.socket)
        self.server_holder.start()
        print("发送基本信息")
        self.send(self.system.makebaseinfomessage())
        

    def receive(self, messages, source):
        print("收到信息包:")
        for message in messages:
            print("收到了类型为%d的信息" % message.typ)
            self.system.dealmessage(message)

    def send(self, data):
        self.server_holder.send(data)

from communicator import *

from const import *

if __name__ == "__main__" :
        
    host = "localhost"
    
    port = 51234
    
    client = Client(host, port)
    












        
            
