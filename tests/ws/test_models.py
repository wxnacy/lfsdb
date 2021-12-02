#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com

from lfsdb.ws.models import SocketModel

def test_socket_model_dumps():
    sm = SocketModel()
    sm.db = 'test_db'
    sm.table = 'test_table'
    sm.method = 'find'
    sm.params = { "id": "test" }

    dump_data = sm.dumps()
    assert type(dump_data) == bytes

    sm2 = SocketModel.loads(dump_data)

    assert isinstance(sm2, SocketModel)

    assert sm.db == sm2.db
    assert sm.table == sm2.table
    assert sm.method == sm.method
    assert sm.params == sm.params
