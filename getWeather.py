#!/usr/env python
# coding: utf-8

from __future__ import unicode_literals

import urllib.request as url
import time as time
import json
import ssl

import datetime

import configparser

cfg = configparser.ConfigParser()

def readConfig():
    try:
        cfg.read('config.ini')
    except Exception:
        print(e)
        return
    else:
        if not cfg.sections():
            return False
        return True
        
    

def getWeather(city1,city2,apikey):
    weather_url = 'https://api.openweathermap.org/data/2.5/group?id=' + city1 + ',' + city2 + '&lang=de&units=metric&appid=' + apikey

    for t in range(0,3):
        try:
            response = url.urlopen(weather_url)

            data = json.load(response)
        except Exception as e:
            condition1 = "Fehler"
            temp1 = "  -"
            icon1 = "  -"
            condition2 = "Fehler"
            temp2 = "  -"
            icon2 = "  -"
        else:
            e=""
            name1=data['list'][0]['name']
            temp1=data['list'][0]['main']['temp']
            icon1=data['list'][0]['weather'][0]['icon']

            cond_array = data['list'][0]['weather']
            condition1 = ""
            for i in range(0,len(cond_array)):
                condition1 += cond_array[i]['description'].title()
                if not (i == (len(cond_array)-1)):
                    condition1 += ", "


            name2=data['list'][1]['name']
            temp2=data['list'][1]['main']['temp']
            icon2=data['list'][1]['weather'][0]['icon']

            cond_array = data['list'][1]['weather']
            condition2 = ""
            for i in range(0,len(cond_array)):
                condition2 += cond_array[i]['description'].title()
                if not (i == (len(cond_array)-1)):
                    condition2 += ", "

            break

    lt = time.localtime()
    zeit = time.strftime("%H:%M",lt)
       
    w_out = open("weather.wtd","w")
    w_out.write(name1 + "\n" + str(temp1) + "\n" + condition1 + "\n" + icon1 + "\n" + name2 + "\n" + str(temp2) + "\n" + condition2 + "\n" + icon2 + "\n--------\n" + zeit + "\n" + "Try: " + str(t) + "\n" + str(e))
    w_out.close()


def getStorm(stormid):
    storm_url='https://www.dwd.de/DWD/warnungen/warnapp/json/warnings.json'

    w_out = open("storm.wtd","w")
    context = ssl._create_unverified_context()
    try:
        response = url.urlopen(storm_url, context=context)
    except:
        print('ERROR')
        w_out.write('error')
        w_out.close()
        return
    else:
        html = response.read()
        html = html[24:-2]#Fix to make valid JSON
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
                warnung = data_u['warnings'][stormid]
            except:
                pass
            else:
                w_count = len(warnung)
                region = warnung[0]['regionName']
                warnString = "\n" + region

                for i in range(0,w_count):
                    w_headline = warnung[i]['headline']
                    w_description = warnung[i]['description']
                    start = warnung[i]['start']/1000
                    end = warnung[i]['end']/1000

                    start = datetime.datetime.fromtimestamp(start).strftime('%d.%m %H:%M')
                    end = datetime.datetime.fromtimestamp(end).strftime('%d.%m %H:%M')

                    warnString += "\n" + w_headline + "\n" + w_description + "\n" + start + "\n" + end
                    if (i == (w_count-1)):
                        warnString += "\n"
                    warnString = warnString

            try:
                vorwarnung = data_u['vorabInformation'][stormid]
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
                    vWarnString = vWarnString
            w_out.write(str(w_count) + warnString + str(v_count) + "\n" + vWarnString)
            w_out.close()

if not (readConfig()):
    print('[getWeather] Could not read config!')
    exit()

try:
    weather = cfg['weather']
    city1 = weather['cityid1']
    city2 = weather['cityid2']
    apikey = weather['apikey']

    stormid = weather['stormid']
except Exception as e:
    print('[getWeather] Could not read config!')
    exit()
else:
    getWeather(city1,city2,apikey)
    getStorm(stormid)
