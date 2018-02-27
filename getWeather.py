#!/usr/env python
# coding: utf-8

import urllib2 as url
import time as time
import json

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

LOCATION_ID = 'YOURDATA'

def umlaute(string):
    string=string.replace('ä', 'ae')
    string=string.replace('ö', 'oe')
    string=string.replace('ü', 'ue')
    string=string.replace('Ä', 'Ae')
    string=string.replace('Ö', 'Oe')
    string=string.replace('Ü', 'Ue')
    string=string.replace('ß', 'ss')
    return string

def getWeather():

    try:
        response = url.urlopen('http://api.openweathermap.org/data/2.5/'+ YOURDATA)

        data = json.load(response)
    except Exception, e:
        condition1 = "Fehler"
        temp1 = "  -"
        condition2 = "Fehler"
        temp2 = "  -"

    else:
        temp1=data['list'][0]['main']['temp']
        condition1=data['list'][0]['weather'][0]['description']

        temp2=data['list'][1]['main']['temp']
        condition2=data['list'][1]['weather'][0]['description']

    lt = time.localtime()
    zeit = time.strftime("%H:%M",lt)
       
    w_out = open("weather.wtd","w")
    w_out.write(str(temp1) + "\n" + condition1 + "\n" + str(temp2) + "\n" + condition2 + "\n" + zeit)
    w_out.close()


def getUnweather():
    w_out = open("storm.wtd","w")
    try:
        response = url.urlopen('http://www.dwd.de/DWD/warnungen/warnapp/json/warnings.json')
    except:
        w_out.write('error')
        w_out.close()
        return
    else:
        html = response.read()
        html = html[24:-2]
        try:
            data_u = json.loads(html)
        except:
            w_out.write('error')
            w_out.close()
            return
        else:
            region = ""
            w_count = 0
            w_headline = 'NA'
            w_description = 'NA'
            v_count = 0
            v_headline = 'NA'
            v_description = 'NA'

            warnString = "\n"
            vWarnString = ""
            try:
                warnung = data_u['warnings']['105374000']
            except:
                pass
            else:
                w_count = len(warnung)
                region = warnung[0]['regionName']
                warnString = "\n" + region

                for i in range(0,w_count):
                    w_headline = warnung[i]['headline']
                    w_description = warnung[i]['description']

                    warnString += "\n" + w_headline + "\n" + w_description
                    if (i == (w_count-1)):
                        warnString += "\n"

            try:
                vorwarnung = data_u['vorabInformation']['105374000']
            except:
                pass
            else:
                v_count = len(vorwarnung)
                region = vorwarnung[0]['regionName']
                vWarnString = "\n" + region

                for i in range(0,v_count):
                    v_headline = vorwarnung[i]['headline']
                    v_description = vorwarnung[i]['description']

                    vWarnString += "\n" + v_headline + "\n" + v_description

            w_out.write(str(w_count) + warnString + str(v_count) + "\n" + vWarnString)
            w_out.close()

getWeather()
getUnweather()
