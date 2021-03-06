#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
服务端
"""

import socket               # 导入 socket 模块

from lfsdb.common.loggers import get_logger
from lfsdb.sockets.constants import SocketConstants
from lfsdb.sockets.models import SocketRequest
from lfsdb.sockets.models import SocketResponse

class Client(object):
    logger = get_logger('SocketClient')

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
        print(res.data, type(res.data))
        return res

    def stop_server(self):
        """停止服务"""
        data = SocketRequest().build_stop().dumps()
        self.socket.send(data)
        res = self.receive_message()
        print(res.data)
        return res

    def heart(self):
        """发送心跳信息"""
        data = SocketRequest().build_heart().dumps()
        self.socket.send(data)
        return self.receive_message()

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
        self.logger.debug('接收服务端信息 %s', data)
        res = SocketResponse.loads(data)
        self.logger.debug('接收服务端信息 %s', res.to_dict())
        return res

if __name__ == "__main__":
    client = Client()
    client.connect()
    params = {
        "query": { "_id": "20210806152807_1628234887" }
    }
    client.exec('wush', 'version', 'find', params)
    #  client.stop_server()
    #  client.heart()

    client.close()

    client = Client()
    client.connect()
    params = {
        "query": { "_id": "20210806152807_1628234887" }
    }
    #  client.exec('wush', 'version', 'find', params)
    #  client.stop_server()
    client.heart()

    client.close()
