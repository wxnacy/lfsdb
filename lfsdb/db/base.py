#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
基类
"""

import uuid
from abc import ABCMeta
from abc import abstractmethod
from datetime import datetime

from wpy.base import BaseObject
from wpy.tools import sorted_plus

from lfsdb.common.loggers import get_logger
from .errors import FileStorageError
from .errors import FSQueryError
from .query import FSQuery

class BaseTable(BaseObject, metaclass=ABCMeta):

    def __init__(self, db, table):
        self.db = db
        self.table = table

    def insert(self, doc):
        """
        插入文档
        """
        data = dict(doc)
        _id = doc.get("_id") or self._generage_id()
        if self._exists_id(_id):
            raise FileStorageError('{}._id {} is exists'.format(self.table, _id))
        data['_id'] = _id
        data['_create_time'] = self._now()
        data['_update_time'] = self._now()
        self._write(data)
        return _id

    def find_by_id(self, _id):
        """通过 _id 查找"""
        if self._exists_id(_id):
            doc = self._read_by_id(_id)
            return doc
        return None

    def find(self, query=None, projection=None, **kwargs):
        """
        查询列表

        :param dict query: 查询条件
            {"name": "wxnacy", "_create_time": { "$gt": "2021-08-06" }}
        :param dict projection: 需要返回的字段
            {"_id": 0}
        :param kwargs:
            `sort`: [('age', 1), ('_create_time', -1)]
                使用 `age` 正序排列，`_create_time` 倒序排列
        """
        if not query:
            query = {}
        if not projection:
            projection = {}

        # 先将 _id 从过滤条件中提取出来
        projection_id_type = projection.pop('_id', None)

        # 判断过滤字段中，是否有 1 和 0 的混用，_id 除外
        # 例如 { "field1": 1, "field1": 0 } 不允许出现
        projection_values = set(projection.values())
        if len(projection_values) > 1:
            raise FSQueryError(('Projection cannot have a mix of inclusion'
                ' and exclusion.'))

        # 判断过滤字段的条件是 include 还是 exclude
        projection_type = list(projection_values)[0] if len(
                projection_values) > 0 else None

        # 如果查询条件中出现 _id，则直接查询该 _id
        if '_id' in query:
            item = self.find_by_id(query['_id'])
            return [item] if item else []

        # 列出表内所有 id
        ids = self._list_ids()
        res = []
        # 构建查询条件模型实例
        fsquery = FSQuery(query)
        for _id in ids:
            doc  = self._read_by_id(_id)
            # 判断 doc 是否符合 query 条件
            if fsquery.exists(doc):
                # 过滤指定字段
                doc = self._get_projection_doc(doc, projection, projection_type)
                # 判断是否返回 _id 字段
                if projection_id_type == 1:
                    doc['_id'] = _id
                elif projection_type == 0:
                    doc.pop('_id', None)
                res.append(doc)

        # 默认使用时间排序
        sorter = kwargs.get('sorter', [('_create_time', 1)])
        sorted_plus(res, sorter = sorter)
        return res

    def find_one(self, query=None, projection=None, **kwargs):
        docs = self.find(query, projection, **kwargs)
        return docs[0] if docs else None

    def count(self, query=None):
        """
        查询数量
        """
        projection = { "_id": 1 }
        return len(self.find(query, projection=projection))

    def update(self, query, update_data):
        if '_id' in update_data:
            raise FileStorageError('_id can not update')
        docs = self.find(query)
        count = 0
        for doc in docs:
            doc.update(update_data)
            doc['_update_time'] = self._now()
            if self._update(doc):
                count += 1
        return count

    def delete(self, query):
        """删除数据"""
        docs = self.find(query)
        count = 0
        for doc in docs:
            _id = doc.get("_id")
            if self._exists_id(_id) and self._delete_by_id(_id):
                count += 1
        return count

    @abstractmethod
    def drop(self):
        """删除表"""

    def _get_projection_doc(self, doc, projection, projection_type):
        """获取指定字段的数据"""
        if not projection:
            return doc

        if projection_type == 0:
            for k, v in projection.items():
                doc.pop(k)
            return doc
        res = {"_id": doc.get("_id")}
        for k, v in projection.items():
            if v == 1 and k in doc:
                res[k] = doc[k]
        return res

    def _now(self):
        """获取当前时间"""
        return str(datetime.now())

    def _generage_id(self):
        """生成 id"""
        return str(uuid.uuid4())

    @abstractmethod
    def _write(doc):
        """写入数据"""

    @abstractmethod
    def _read_by_id(self, _id):
        """使用 _id 读取数据"""

    @abstractmethod
    def _exists_id(self, _id):
        """是否存在 _id"""

    @abstractmethod
    def _update(self, doc):
        """修改数据
        如果成功需要返回 True
        """

    @abstractmethod
    def _delete_by_id(self, _id):
        """根据 _id 删除
        如果成功需要返回 True
        """

    @abstractmethod
    def _list_ids(self):
        """列出当前表内的 id 列表"""
