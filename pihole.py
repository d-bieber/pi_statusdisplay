#!/usr/env python
# coding: utf-8


import urllib2 as url
import json

def getStatus():
    try:
        response = url.urlopen('http://192.168.2.200/admin/api.php?status')
    except:
        return False
    else:
        data = json.load(response)
        if(data['status'] == "enabled"):
            return True
        else:
            return False

def getQueries():
    try:
        response = url.urlopen('http://192.168.2.200/admin/api.php')
    except:
        ret = -1
    else:
        data = json.load(response)
        ret = '{0:,}'.format(data['dns_queries_today'])
    return ret

def getBlocked():
    try:
        response = url.urlopen('http://192.168.2.200/admin/api.php')
    except:
        ret = -1
    else:
        data = json.load(response)
        ret = '{0:,}'.format(data['ads_blocked_today'])
    return ret

def getPercentage():
    try:
        response = url.urlopen('http://192.168.2.200/admin/api.php')
    except:
        ret = -1
    else:
        data = json.load(response)
        h = data['ads_percentage_today']
        ret = round(h,2)
    return ret

