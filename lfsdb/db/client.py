#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
文件存储
"""

import os
import shutil
from datetime import datetime
from wpy.files import FileUtils
from wpy.files import ZipUtils
from .base import BaseTable
from lfsdb.common.loggers import get_logger

class FileStorage(object):
    logger = get_logger('FileStorage')

    def __init__(self, root=None):
        """
        :param str root: 数据存储根路径
        """
        # 处理数据库存储位置
        if not root:
            root = os.path.expanduser('~/.lfsdb')
        if not root.endswith('/data'):
            root = os.path.join(root, 'data')

        self.root = root
        self.logger.info('FileStorage root %s', self.root)
        # 备份根路径
        self.dump_root = os.path.expanduser('~/.lfsdb/dump')
        self.logger.info('FileStorage dump_root %s', self.dump_root)

        # 创建目录
        if not os.path.exists(self.root):
            os.makedirs(self.root)
        if not os.path.exists(self.dump_root):
            os.makedirs(self.dump_root)

    def list_db_names(self):
        """列出数据名列表"""
        if not os.path.exists(self.root):
            return []
        return os.listdir(self.root)

    def get_db(self, db):
        """获取数据库"""
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
        # TODO 缺失单侧
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

class FileTable(BaseTable):
    def __init__(self, root, db, table):
        self.table = table
        # 表根路径
        self.table_root = os.path.join(os.path.expanduser(root), db, table)
        #  self._create_table_root()

    def _create_table_root(self):
        if not os.path.exists(self.table_root):
            os.makedirs(self.table_root)

    def _write(self, doc):
        """写入数据"""
        self._create_table_root()
        _id = doc['_id']
        doc_path = os.path.join(self.table_root, _id)
        # 写入文件
        FileUtils.write_dict(doc_path, doc)
        return True

    def drop(self):
        """删除表"""
        if os.path.exists(self.table_root):
            # 删除本地表目录
            shutil.rmtree(self.table_root)


    def _delete_by_id(self, _id):
        os.remove(self._generage_path(_id))
        return True

    def _update(self, doc):
        _id = doc.get("_id")
        FileUtils.write_dict(self._generage_path(_id), doc)
        return True


    def _list_ids(self):
        """列出当前表内的 id 列表"""
        if not os.path.exists(self.table_root):
            return []
        return os.listdir(self.table_root)

    def _read_by_id(self, _id):
        """使用 _id 读取数据"""
        try:
            return FileUtils.read_dict(self._generage_path(_id))
        except Exception as e:
            return None

    def _generage_path(self, _id):
        """根据 _id 构建存储地址"""
        return os.path.join(self.table_root, _id)

    def _exists_id(self, _id):
        """是否存在 _id"""
        return os.path.exists(self._generage_path(_id))
