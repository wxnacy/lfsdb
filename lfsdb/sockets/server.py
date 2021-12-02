#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
服务端
"""

import socket               # 导入 socket 模块

from lfsdb.sockets.constants import SocketConstants
from lfsdb.sockets.models import SocketRequest

class Server(object):

    def __init__(self, *args, **kwargs):
        self.socket = socket.socket()

    def run(self):
        """运行服务
        """
        print("开始运行服务")
        self.socket.bind(
            (SocketConstants.HOST, SocketConstants.PORT)
        )
        self.socket.listen(3)

        while True:
            c,addr = self.socket.accept()     # 建立客户端连接
            print('连接地址：', c, addr)
            req = self.receive_message(c)
            print(req)
            res = req.run()
            c.send(res.dumps())
            c.close()                # 关闭连接

    def receive_message(self, receive_socket: socket.socket):
        """接收消息"""
        data = b''
        while True:
            #  fragment = receive_socket.recv(SocketConstants.FRAGMENT_SIZE)
            fragment = receive_socket.recv(2)
            print(fragment)
            if not fragment:
                break
            print('w')
            data += fragment
            print(data)
        print(data)
        return SocketRequest.loads(data)

