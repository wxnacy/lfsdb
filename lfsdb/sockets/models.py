#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
模型
"""

import msgpack
import json

from wpy.base import BaseObject
from wpy.base import BaseEnum

from lfsdb.db.client import FileStorage
from lfsdb.common.loggers import get_logger

class PickleModel(BaseObject):

    def dumps(self):
        '''序列化'''
        return msgpack.dumps(self.to_dict())

    @classmethod
    def loads(cls, bytes_data):
        """加载"""
        data = msgpack.loads(bytes_data)
        return cls(**data)

class SRAction(BaseEnum):
    EXEC = 'exec'   # 执行语句
    STOP = 'stop'   # 停止服务
    HEART = 'heart' # 心跳监听


class SocketRequest(PickleModel):
    logger = get_logger('SocketRequest')
    _db_dict = {}

    action = SRAction.EXEC.value
    db = None
    table = None
    method = None
    params = None

    def is_stop(self):
        """是否为停止"""
        return self.action == SRAction.STOP.value

    def is_heart(self):
        """是否为心跳信息"""
        return self.action == SRAction.HEART.value

    def is_unkown(self):
        """是否不明确的信息"""
        return self.action not in SRAction.values()

    @classmethod
    def build_stop(cls):
        return cls(action = SRAction.STOP.value)

    @classmethod
    def build_heart(cls):
        return cls(action = SRAction.HEART.value)

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
        print(data)
        return SocketResponse(data = data)

class SocketResponse(PickleModel):
    code = 0
    data = None
    e = None
    error_name = None

    def json(self):
        """将数据格式化为 dict 结构"""
        if isinstance(self.data, dict) or \
                isinstance(self.data, list):
            return self.data
        else:
            try:
                return json.loads(self.data)
            except:
                return None
        return None

    @classmethod
    def build_unkown(cls):
        """构建 unkown 回复"""
        return cls(code = 1, data='unkown message')

    @classmethod
    def build_error(cls, e):
        return cls(code = 1, error_name = e.NAME, data = str(e))

