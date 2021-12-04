#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
缓存存储
"""

from lfsdb.db.base import BaseTable
from lfsdb.common.cache import CACHE


class CacheTable(BaseTable):

    cache = CACHE

    def __init__(self, db, table):
        super().__init__(db, table)
        self.key = '{}-{}'.format(db, table)

    def drop(self):
        """删除表"""
        self.cache.hdrop(self.key)

    def _delete_by_id(self, _id):
        """根据 _id 删除
        如果成功需要返回 True
        """
        return self.cache.hdel(self.key, _id) == 1

    def _update(self, doc):
        """修改数据
        如果成功需要返回 True
        """
        _id = doc.get("_id")
        self.cache.hset(self.key, _id, doc)
        return True

    def _list_ids(self):
        """列出当前表内的 id 列表"""
        return self.cache.hkeys(self.key)

    def _read_by_id(self, _id):
        """使用 _id 读取数据"""
        return self.cache.hget(self.key, _id)

    def _exists_id(self, _id):
        """是否存在 _id"""
        return bool(self.cache.hget(self.key, _id))

    def _write(self, doc):
        """写入数据"""
        self.cache.hset(self.key, doc['_id'], doc)
