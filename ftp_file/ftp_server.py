"""
文件服务器 服务端程序
"""
from socket import *
from threading import Thread
import os, time, sys

# 全局变量
HOST = ("0.0.0.0")
PORT = 11111
ADDR = (HOST, PORT)

# 共享文件库
FTP = "/home/tarena/share/"


# 服务端实现
class FtpServer(Thread):
    def __init__(self, connfd):
        self.connfd = connfd
        super().__init__()


    def find_all_files(self):
        files = os.listdir(FTP)
        if files:
            self.connfd.send(b"OK")
            # time.sleep(0.1)
            files = "\n".join(files)
            self.connfd.send(files.encode())
        else:
            self.connfd.send(b"FAIL")

    def download(self):
        file = self.connfd.recv(1024).decode()
        filename = FTP + file
        if os.path.exists(filename):
            self.connfd.send(b"OK")
            time.sleep(0.1)
            f = open(filename, "rb")
            while True:
                data = f.read(1024)
                if not data:
                    f.close()
                    break
                self.connfd.send(data)
            time.sleep(0.1)
            self.connfd.send(b"##")
        else:
            self.connfd.send(b"FAIL")

    def upload(self):
        filname = self.connfd.recv(128).decode()
        if os.path.exists(FTP + filname):
            self.connfd.send(b"FAIL")
        else:
            self.connfd.send(b"OK")
            f = open(FTP+filname, "wb")
            while True:
                data = self.connfd.recv(1024)
                if data == b"##":
                    f.close()
                    return
                f.write(data)

    def run(self):
        while True:
            data = self.connfd.recv(1024).decode()
            if data == "LIST":
                self.find_all_files()
            elif data == "GET":
                self.download()
            elif data == "PUT":
                self.upload()
            else:
                sys.exit()


def main():
    sock = socket()
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(ADDR)
    sock.listen(5)
    print("listen port", ADDR)
    while True:
        connfd, addr = sock.accept()
        print("connect from", addr)
        t = FtpServer(connfd)
        t.setDaemon(True)
        t.start()




if __name__ == '__main__':
    main()