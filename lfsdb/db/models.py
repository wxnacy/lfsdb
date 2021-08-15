#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""

"""

import os
import uuid
from datetime import datetime

from .client import FileStorage

fs = FileStorage()

class FSColumn(object):
    datatype = None
    default = None

    def __init__(self, datatype, **kwargs):
        self.datatype = datatype
        for k, v in kwargs.items():
            setattr(self, k, v)
        if self.default == None:
            if issubclass(datatype, int):
                self.default = 0

    def value(self):
        val = str(self.default()) if callable(self.default) else self.default
        if not val:
            val = self.datatype()
        return val

class FSModel(object):
    db = ''
    table = ''
    _db = None

    _id = FSColumn(str, default = uuid.uuid4)
    _create_time = FSColumn(datetime, default=datetime.now)
    _update_time = FSColumn(datetime, default=datetime.now)

    def __init__(self, **kwargs):
        init_data = self.__default_dict__()
        init_data.update(kwargs)
        for k, v in init_data.items():
            setattr(self, k, v)

    @classmethod
    def __default_dict__(cls):
        '''获取默认 dict'''
        res = {}
        classes = [cls]
        # 兼容父类的 __dict__
        classes.extend(cls.__bases__)
        for clz in classes:
            for k, v in clz.__dict__.items():
                if isinstance(v, FSColumn):
                    res[k] = v.value()
        return res

    @classmethod
    def db_col(cls, **kwargs):
        table = cls.table.format(**kwargs)
        return fs.get_db(cls.db).get_table(table)

    @classmethod
    def insert(cls, data):
        """插入数据"""
        item = cls(**data)
        item.save()
        return item

    @classmethod
    def find_one_by_id(cls, _id, db_col=None):
        if not db_col:
            db_col = {}
        item = cls.db_col(**db_col).find_one_by_id(_id)
        return cls(**item) if item else None

    @classmethod
    def find(cls, query=None, db_col=None, **kwargs):
        """查找列表"""
        if not db_col:
            db_col = {}
        items = cls.db_col(**db_col).find(query, **kwargs)
        return [cls(**item) for item in items]

    def delete(self):
        """删除"""
        return self.db_col(**self.__dict__).delete({ "_id": self._id })

    def save(self):
        """保存"""
        data = self.__default_dict__()
        data.update(self.__dict__)
        db = self.db_col(**self.__dict__)
        item = db.find_one_by_id(self._id)
        if item:
            data.pop('_id', None)
            db.update({ "_id": self._id }, data)
        else:
            db.insert(data)

    def to_dict(self):
        return dict(self.__dict__)
