#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
随机方法
"""

import pytest
import os

from wpy.path import read_dict
from wpy.randoms import (
         random_str
        )

from lfsdb import FileStorage
from lfsdb.db import FileStorageError
from lfsdb.db.errors import FSQueryError
from lfsdb.db.cache import CacheTable
from lfsdb.db.client import FileTable
from lfsdb.sockets.db import SocketTable

root = '/tmp'
root = None
db_name = 'wpy_db'
table = 'wpy_table'

fs = FileStorage(root)

file_table = fs.get_db(db_name).get_table(table)
socket_table = SocketTable(db_name, table)
cache_table = CacheTable(db_name, table)

tables = [file_table, socket_table, cache_table]

table_root = os.path.join(fs.root, db_name, table)

def _origin_data(data):
    for k in ('_id', '_update_time', "_create_time"):
        data.pop(k, None)
    return data

def _handle_table_test(func):
    for table in tables:
        table.drop()
        func(table)
        table.drop()

def test_insert():
    _handle_table_test(_test_insert)

def _test_insert(db):
    name = random_str(6)
    doc = {
        "name": name
    }
    # 查看插入的数据是否存入到文件中
    _id = db.insert(doc)
    if isinstance(db, FileTable):
        path = os.path.join(table_root, _id)
        data = read_dict(path)
        data = _origin_data(data)
        assert doc == data

    data = db.find_by_id(_id)
    data = _origin_data(data)
    assert doc == data

    doc['_id'] = _id
    with pytest.raises(FileStorageError) as excinfo:
        db.insert(doc)
        assert str(excinfo) == '{}._id {} is exists'.format(table, _id)

    db.drop()

    assert not os.path.exists(table_root)

def test_find():
    _handle_table_test(_test_find)

def _test_find(db):
    name = random_str(6)
    doc = { "name": name}
    db.drop()
    db.insert(doc)
    db.insert(doc)
    doc['age'] = 12
    db.insert(doc)

    # 条件为空
    docs = db.find()
    assert len(docs) == 3

    docs = db.find({ "name": name })
    assert len(docs) == 3

    docs = db.find({ "name": name, "age": 12 })
    assert len(docs) == 1

    doc = db.find_one({"age": 12}, {})
    assert len(doc.keys()) == 5

    doc = db.find_one({"age": 12}, {"name": 1})
    assert len(doc.keys()) == 2

    with pytest.raises(FSQueryError) as exe_info:
        doc = db.find_one({"age": 12}, {"name": 1, "age": 0})
        assert str(exe_info) == ('Projection cannot have a mix of inclusion'
                ' and exclusion.')

    doc = db.find_one({"age": 12}, {"name": 1, "_id": 0})
    assert len(doc.keys()) == 2

    db.drop()

def test_update():
    _handle_table_test(_test_update)

def _test_update(db):
    # TODO 缓存
    name = random_str(6)
    doc = { "name": name}
    db.insert(doc)
    _id = db.insert(doc)
    insert_utime = db.find_by_id(_id).get("_update_time")
    db.insert(doc)

    count = db.update(doc, {"name": "wxnacy"})
    assert count == 3

    db.update({"_id": _id}, {"name": "wxn"})
    data = db.find_by_id(_id)
    update_utime = data.get("_update_time")
    # 检查修改时间是否改变
    assert insert_utime < update_utime

    data = db.find_by_id(_id)
    data = _origin_data(data)
    assert { "name": "wxn" } == data

    db.drop()

def test_delete():
    _handle_table_test(_test_delete)

def _test_delete(db):
    db.drop()
    name = random_str(6)
    doc = { "name": name}
    db.insert(doc)
    _id = db.insert(doc)
    db.insert(doc)

    assert db.delete({ "_id": _id }) == 1

    docs = db.find()
    assert len(docs) == 2

    count = db.delete(doc)
    assert count == 2

    db.drop()

def test_sort():
    _handle_table_test(_test_sort)

def _test_sort(db):
    db.drop()

    arr = [{"age": 5, "id": 2}, {"age": 5, "id": 5}, {"age": 3, "id": 4}]
    for a in arr:
        db.insert(a)
    items = db.find(sorter = [('age', 1), ('id', -1)])
    for item in items:
        item.pop('_id', None)
        item.pop('_create_time', None)
        item.pop('_update_time', None)

    assert items == [{"age": 3, "id": 4},{"age": 5, "id": 5}, {"age": 5, "id": 2}]

    db.drop()

socket_table.close()
