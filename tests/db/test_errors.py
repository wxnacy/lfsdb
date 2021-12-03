#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
随机方法
"""


from lfsdb.db.errors import FSQueryError
from lfsdb.db.errors import LfsdbError

def test_get_error():

    e = LfsdbError.get_error('FSQueryError')
    assert issubclass(e, FSQueryError)
