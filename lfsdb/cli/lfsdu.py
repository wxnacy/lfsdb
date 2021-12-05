#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""

"""

import os
import m3u8
import hashlib
from collections import defaultdict

from wpy.files import FileUtils
from lfsdb import FSModel
from lfsdb import FSColumn

def md5(content):
    h = hashlib.md5()
    h.update(content.encode())
    return h.hexdigest()

def md5_file(filepath):
    h = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
        return h.hexdigest()

class File(FSModel):
    db = 'filesystem'
    table = 'file'

    path = FSColumn(str)
    md5 = FSColumn(str)
    md5_count = FSColumn(int)
    size = FSColumn(int)

def col_md5(dirname):
    count = 0
    dirname = os.path.expanduser(dirname)
    for path in FileUtils.file_iter(dirname):
        _id = md5(path)
        print(_id, path)
        count += 1
        video = File.find_by_id(_id)
        if video:
            continue
        video = File(_id = md5(path))
        video.path = path
        video.md5 = md5_file(path)
        video.size = os.path.getsize(path)
        video.save()
    print(count)

def repeat():
    videos = File.find()
    for video in videos:
        if not os.path.exists(video.path):
            video.delete()
    videos = File.find()
    md5_data = defaultdict(list)
    for video in videos:
        md5_data[video.md5].append(video)

    for md5, videos in md5_data.items():
        if len(videos) == 1:
            continue
        print('=' * 10)
        for video in videos:
            print(md5, video.size / 1024.0 / 1024.0, video.path)

def main():
    """添加任务"""
    import sys
    action = sys.argv[1:][0]
    if action == 'md5':
        dirname = sys.argv[1:][1]
        #  dirname = '/Users/wxnacy/Movies/xvideos'
        col_md5(dirname)
    if action == 'repeat':
        repeat()

