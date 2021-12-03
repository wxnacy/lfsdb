#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
服务端
"""

import time
from multiprocessing import Process

from lfsdb.sockets.client import Client
from lfsdb.sockets.server import Server
from lfsdb.common.loggers import get_logger

logger = get_logger(__name__)

def heart():
    while True:
        time.sleep(2)
        logger.info(time.time())
        #  c = Client()
        #  c.connect()
        #  c.heart()
        #  c.close()

def stop():
    c = Client()
    c.connect()
    c.stop_server()
    c.close()

def main():
    import sys
    args = sys.argv[1:]
    typ = 'start'
    if args:
        typ = args[0]
    if typ == 'stop':
        stop()
    else:
        p = Process(target=heart)
        p.daemon = True
        p.start()

        Server().run()


if __name__ == "__main__":
    main()
