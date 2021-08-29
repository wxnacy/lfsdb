#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
query
"""
from .errors import FSQueryError
from .enum import QueryOperator
from functools import singledispatch

class FSQuery(object):
    _query = {}
    def __init__(self, query):
        if not query:
            query = {}
        self._query = query

    def exists(self, doc):
        """判断是否存在符合的数据"""
        if not doc:
            return False
        for k, v in self._query.items():
            value = doc.get(k)
            if not _exists(v, value):
                return False
        return True

    def filter(self, docs):
        """获取数据列表"""
        items = []
        for doc in docs:
            if self.exists(doc):
                items.append(doc)
        return items

@singledispatch
def _exists(query_value, value):
    return query_value == value

@_exists.register(dict)
def _(dict_value, value):
    if QueryOperator.IN.value in dict_value:
        v = dict_value.get(QueryOperator.IN.value)
        if not isinstance(v, list):
            raise FSQueryError('after query $in value must be list')
        if isinstance(value, list):
            # 如果字段为列表，那其中有指定数据则返回 True
            for sv in value:
                if sv in v:
                    return True
            return False
        else:
            if value not in v:
                return False
    # 不包含
    if QueryOperator.NIN.value in dict_value:
        v = dict_value.get(QueryOperator.NIN.value)
        if not isinstance(v, list):
            raise FSQueryError('after query $nin value must be list')
        if isinstance(value, list):
            for sv in value:
                if sv in v:
                    return False
        else:
            if value in v:
                return False
    if QueryOperator.GT.value in dict_value:
        v = dict_value.get(QueryOperator.GT.value)
        if value <= v:
            return False

    if QueryOperator.GTE.value in dict_value:
        v = dict_value.get(QueryOperator.GTE.value)
        if value < v:
            return False

    if QueryOperator.LT.value in dict_value:
        v = dict_value.get(QueryOperator.LT.value)
        if value >= v:
            return False

    if QueryOperator.LTE.value in dict_value:
        v = dict_value.get(QueryOperator.LTE.value)
        if value > v:
            return False

    return True

if __name__ == "__main__":
    _exists('value', '')
