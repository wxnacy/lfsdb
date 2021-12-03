#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
常量
"""

import socket

# 获取本机主机名
localhost = socket.gethostname()

class SocketConstants(object):
    PORT = 60608
    HOST = localhost

    FRAGMENT_SIZE = 16 * 1024 * 1024
