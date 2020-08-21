from socket import *
from threading import Thread
import time, os

# 全局变量
HOST = ("172.88.8.72")
PORT = 11111
ADDR = (HOST, PORT)

# 文件库
FTP = "./share/"


class FtpClient:
    def __init__(self):
        self.sock = socket()
        self.sock.connect(ADDR)

    def find_all_files(self):
        self.sock.send(b"LIST")
        data = self.sock.recv(128)
        if data == b"OK":
            files = self.sock.recv(1024 * 10).decode()
            print(files)
        else:
            print("文件库为空")

    def upload(self, opt):
        self.sock.send(b"PUT")
        time.sleep(0.1)
        filename = opt.split(" ")[-1]
        self.sock.send(filename.encode())
        if self.sock.recv(128) == b"OK":
            f = open(FTP + filename, "rb")
            while True:
                data = f.read(1024)
                if not data:
                    f.close()
                    time.sleep(0.1)
                    self.sock.send(b"##")
                    break
                self.sock.send(data)
        else:
            print("文件已存在")

    def download(self, opt):
        self.sock.send(b"GET")
        time.sleep(0.1)
        self.sock.send(opt.split(" ")[-1].encode())
        if self.sock.recv(2).decode() == "OK":
            if not os.path.exists(FTP + opt.split(" ")[-1]):
                f = open(FTP + opt.split(" ")[-1], "wb")
                while True:
                    data = self.sock.recv(1024)
                    if data == b"##":
                        f.close()
                        break
                    f.write(data)
            else:
                print("文件已存在")
        else:
            print("该文件不存在")

    def menu(self):
        print("""
        ======================
            1.  LIST
            2.GET FILE
            3.PUT FILE
            4.  EXIT
        ======================
        """)

    def main(self):
        while True:
            self.menu()
            opt = input(">>")
            if not opt:
                self.sock.send(b"QIUT")
                self.sock.close()
                return
            elif opt.split(" ")[0] == "LIST":
                self.find_all_files()
            elif opt.split(" ")[0] == "GET":
                self.download(opt)
            elif opt.split(" ")[0] == "PUT":
                self.upload(opt)


if __name__ == '__main__':
    client = FtpClient()
    client.main()
