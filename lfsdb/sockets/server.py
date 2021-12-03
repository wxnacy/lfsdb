#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
服务端
"""

import socket               # 导入 socket 模块
import traceback

from lfsdb.sockets.constants import SocketConstants
from lfsdb.sockets.models import SocketRequest
from lfsdb.sockets.models import SocketResponse
from lfsdb.sockets.exceptions import ServerStopException

from threading import Event

done_event = Event()

def handle_sigint(signum, frame):
    done_event.set()

import signal
signal.signal(signal.SIGINT, handle_sigint)


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
            if done_event.is_set():
                print('服务停止')
                break
            try:
                self.accept()
            except ServerStopException:
                break
            except:
                print(traceback.format_exc())
                print(traceback.format_stack())

    def accept(self):
        """接收客户端信息"""
        c,addr = self.socket.accept()     # 建立客户端连接
        print('连接地址：', c, addr)
        #  try:
        self._accept(c)
        #  except ServerStopException:
            #  break
        #  except:
            #  print(traceback.format_exc())
            #  print(traceback.format_stack())
        c.close()                # 关闭连接

    def _accept(self, socket):
        """接收客户端信息"""
        req = self.receive_message(socket)
        if req.is_unkown():
            socket.send(SocketResponse.build_unkown().dumps())
            return

        # 回复心跳信息
        if req.is_heart():
            socket.send(SocketResponse().dumps())
            return

        print(req.is_stop())
        if req.is_stop():
            print('服务停止')
            socket.send(SocketResponse(data = '服务停止').dumps())
            raise ServerStopException()
        print(req)
        res = req.run()
        socket.send(res.dumps())

    def receive_message(self, receive_socket: socket.socket):
        """接收消息"""
        data = receive_socket.recv(SocketConstants.FRAGMENT_SIZE)
        return SocketRequest.loads(data)

