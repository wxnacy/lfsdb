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
