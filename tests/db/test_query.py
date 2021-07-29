#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
随机方法
"""

import pytest
import os

from lfsdb.db.query import FSQuery
from lfsdb.db.errors import FSQueryError

def test_exists():
    query = { "name": "wxnacy" }
    data = { "name": "wxnacy" }
    assert FSQuery(query).exists(data)

    query = { "status": { "$in": ['success'] } }
    data = { "status": "success" }
    assert FSQuery(query).exists(data)

    query = { "status": { "$in": ['success'] } }
    data = { "status": "failed" }
    assert not FSQuery(query).exists(data)

    query = { "status": { "$in": 'success' } }
    data = { "status": "failed" }
    with pytest.raises(FSQueryError) as exe_info:
        assert not FSQuery(query).exists(data)
        assert str(exe_info) == 'after query $in value must be list'
    assert 1 == 2
