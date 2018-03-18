#!/usr/bin/env python
'''
Loads Raw data into Mongo Database
'''

from flask import Flask
from datetime import datetime
import traceback
import configparser
import sys
from bson.json_util import loads
from bson.json_util import dumps
from pymongo import MongoClient
import os.path



def readCatalog(catalog,key):
    '''
    Reads entryies from paramter catalog
    '''
    try:
        entry = catalog.find_one({'_id': key})
        print(entry)
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print('%s %s' % (exc_type,exc_value))
        traceback.print_tb(exc_traceback)

def errorLog(errors,src,msg):
    obj = {}
    obj['date'] = datetime.now()
    obj['source'] = src
    obj['msg'] = msg
    errors.insert_one(obj)

def loadRawData(catmap,raw,errors,data):
    ''' 
    Data loading procedure
    '''
    try:
        obj = {}
        tok = data.split(';')
        now = datetime.now()
        obj['_id'] = '%s_%s' % (tok[0],now.strftime('%Y%m%d-%H%M%S.%f'))
        obj['loaddate'] = datetime.now()
        obj['meter'] = tok[0]
        obj['testdate'] = datetime.strptime(tok[1],'%Y%m%d%H%M%S') 
        tok.pop(0)
        tok.pop(0)
        for item in tok:
            if item[:2] in catmap:
                catitem = catmap[item[:2]]
                name = catitem['name']
                value = item[2:]
                # Convert?
                if (catitem['type'] == 'F'):
                    obj[name] = float(value)
                else:
                    obj[name] = value
            else:
                errorLog(errors,data,'Unknown parameter %s' % item[:2])

        raw.insert(obj)
        print('Updated db')
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        errorLog(errors,data,'%s %s' % (exc_type,exc_value))
        traceback.print_tb(exc_traceback)
        raise



# Config File
fp = '/usr/local/etc/config.ini'
if not os.path.isfile(fp):
    print("Can't find config file: %s" % fp)
    sys.exit(1)

config = configparser.ConfigParser()
config.read_file(open(fp))

client = MongoClient(config['mongo']['host'],int(config['mongo']['port']))
db = client.data
raw = db.raw
errors = db.errors

# Load catmap
catmap = {}
catalog = db.catalog
cursor = catalog.find()
for doc in cursor:
    catmap[doc['_id']] = doc

# Sample Data
#data = "01;20180316113000;0125.0;0220;0323;046.8"
#loadRawData(catmap,raw,data)
#sys.exit(0)


app = Flask(__name__)

@app.route('/')
def root():
    return('Hello')

@app.route('/d/<data>')
def data_input(data=None):
    if (data is None):
        return('Data not supplied\n')
    else:
        try:
            loadRawData(catmap,raw,errors,data)
            return('Loaded data...\n')
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print('%s %s' % (exc_type,exc_value))
            return('Error Loading Data: %s\n' % traceback.print_tb(exc_traceback))
