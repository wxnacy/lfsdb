#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""

"""

import os
import socket               # 导入 socket 模块
import json

from lfsdb.ws.constants import WSConstants

if __name__ == "__main__":

    s = socket.socket()         # 创建 socket 对象
    host = socket.gethostname() # 获取本地主机名
    port = WSConstants.PORT                # 设置端口号

    s.connect((host, port))

    params = { "_id": 20 }
    s.send(json.dumps(params).encode())
    #  print(s.recv(1024))
    while True:
        data = s.recv(1024)
        if not data:
            break
        print(data.decode())
    s.close()
