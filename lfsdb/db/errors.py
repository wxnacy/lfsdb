#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
异常
"""

class LfsdbError(Exception):
    NAME = ''

    @classmethod
    def get_error(cls, name):
        for item in cls.__subclasses__():
            if item.NAME == name:
                return item
        return None

class FileStorageError(LfsdbError):
    NAME = 'FileStorageError'

class FSQueryError(LfsdbError):
    NAME = 'FSQueryError'

