#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""

"""

import timeit

from lfsdb.db.client import FileTable
from lfsdb.db.cache import CacheTable

def file_func():
    table = FileTable('/tmp/lfsdb/', 'test', 'test')
    for i in range(10000):
        table.insert({ "name": "wxnacy" })

def cache_func():
    table = CacheTable('test', 'test')
    for i in range(10000):
        table.insert({ "name": "wxnacy" })

if __name__ == "__main__":
    import time
    begin = time.time()
    #  file_func()
    cache_func()
    print(time.time() - begin)
    
