#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
socket lfs 客户端
"""

from lfsdb.sockets.client import Client
from lfsdb.db.errors import LfsdbError

class SocketStorage(object):
    pass

class SocketDB(object):
    pass

class SocketTable(object):
    def __init__(self, db, table):
        self.db = db
        self.table = table

    def _exec(self, method, **kwargs):
        self.client = Client()
        self.client.connect()
        params = {}
        params.update(kwargs)
        res = self.client.exec(self.db, self.table, method, params)
        self.close()

        if res.error_name:
            raise LfsdbError.get_error(res.error_name)(res.data)

        return res.json() or res.data

    def close(self):
        try:
            self.client.close()
        except:
            pass

    def find(self, query=None, projection=None, **kwargs):
        """
        查询列表
        """
        return self._exec('find', **self._build_params(locals()))

    def find_one(self, query=None, projection=None, **kwargs):
        """
        查询单个 doc
        """
        return self._exec('find_one', **self._build_params(locals()))

    def find_by_id(self, _id):
        """
        根据 _id 查询
        """
        return self._exec('find_by_id', **self._build_params(locals()))

    def count(self, doc):
        """
        查询数量
        """
        return self._exec('count', **self._build_params(locals()))

    def insert(self, doc):
        """
        插入数据
        """
        return self._exec('insert', **self._build_params(locals()))

    def update(self, query, update_data):
        """
        修改数据
        """
        return self._exec('update', **self._build_params(locals()))

    def delete(self, query):
        """
        删除数据
        """
        return self._exec('delete', **self._build_params(locals()))

    def drop(self):
        """
        删除表
        """
        return self._exec('drop', **self._build_params(locals()))

    @classmethod
    def _build_params(cls, locals_params):
        """构造参数"""
        params = locals_params
        params.pop('self', None)
        kw = params.pop('kwargs', {})
        params.update(kw)
        return params

if __name__ == "__main__":
    table = SocketTable('lfsdb_test','socket')
    doc = { "_id": "1234", "name": "wxnacy" }
    _id = table.insert(doc)
    print(_id)
    _id = table.insert(doc)
    print(_id)
    #  table.update({ "_id": _id }, { "name": "wxnacy" })
    #  import json
    #  print(json.dumps(table.find_by_id(_id), indent=4))
    #  table.drop()
    #  table.close()
         
