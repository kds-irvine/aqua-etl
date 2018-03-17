#!/usr/bin/env python

from datetime import datetime
import sys

def translate(catalog,key):
    if key in catalog:
        return catalog[key]
    else:
        return None


def parseData(catalog,input):
    try:
        obj = {}
        tok = input.split(';')
        obj['id'] = tok[0]
        obj['date'] = datetime.strptime(tok[1],'%Y%m%d%H%M%S')
        tok.pop(0)
        tok.pop(0)
        for item in tok:
            citem = translate(catalog,item[:2])
            if citem is not None:
                name = citem.name
                value = item[2:]
                obj[name] = value
        print(obj)
    except:
        print("Unexpected error:", sys.exc_info()[0])

data = "01;20180316113000;0125.0;0220;0323;046.8;"


catalog = {}
citem = {}
citem['name'] = 'Temp'
citem['uom'] = 'Cel'
citem['min'] = 0
citem['max'] = 40
catalog['01'] = citem

citem['name'] = 'EC'
citem['uom'] = 'micro siemens/cm'
citem['min'] = 0
citem['max'] = 50000
catalog['02'] = citem

citem['name'] = 'Oxygen'
citem['uom'] = 'mg/l'
citem['min'] = 0
citem['max'] = 18
catalog['03'] = citem

citem['name'] = 'pH'
citem['uom'] = 'ph units'
citem['min'] = 0
citem['max'] = 14
catalog['04'] = citem

print('parser')

parseData(catalog,data)

