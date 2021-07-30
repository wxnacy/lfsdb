#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""


from lfsdb.db.client import FileStorage


if __name__ == "__main__":
    db = FileStorage()
    db.get_db('download').dump('~/Downloads')
    db.get_db('download').dump()
    db.get_db('download').store('/Users/wxnacy/.lfsdb/dump/lfsdb_download_20210730163548_dump')
    db.get_db('download').store()
    db.get_db('download').store('lfsdb_download_20210730164153_dump')
