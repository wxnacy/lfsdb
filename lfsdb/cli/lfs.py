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
    item = db.get_db(_db).get_table(table).find_one_by_id(_id)
    print(json.dumps(item, indent=4))
    #  print('s')
    #  task = db.get_db('download').get_table('task')
    #  #  task.insert({"name": "test"})
    #  items = task.find()
    #  for item in items:
        #  print(json.dumps(item, indent=4))

if __name__ == "__main__":
    main()
