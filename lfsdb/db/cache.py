#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
数据缓存
"""

import os
import json
import sys

from collections import defaultdict

class FileCache(object):
    _table_data = defaultdict(dict)

    def init(self, db, table):
        self.db = db
        self.table = table

    def _generage_key(self):
        """生成 key"""
        return '{}_{}'.format(self.db, self.table)

    def set(self, data):
        """插入数据"""
        key = self._generage_key()
        if isinstance(data, dict) and '_id' in data:
            self._table_data[key][data['_id']] = data
        #  print(json.dumps(self._table_data, indent=4))

    def get(self, _id):
        """通过 id 查找"""
        key = self._generage_key()
        return self._table_data[key].get(_id)

    def remove(self, _id):
        """通过 id 查找"""
        key = self._generage_key()
        return self._table_data[key].pop(_id, None)

    def list_ids(self,):
        """列出 id 列表"""
        key = self._generage_key()
        data = self._table_data.get(key)

        return list(data.keys()) if data else []

    def drop(self):
        """删除表"""
        self._table_data[self._generage_key()] = {}

    def memory(self):
        """内存"""
        return sys.getsizeof(self._table_data)

FILE_CACHE = FileCache()

del FileCache
