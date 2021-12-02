#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
模型
"""

import pickle

from wpy.base import BaseObject

from lfsdb.db.client import FileStorage

class PickleModel(BaseObject):

    def dumps(self):
        '''序列化'''
        return pickle.dumps(self.to_dict())

    @classmethod
    def loads(cls, bytes_data):
        """加载"""
        data = pickle.loads(bytes_data)
        return cls(**data)

class SocketModel(PickleModel):
    _db_dict = {}
    db = None
    table = None
    method = None
    params = None

    def get_db(self):
        """获取数据库"""
        key = '{}-{}'.format(self.db, self.table)
        if key not in self._db_dict:
            self._db_dict[key] = FileStorage(None).get_db(self.db
                ).get_table(self.table)
        return self._db_dict

    def run(self):
        pass
