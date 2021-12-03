#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
socket lfs 客户端
"""

from lfsdb.sockets.client import Client

class LfsSocketClient(object):
    pass

class LfsSocketDB(object):
    pass

class LfsSocketTable(object):
    def __init__(self, db, table):
        self.db = db
        self.table = table
        self.client = Client()

    def _exec(self, method, **kwargs):
        self.client.connect()
        params = {}
        params.update(kwargs)
        res = self.client.exec(self.db, self.table, method, params)
        self.client.close()

        return res.json() or res.data


    def find(self, query=None, projection=None, **kwargs):
        """
        查询列表
        """
        return self._exec('find', **self._build_params(locals()))

    def find_by_id(self, _id):
        """
        根据 _id 查询
        """
        return self._exec('find_one_by_id', **self._build_params(locals()))

    def insert(self, doc):
        """
        插入数据
        """
        return self._exec('insert', **self._build_params(locals()))

    @classmethod
    def _build_params(cls, locals_params):
        """构造参数"""
        params = locals_params
        params.pop('self', None)
        kw = params.pop('kwargs', {})
        params.update(kw)
        return params

if __name__ == "__main__":
    table = LfsSocketTable('lfsdb_test', 'socket')
    res = table.insert({ "name": "wxnacy" })
    query = { "_id": "20210806152807_1628234887" }
    #  res = table.find(query)
    #  res = table.find_by_id(query.get("_id"))
    print(res)

