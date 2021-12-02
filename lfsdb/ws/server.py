#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
服务端
"""

import socket               # 导入 socket 模块
import json

from lfsdb.ws.constants import WSConstants
from lfsdb.ws.models import SocketModel
from lfsdb.db.client import FileStorage
TEST_TABLE = FileStorage(None).get_db('jable').get_table('video')

class Server(object):
    _db_dict = {}
    def __init__(self, *args, **kwargs):
        self.socket = socket.socket()

    def run(self):
        """运行服务
        """
        print("开始运行服务")
        self.socket.bind(
            (WSConstants.HOST, WSConstants.PORT)
        )
        self.socket.listen(1)

        while True:
            c,addr = self.socket.accept()     # 建立客户端连接
            print('连接地址：', c, addr)
            model = self.receive_message(c)
            c.send('test'.encode())
            c.close()                # 关闭连接

    def receive_message(self, receive_socket: socket.socket):
        """接收消息"""
        data = b''
        while True:
            fragment = receive_socket.recv(1024)
            if not fragment:
                break
            data += fragment
        return SocketModel.loads(data)


    def db(self, db, table):
        """获取数据库"""
        key = '{}-{}'.format(db, table)
        if key not in self._db_dict:
            self._db_dict[key] = FileStorage(None).get_db(db).get_table(table)
        return self._db_dict

