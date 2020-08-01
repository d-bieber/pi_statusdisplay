#!/usr/env python
# coding: utf-8


import urllib.request as url
import json

def getStatus(ip):
    try:
        response = url.urlopen('http://' + ip + '/admin/api.php?status')
    except:
        return False
    else:
        data = json.load(response)
        if(data['status'] == "enabled"):
            return True
        else:
            return False

def getQueries(ip):
    try:
        response = url.urlopen('http://' + ip + '/admin/api.php')
    except:
        ret = -1
    else:
        data = json.load(response)
        ret = '{0:,}'.format(data['dns_queries_today'])
    return ret

def getBlocked(ip):
    try:
        response = url.urlopen('http://' + ip + '/admin/api.php')
    except:
        ret = -1
    else:
        data = json.load(response)
        ret = '{0:,}'.format(data['ads_blocked_today'])
    return ret

def getPercentage(ip):
    try:
        response = url.urlopen('http://' + ip + '/admin/api.php')
    except:
        ret = -1
    else:
        data = json.load(response)
        h = data['ads_percentage_today']
        ret = round(h,2)
    return ret
