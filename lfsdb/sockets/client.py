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

class Client(object):

    def __init__(self, *args, **kwargs):
        self.socket = socket.socket()

    def connect(self):
        self.socket.connect(
            (SocketConstants.HOST, SocketConstants.PORT)
        )

    def exec(self, db, table, method, params):
        """执行"""
        basic_params = locals()
        basic_params.pop('self', None)
        sq = SocketRequest(**basic_params)
        self.socket.send(sq.dumps())

        res = self.receive_message()
        print(res.data)

    def close(self):
        self.socket.close()

    def receive_message(self):
        """接收消息"""
        data = b''
        while True:
            fragment = self.socket.recv(SocketConstants.FRAGMENT_SIZE)
            if not fragment:
                break
            data += fragment
        return SocketResponse.loads(data)

if __name__ == "__main__":
    client = Client()
    client.connect()
    params = {
        "query": { "_id": 20 }
    }
    client.exec('jable', 'video', 'find', params)

    client.close()
     
