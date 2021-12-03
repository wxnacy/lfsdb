#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
模型
"""

import pickle
import json

from wpy.base import BaseObject
from wpy.base import BaseEnum

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

class SRAction(BaseEnum):
    EXEC = 'exec'   # 执行语句
    STOP = 'stop'   # 停止服务


class SocketRequest(PickleModel):
    _db_dict = {}
    action = SRAction.EXEC.value
    db = None
    table = None
    method = None
    params = None

    def is_stop(self):
        """是否为停止"""
        return self.action == SRAction.STOP.value

    @classmethod
    def build_stop(cls):
        return cls(action = SRAction.STOP.value)

    def get_db(self):
        """获取数据库"""
        key = '{}-{}'.format(self.db, self.table)
        if key not in self._db_dict:
            self._db_dict[key] = FileStorage(None).get_db(self.db
                ).get_table(self.table)
        return self._db_dict[key]

    def run(self):
        """运行结果"""
        data = getattr(self.get_db(), self.method)(**self.params)
        return SocketResponse(data = data)

class SocketResponse(PickleModel):
    data = None

    def json(self):
        """将数据格式化为 dict 结构"""
        if isinstance(self.data, dict):
            return self.data
        else:
            try:
                return json.loads(self.data)
            except:
                return None
        return None




