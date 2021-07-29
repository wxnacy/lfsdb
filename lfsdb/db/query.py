#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
query
"""
from .errors import FSQueryError

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
            value = data.get("k")
            if isinstance(v, str):
                if value != v:
                    return False
            if isinstance(v, dict):
                for sk, sv in v.items():
                    if sk == "$in":
                        if not isinstance(sv, list):
                            raise FSQueryError(
                                'after query $in value must be list')
                        if value not in sv:
                            return False
        return True

