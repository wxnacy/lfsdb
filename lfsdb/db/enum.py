#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
异常
"""

from wpy.base import BaseEnum

class QueryOperator(BaseEnum):
    IN = '$in'
    NIN = '$nin'
    GT = '$gt'      # 大于
    GTE = '$gte'    # 大于等于
    LT = '$lt'      # 小于
    LTE = '$lte'    # 小于等于

class TableFunction(BaseEnum):
    FIND = 'find'
    FIND_BY_ID = 'find_by_id'
    FIND_ONE = 'find_one'
    INSERT = 'insert'
    UPDATE = 'update'
    DELETE = 'delete'
    DROP = 'drop'

    @classmethod
    def write_values(cls):
        """写入类操作"""
        return (cls.INSERT.value, cls.UPDATE.value, cls.DELETE.value,
            cls.DROP.value)
