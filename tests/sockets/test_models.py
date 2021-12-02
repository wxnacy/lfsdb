#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com

from lfsdb.sockets.models import PickleModel

def test_pickle_model_dumps():
    sm = PickleModel()
    sm.db = 'test_db'
    sm.table = 'test_table'
    sm.method = 'find'
    sm.params = { "id": "test" }

    dump_data = sm.dumps()
    assert type(dump_data) == bytes

    sm2 = PickleModel.loads(dump_data)

    assert sm.db == sm2.db
    assert sm.table == sm2.table
    assert sm.method == sm.method
    assert sm.params == sm.params
