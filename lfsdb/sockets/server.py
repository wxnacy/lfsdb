#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
服务端
"""

import socket               # 导入 socket 模块

from lfsdb.sockets.constants import SocketConstants
from lfsdb.sockets.models import SocketRequest
from lfsdb.sockets.models import SocketResponse

class Server(object):

    def __init__(self, *args, **kwargs):
        self.socket = socket.socket()

    def run(self):
        """运行服务
        """
        print("开始运行服务")
        # 处理 TCP 断开后端口占用问题
        # https://blog.csdn.net/Jason_WangYing/article/details/105420659
        self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
        self.socket.bind(
            (SocketConstants.HOST, SocketConstants.PORT)
        )
        self.socket.listen(5)

        while True:
            c,addr = self.socket.accept()     # 建立客户端连接
            print('连接地址：', c, addr)
            req = self.receive_message(c)
            print(req.is_stop())
            if req.is_stop():
                print('服务停止')
                c.send(SocketResponse(data = '服务停止').dumps())
                c.close()
                break
            print(req)
            res = req.run()
            c.send(res.dumps())
            c.close()                # 关闭连接

    def receive_message(self, receive_socket: socket.socket):
        """接收消息"""
        data = receive_socket.recv(SocketConstants.FRAGMENT_SIZE)
        return SocketRequest.loads(data)

