#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
文件存储
"""


import os
import shutil
import uuid
from datetime import datetime
from wpy.files import FileUtils
from wpy.files import ZipUtils
from .errors import FileStorageError
from .errors import FSQueryError
from .query import FSQuery

class FileStorage(object):
    def __init__(self, root=None):
        if not root:
            root = os.path.expanduser('~/.lfsdb/data')
        self.root = root
        self.dump_root = os.path.expanduser('~/.lfsdb/dump')
        if not os.path.exists(self.root):
            os.makedirs(self.root)
        if not os.path.exists(self.dump_root):
            os.makedirs(self.dump_root)

    def list_db_names(self):
        if not os.path.exists(self.root):
            return []
        return os.listdir(self.root)

    def get_db(self, db):
        return FileDB(self.root, db)

class FileDB(FileStorage):
    def __init__(self, root, db):
        super().__init__(root)
        self.db = db

        self.db_root = os.path.join(os.path.expanduser(root), db)

    def _create_db_root(self):
        self._create_root(self.db_root)

    def _create_root(self, root):
        if not os.path.exists(root):
            os.makedirs(root)

    def list_table_names(self):
        """列出表名列表"""
        if not os.path.exists(self.db_root):
            return []
        return os.listdir(self.db_root)

    def get_table(self, table):
        return FileTable(self.root, self.db, table)

    def dump(self, dump_root=None):
        """
        备份数据库
        :param str dump_root: 备份目录，空值，则使用默认目录
        """
        if not dump_root:
            dump_root = self.dump_root
        dump_root = os.path.expanduser(dump_root)
        path = os.path.join(dump_root, 'lfsdb_{}_{}_dump'.format(self.db,
            datetime.now().strftime("%Y%m%d%H%M%S")))
        print('备份地址:', path)
        ZipUtils.zip(self.db_root, path)

    def store(self, dump_path=None):
        """恢复备份
        :param str dump_path: 备份文件地址
                                1、绝对路径
                                2、文件名称
                                3、空（使用最新备份）
                                4、目录（使用目录下最新备份）
        """
        print('恢复备份会覆盖当前数据')
        if not dump_path:
            dump_path = self._get_last_dump_name(self.dump_root)
        if os.path.isdir(dump_path):
            dump_name = self._get_last_dump_name(dump_path)
            if not dump_name:
                print('当前无备份')
                return
            dump_path = os.path.join(dump_path, dump_name)
        if not dump_path:
            print('当前无备份')
            return
        if dump_path.startswith('lfsdb_'):
            dump_path = os.path.join(self.dump_root, dump_path)
        if not os.path.exists(dump_path):
            print('备份文件不存在:', dump_path)
            return
        print('使用备份文件:', dump_path)

        ZipUtils.unzip(dump_path, self.root)

    def _get_last_dump_name(self, dump_root):
        """获取最后一个备份名"""
        names = os.listdir(dump_root)
        names = [o for o in names if 'lfsdb_{}'.format(self.db) in o]
        names.sort(key = lambda x: x, reverse=True)
        return names[0] if names else None

class FileTable(FileDB):
    def __init__(self, root, db, table):
        super().__init__(root, db)
        self.table = table
        self.table_root = os.path.join(os.path.expanduser(root), db, table)

    def _create_table_root(self):
        self._create_root(self.table_root)

    def _generage_id(self):
        """生成 id"""
        return str(uuid.uuid4())

    def insert(self, doc):
        data = dict(doc)
        self._create_table_root()
        _id = doc.get("_id") or self._generage_id()
        if self._exists_id(_id):
            raise FileStorageError('{}._id {} is exists'.format(self.table, _id))
        data['_id'] = _id
        data['_create_time'] = self._now()
        data['_update_time'] = self._now()
        table_path = os.path.join(self.table_root, _id)
        FileUtils.write_dict(table_path, data)
        return _id

    def find_one_by_id(self, _id):
        """通过 _id 查找"""
        if self._exists_id(_id):
            return self._read_by_id(_id)
        return None

    def find(self, query=None, projection=None, **kwargs):
        if not query:
            query = {}
        if not projection:
            projection = {}
        projection_id_type = projection.pop('_id', None)
        projection_values = set(projection.values())
        projection_type = list(projection_values)[0] if len(
                projection_values) > 0 else None
        if len(projection_values) > 1:
            raise FSQueryError(('Projection cannot have a mix of inclusion'
                ' and exclusion.'))

        if '_id' in query:
            item = self.find_one_by_id(query['_id'])
            return [item] if item else []
        ids = self._list_ids()
        res = []
        fsquery = FSQuery(query)
        for _id in ids:
            doc = self._read_by_id(_id)
            if fsquery.exists(doc):
                doc = self._get_projection_doc(doc, projection, projection_type)
                if projection_id_type == 1:
                    doc['_id'] = _id
                elif projection_type == 0:
                    doc.pop('_id', None)
                res.append(doc)

        res.sort(key = lambda x: x.get("_create_time", ''))
        return res

    def find_one(self, query=None, projection=None, **kwargs):
        docs = self.find(query, projection, **kwargs)
        return docs[0] if docs else None

    def count(self, query):
        return len(self.find(query))

    def update(self, query, update_data):
        if '_id' in update_data:
            raise FileStorageError('_id can not update')
        docs = self.find(query)
        count = 0
        for doc in docs:
            doc.update(update_data)
            if self._update(doc):
                count += 1
        return count

    def delete(self, query):
        """删除数据"""
        docs = self.find(query)
        count = 0
        for doc in docs:
            _id = doc.get("_id")
            if self._delete_by_id(_id):
                count += 1
        return count

    def drop(self):
        """删除表"""
        if os.path.exists(self.table_root):
            #  os.removedirs(self.table_root)
            shutil.rmtree(self.table_root)

    def _get_projection_doc(self, doc, projection, projection_type):
        if not projection:
            return doc

        if projection_type == 0:
            for k, v in projection.items():
                doc.pop(k)
            return doc
        res = {"_id": doc.get("_id")}
        for k, v in projection.items():
            if v == 1 and k in doc:
                res[k] = doc[k]
        return res

    def _delete_by_id(self, _id):
        if self._exists_id(_id):
            os.remove(self._generage_path(_id))
            return True
        return False

    def _update(self, doc):
        _id = doc.get("_id")
        doc['_update_time'] = self._now()
        FileUtils.write_dict(self._generage_path(_id), doc)
        return True

    def _now(self):
        return str(datetime.now())

    def _exists_doc(self, query, doc):
        for k, v in query.items():
            if doc.get(k) != v:
                return False
        return True

    def _list_ids(self):
        if not os.path.exists(self.table_root):
            return []
        return os.listdir(self.table_root)

    def _read_by_id(self, _id):
        try:
            return FileUtils.read_dict(self._generage_path(_id))
        except Exception as e:
            return {}

    def _generage_path(self, _id):
        """根据 _id 构建存储地址"""
        return os.path.join(self.table_root, _id)

    def _exists_id(self, _id):
        """是否存在 _id"""
        return os.path.exists(self._generage_path(_id))
