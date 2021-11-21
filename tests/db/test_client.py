#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
随机方法
"""

import pytest
import os

from lfsdb import FileStorage
from lfsdb.db import FileStorageError
from lfsdb.db.errors import FSQueryError
from wpy.files import FileUtils
from wpy.tools import randoms

root = '/tmp'
root = None
db_name = 'wpy_db'
table = 'wpy_table'
db = FileStorage(root).get_db(db_name).get_table(table)
table_root = os.path.join(db.root, db_name, table)

def _origin_data(data):
    for k in ('_id', '_update_time', "_create_time"):
        data.pop(k, None)
    return data

def test_insert():
    name = randoms.random_str(6)
    doc = {
        "name": name
    }
    _id = db.insert(doc)

    path = os.path.join(table_root, _id)
    data = FileUtils.read_dict(path)
    data = _origin_data(data)
    assert doc == data

    data = db.find_one_by_id(_id)
    data = _origin_data(data)
    assert doc == data

    doc['_id'] = _id
    with pytest.raises(FileStorageError) as excinfo:
        db.insert(doc)
        assert str(excinfo) == '{}._id {} is exists'.format(table, _id)

    db.drop()

    assert not os.path.exists(table_root)

def test_find():
    name = randoms.random_str(6)
    doc = { "name": name}
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
    name = randoms.random_str(6)
    doc = { "name": name}
    db.insert(doc)
    _id = db.insert(doc)
    db.insert(doc)

    count = db.update(doc, {"name": "wxnacy"})
    assert count == 3

    data = db.find_one_by_id(_id)
    data = _origin_data(data)
    #  assert { "name": "wxnacy" } == data

    db.drop()

def test_delete():
    name = randoms.random_str(6)
    doc = { "name": name}
    db.insert(doc)
    _id = db.insert(doc)
    db.insert(doc)

    count = db.delete(doc)
    assert count == 3

    db.drop()

def test_sort():

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
