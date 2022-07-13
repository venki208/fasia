#!/usr/bin/env python
import sys
import pandas as pd
import pymongo
import json
import os
import sys



def import_content(filepath):
    mng_client = pymongo.MongoClient('localhost', 27017, username='fasiaadmin', password='fasiaadmin@123#', authSource='fasiadb', authMechanism='SCRAM-SHA-1')
    mng_db = mng_client['fasiadb'] # Replace mongo db name
    collection_name = 'u_s_zipcode' # Replace mongo db collection name
    db_cm = mng_db[collection_name]
    cdir = os.path.dirname(__file__)
    file_res = os.path.join(cdir, filepath)

    data = pd.read_csv(file_res)
    data_json = json.loads(data.to_json(orient='records'))
    db_cm.remove()
    db_cm.insert(data_json)

if __name__ == "__main__":
  arg = sys.argv[1]
  print arg
  filepath = arg  # pass csv file path
  import_content(filepath)
