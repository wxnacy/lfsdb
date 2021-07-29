#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
随机方法
"""

import pytest
import os

from lfsdb.db.query import FSQuery

def test_exists():
    query = { "name": "wxnacy" }
    data = { "name": "wxnacy" }
