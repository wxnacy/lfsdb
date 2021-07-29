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

    query = { "name": "wxnacy" }
    data = { "name": "wen" }
    assert not FSQuery(query).exists(data)

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

    query = { "status": { "$nin": ['success'] } }
    data = { "status": "failed" }
    assert FSQuery(query).exists(data)

    query = { "status": { "$nin": ['success'] } }
    data = { "status": "success" }
    assert not FSQuery(query).exists(data)

    query = { "status": { "$nin": 'success' } }
    data = { "status": "failed" }
    with pytest.raises(FSQueryError) as exe_info:
        assert not FSQuery(query).exists(data)
        assert str(exe_info) == 'after query $nin value must be list'

    # $gt
    query = { "time": { "$gt": "2021-07-30 00:01:46" } }
    data = { "time": "2021-07-30 00:03:04" }
    assert FSQuery(query).exists(data)

    query = { "time": { "$gt": "2021-07-30 00:05:46" } }
    data = { "time": "2021-07-30 00:03:04" }
    assert not FSQuery(query).exists(data)

    query = { "time": { "$gt": "2021-07-30 00:03:04" } }
    data = { "time": "2021-07-30 00:03:04" }
    assert not FSQuery(query).exists(data)

    # $gte
    query = { "time": { "$gte": "2021-07-30 00:01:46" } }
    data = { "time": "2021-07-30 00:03:04" }
    assert FSQuery(query).exists(data)

    query = { "time": { "$gte": "2021-07-30 00:05:46" } }
    data = { "time": "2021-07-30 00:03:04" }
    assert not FSQuery(query).exists(data)

    query = { "time": { "$gte": "2021-07-30 00:03:04" } }
    data = { "time": "2021-07-30 00:03:04" }
    assert FSQuery(query).exists(data)

    # $lt
    query = { "time": { "$lt": "2021-07-30 00:01:46" } }
    data = { "time": "2021-07-30 00:03:04" }
    assert not FSQuery(query).exists(data)

    query = { "time": { "$lt": "2021-07-30 00:05:46" } }
    data = { "time": "2021-07-30 00:03:04" }
    assert FSQuery(query).exists(data)

    query = { "time": { "$lt": "2021-07-30 00:03:04" } }
    data = { "time": "2021-07-30 00:03:04" }
    assert not FSQuery(query).exists(data)

    # $lte
    query = { "time": { "$lte": "2021-07-30 00:01:46" } }
    data = { "time": "2021-07-30 00:03:04" }
    assert not FSQuery(query).exists(data)

    query = { "time": { "$lte": "2021-07-30 00:05:46" } }
    data = { "time": "2021-07-30 00:03:04" }
    assert FSQuery(query).exists(data)

    query = { "time": { "$lte": "2021-07-30 00:03:04" } }
    data = { "time": "2021-07-30 00:03:04" }
    assert FSQuery(query).exists(data)

def test_filter():
    query = { "name": "wxnacy" }
    items = [
        { "name": "wxnacy"  },
        { "name": "wen"  },
    ]
    assert len(FSQuery(query).filter(items)) == 1
