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

    def exists(self, data):
        """判断是否存在符合的数据"""
        if not data:
            return False
        for k, v in self._query.items():
            value = data.get(k)
            if not _exists(v, value):
                return False
            print(k, v, value)
            #  if isinstance(v, str):
                #  if value != v:
                    #  return False
            if isinstance(v, dict):
                for sk, sv in v.items():
                    if sk == "$in":
                        if not isinstance(sv, list):
                            raise FSQueryError(
                                'after query $in value must be list')
                        if value not in sv:
                            return False
        return True


@singledispatch
def _exists(query_value, value):
    return True

@_exists.register(str)
def _(str_value, value):
    print('str')
    return str_value == value

@_exists.register(str)
def _(str_value, value):
    print('str')
    return str_value == value

if __name__ == "__main__":
    _exists('value', '')
