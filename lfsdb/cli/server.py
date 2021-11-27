#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
服务端
"""

import socket               # 导入 socket 模块
import json
from lfsdb.db.client import FileStorage
TEST_TABLE = FileStorage(None).get_db('jable').get_table('video')


if __name__ == "__main__":

    s = socket.socket()         # 创建 socket 对象
    host = socket.gethostname() # 获取本地主机名
    port = 12345                # 设置端口
    s.bind((host, port))        # 绑定端口

    s.listen(1)                 # 等待客户端连接
    while True:
        c,addr = s.accept()     # 建立客户端连接
        print('连接地址：', c, addr)
        data = c.recv(1024)
        params = json.loads(data.decode())
        print(params, type(params))
        res = TEST_TABLE.find_one_by_id(str(params.get("_id")))
        #  res = 'ss'
        print(res)
        c.send(json.dumps(res).encode())
        c.close()                # 关闭连接
