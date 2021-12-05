#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""

"""


import json
from lfsdb.db.client import FileStorage

db = FileStorage()

def main():
    import sys
    args = sys.argv[1:]
    _db = args[0]
    table = args[1]
    _id = args[2]
    fields = []
    if len(args) > 3:
        fields = args[3:]
    item = db.get_db(_db).get_table(table).find_by_id(_id)
    data = {}
    print(fields)
    if fields:
        for f in fields:
            data[f] = item.get(f)
    else:
        data = item
    print(json.dumps(data, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()
