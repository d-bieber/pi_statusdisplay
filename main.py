#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2020 Dominik Bieber

import signal
import sys

import oled_control as oled #modified display driver
import time
import datetime

from luma.core.render import canvas
from luma.core.sprite_system import framerate_regulator

import timetable as ttb #public transport timetable
import os #system temperature and voltage
import urllib.request as url #Urlopen
import pihole #PiHole Status

INTERVALL = 10 #time in seconds between two screens
VERSION = '6.0'

degreeSymbol = '°C'

#TODO
# def sleep(sleepTime):
#     t = sleepTime*10
#     for i in range(0,time):
#         try:
#             time.sleep(0.1)
#         except:
#             pass

def umlaute(string):
    return oled.umlaute(string)

def start():
    device = oled.getDevice()

    font = oled.getFont()
    brands_font = oled.make_font("fa-brands.ttf", device.height - 30)
    icon = '\uf7bb'#raspberry-pi

    for i in range(33,138):#print fancy chars on startup
        oled.puts(chr(i))
        oled.flush()
        time.sleep(0.025)
    time.sleep(2)


    with canvas(device) as draw:
        w, h = draw.textsize(text=icon, font=brands_font)
        left = (device.width - w) / 2
        draw.text((left, 25), text=icon, font=brands_font)
        draw.text((0,0), text=oled.center('StatusPi'), font=font)
        draw.text((0,10), text=oled.center('Version ' + VERSION), font=font)

    time.sleep(5)

def getIcon(icon):#get weather icons
    iconList = {
        '01d': '\uf185','01n': '\uf186', #clear sky
        '02d': '\uf6c4','02n': '\uf6c3', #few clouds
        '03d': '\uf0c2','03n': '\uf0c2', #scattered clouds
        '04d': '\uf0c2','04n': '\uf0c2', #broken clouds
        '09d': '\uf740','09n': '\uf740', #shower rain
        '10d': '\uf743','10n': '\uf73c', #rain
        '11d': '\uf0e7','11n': '\uf0e7', #thunderstorm
        '13d': '\uf2dc','13n': '\uf2dc', #snow
        '50d': '\uf75f','50n': '\uf75f'  #mist
    }
    return iconList[icon]   

#Clock by luma.oled examples
def clock():
    print('Clock')

    today_last_time = "Unknown"
    device=oled.getDevice()
    count=0
    while (count<INTERVALL):
        now = datetime.datetime.now()
        today_date = now.strftime("%d %b %y")
        today_time = now.strftime("%H:%M:%S")
        if today_time != today_last_time:
            today_last_time = today_time
            with canvas(device) as draw:
                now = datetime.datetime.now()
                today_date = now.strftime("%d %b %y")

                margin = 4

                cx = 30
                cy = min(device.height, 64) / 2

                left = cx - cy
                right = cx + cy

                hrs_angle = 270 + (30 * (now.hour + (now.minute / 60.0)))
                hrs = oled.posn(hrs_angle, cy - margin - 7)

                min_angle = 270 + (6 * now.minute)
                mins = oled. posn(min_angle, cy - margin - 2)

                sec_angle = 270 + (6 * now.second)
                secs = oled. posn(sec_angle, cy - margin - 2)

                draw.ellipse((left + margin, margin, right - margin, min(device.height, 64) - margin), outline="white")
                draw.line((cx, cy, cx + hrs[0], cy + hrs[1]), fill="white")
                draw.line((cx, cy, cx + mins[0], cy + mins[1]), fill="white")
                draw.line((cx, cy, cx + secs[0], cy + secs[1]), fill="red")
                draw.ellipse((cx - 2, cy - 2, cx + 2, cy + 2), fill="white", outline="white")
                draw.text((2 * (cx + margin), cy - 8), today_date, fill="yellow")
                draw.text((2 * (cx + margin), cy), today_time, fill="yellow")

        time.sleep(0.1)
        count+=0.1


#Start Weather
def weather():
    MAX_LENGTH = oled.getWidth()
    device = oled.getDevice()

    regulator = framerate_regulator(fps=1)

    weather_font = oled.make_font("fa-solid.ttf", device.height - 40)
    font = oled.getFont()

    print('Weather')
    try:
        w_in = open("weather.wtd","r")
        
        #Wetter CITY1
        name1 = oled.center("CITY1")#CHANGE ME
        temp1 = w_in.readline().rstrip()
        condition1 = oled.center(umlaute(w_in.readline().rstrip()))
        icon1 = w_in.readline().rstrip()
        #Wetter CITY2
        name2 = oled.center("CITY2")#CHANGE ME
        temp2 = w_in.readline().rstrip()
        condition2 = oled.center(umlaute(w_in.readline().rstrip()))
        icon2 = w_in.readline().rstrip()
        w_in.close()

    except Exception as e:
        print(e)
        oled.scPrint("",oled.center("Wetter"),oled.center("Fehler"),"", oled.center(str(e)))
        time.sleep(INTERVALL)
    else:
        code1 = getIcon(icon1)
        code2 = getIcon(icon2)

        if not condition1:
            condition1 = oled.center("Fehler!")
            code1 = '\uf00d'
            
        if not condition2:
            condition2 = oled.center("Fehler!")
            code2 = '\uf00d'


        #WETTER1 - CITY1
        diff = (len(condition1)-MAX_LENGTH)*6

        if diff<=0:
            diff=1#Print strings that are <21 chars long
        a=0
        with regulator:
            for x in range(0,diff):
                with canvas(device) as draw:
                    w, h = draw.textsize(text=code1, font=weather_font)
                    left = (device.width - w) / 2
                    top = ((device.height - h) / 2)-5
                    draw.text((left, top), text=code1, font=weather_font)
                    draw.text((0,0), text=name1, font=font)
                    draw.text((a,43), text=condition1, font=font)
                    draw.text((0,53), text=oled.center(temp1+'°C'), font=font)

                if(x==0): #Don't scroll in the first seconds, for enough time to read
                    time.sleep(2)

                if(diff>0):
                    a-=1
                    diff-=1

        time.sleep(INTERVALL/2)


        #WETTER2 - CITY2
        diff = (len(condition2)-MAX_LENGTH)*6

        if diff<=0:
            diff=1#Print strings that are <21 chars long
        a=0
        with regulator:
            for x in range(0,diff):
                with canvas(device) as draw:
                    w, h = draw.textsize(text=code2, font=weather_font)
                    left = (device.width - w) / 2
                    top = ((device.height - h) / 2)-5
                    draw.text((left, top), text=code2, font=weather_font)
                    draw.text((0,0), text=name2, font=font)
                    draw.text((a,43), text=condition2, font=font)
                    draw.text((0,53), text=oled.center(temp2+'°C'), font=font)

                if(x==0): #Don't scroll in the first seconds, for enough time to read
                    time.sleep(2)

                if(diff>0):
                    a-=1
                    diff-=1

        time.sleep(INTERVALL/2)


def __old_weather():
    print('Weather')
    try:
        w_in = open("weather.wtd","r")
        
        #Wetter CITY1
        name1 = oled.center("CITY1")
        temp1 = w_in.readline().rstrip()
        condition1 = oled.center(umlaute(w_in.readline().rstrip()))
        #Wetter CITY2
        name2 = oled.center("CITY2")
        temp2 = w_in.readline().rstrip()
        condition2 = oled.center(umlaute(w_in.readline().rstrip()))
        w_in.close()
        if not condition1:
            condition1 = oled.center("Fehler!")
        if not condition2:
            condition2 = oled.center("Fehler!")

        oled.scPrint(oled.center("Wetter"), "", name1, condition1, oled.center(temp1 + degreeSymbol))
        time.sleep(INTERVALL/2)
        oled.scPrint(oled.center("Wetter"), "", name2, condition2, oled.center(temp2 + degreeSymbol))
        time.sleep(INTERVALL/2)
    except Exception as e:
        print(e)
        oled.scPrint("",oled.center("Wetter"),"",oled.center("Fehler"))
        time.sleep(INTERVALL)


#Start Storm
def storm():
    print('Storm')
    try:
        u_in = open("storm.wtd","r")
    except Exception as e:
        oled.oPrint("\n" + oled.center("Fehler Unwetter") + "\n" + str(e))
        u_in.close()
    else:


        #Amtliche Warnung
        try:
            w_count = u_in.readline().rstrip()
        except Exception as e:
            oled.oPrint("\n" + oled.center("Fehler Unwetter") + "\n" + oled.center(str(e)))
            time.sleep(INTERVALL)
        else:
            try:
                int(w_count)
            except:
                return
            if (str(w_count) == 'error'):
                oled.oPrint(oled.center("Unwetter") + "\n\n" + oled.center("Fehler beim Abrufen!"))
                time.sleep(INTERVALL/2)
                return 
            if int(w_count) > 0:
                try:
                    w_region = umlaute(u_in.readline().rstrip())
                    for i in range(0,int(w_count)):
                        w_headline = umlaute(u_in.readline().rstrip())
                        w_description = umlaute(u_in.readline().rstrip())
                        w_start = u_in.readline().rstrip()
                        w_end = u_in.readline().rstrip()
          
                        oled.oPrint(w_region + "\n\n" + w_headline + "\n" + w_description + "\n" + oled.concat('',w_start) + "\n" + oled.concat('(' + str(i+1) + "|" + w_count + ")",w_end))
                        time.sleep(INTERVALL/2)
                except Exception as e:
                    oled.oPrint("\n" + oled.center("Fehler Unwetter") + "\n" + oled.center(str(e)))

                    time.sleep(INTERVALL)



        #Vorwarnung
        try:
            v_count = u_in.readline().rstrip()
        except Exception as e:
            oled.oPrint("\n" + oled.center("Fehler Unwetter") + "\n" + oled.center(str(e)))
            time.sleep(INTERVALL)
        else:
            if int(v_count) > 0:
                try:
                    v_region = umlaute(u_in.readline().rstrip())
                    for i in range(0,int(v_count)):
                        v_headline = umlaute(u_in.readline().rstrip())
                        v_description = umlaute(u_in.readline().rstrip())
                        oled.oPrint(v_region + "\n\n" + v_headline + "\n" + v_description + "\n\n(" + str(i+1) + "|" + v_count + ")")
                        time.sleep(INTERVALL/2)
                except Exception as e:
                    oled.oPrint("\n" + oled.center("Fehler Unwetter") + "\n" + oled.center(str(e)))

                    time.sleep(INTERVALL)
           

#Start PiHole status
def piholeStatus():
    print('piHole Status')
    device = oled.getDevice()
    for i in range(0,INTERVALL):#refresh every second for INTERVALL times
        with canvas(device, dither=None) as draw:
            queries = pihole.getQueries()
            blocked = pihole.getBlocked()
            percentage = pihole.getPercentage()


            if pihole.getStatus():
                ph_status = "(Active)"
            else:
                ph_status = "(STOPPED)"
            if ((queries==-1) or (blocked==-1) or (percentage==-1)):
                oled.oPrint(oled.center("PiHole") + "\n\n" +
                    oled.center("Fehler"))
            else:
                fnt = oled.getFont()
                draw.text((0,0), font = fnt, text = oled.center("PiHole " + ph_status))

                draw.text((0,20), font = fnt, text = oled.concat("Queries:", queries))
                draw.text((0,30), font = fnt, text = oled.concat("Blocking:", blocked))
                draw.text((0,40), font = fnt, text = oled.concat("Percentage:", str(percentage) + "%"))

                pct_bar=127*(percentage/100)
                draw.rectangle((pct_bar, 63, 0, 50), fill="white")
                draw.rectangle((127, 63, 0, 50), outline="grey")

        time.sleep(1)


def __oldPiholeStatus():
    queries = pihole.getQueries()
    blocked = pihole.getBlocked()
    percentage = pihole.getPercentage()
    if pihole.getStatus():
        ph_status = "(Running)"
    else:
        ph_status = "(Stopped)"
    if ((queries==-1) or (blocked==-1) or (percentage==-1)):
        oled.oPrint(oled.center("PiHole " + chr(4)) + "\n\n" +
            oled.center("Fehler"))
    else:
        oled.oPrint(oled.center("PiHole " + ph_status) +"\n" +
            oled.concat("Queries: ", str(queries)) +"\n"+
            oled.concat("Blocked: ", str(blocked)) +"\n"+
            oled.concat("Percentage: ",  str(percentage) + "%"))
    time.sleep(INTERVALL)


#Start timetable
def timetable():
    print('Timetable')
    haltestelle = "Köln Hbf"
    try:
        fplan = fpl.getFahrplan()
    except Exception as e:
        oled.oPrint("\n" + oled.center("FEHLER (Fahrplan)") + "\n" + str(e))
        #print str(e)
        time.sleep(INTERVALL)
    else:
        if fplan:
            for i in range(0,len(fplan)):
                if ((fplan[i].dest == "") or (fplan[i].train == "")):#Fehlerhafte Daten nicht anzeigen
                    continue

                depart = fplan[i].timeDepart
                if(fplan[i].delay > 0):
                    depart = "(+" + str(fplan[i].delay) + ")" + fplan[i].timeDepart

                oled.scPrint(oled.concat(haltestelle,fplan[i].platform), 
                    "---------------------",
                    oled.concat(fplan[i].train, depart),
                    umlaute(fplan[i].via),
                    umlaute(fplan[i].dest),
                    umlaute(fplan[i].messages))
                time.sleep(INTERVALL/2)
        else:
            oled.scPrint(haltestelle, 
                "---------------------",
                "",
                oled.center("Keine Abfahrten"),oled.center("gefunden!"))
            time.sleep(INTERVALL/2)



#Start Raspberry Pi Status 
def pistatus():
    print('PiStatus')

    temp = os.popen('vcgencmd measure_temp').read()
    tempprint = temp[(temp.rfind("=")+1):]
    tempprint = tempprint[:4]
    
    try:
        ip = url.urlopen('https://api.ipify.org').read()
	#ip = "-"
    except:
        ip = "Offline"

    temp = os.popen('vcgencmd measure_volts').read()
    voltprint = temp[(temp.rfind("=")+1):]
    voltprint = voltprint[:7]
    oled.oPrint(oled.center("Pi Status") + "\n\n" + oled.concat("CPU-Temp: ", str(tempprint + '°C')) + "\n" + oled.concat("CPU-Volt: ", str(voltprint)) + "\n" + oled.concat("IP: ", str(ip.decode('utf-8'))))            
    time.sleep(INTERVALL)


def nightMode():
    device = oled.getDevice()
    font = oled.getFont()
    splash = 5

    while(1):
        now = datetime.datetime.now()
        now_time = now.strftime("%H:%M:%S")
        
        f = "%H:%M:%S"
        d_str = '04:00:00'
        thr_clock = datetime.datetime.strptime(d_str, f)        
        if now.time() > thr_clock.time():
            return

        with canvas(device) as draw:
            if(splash>0):
                draw.text((0,20), text=oled.center('Night Mode'), font=font, fill="white")
                splash-=1
            draw.text((40,53), text=now_time, font=font, fill="grey") 
        time.sleep(1)


def handler(signum, frame):
    oled.clear()
    sys.exit(0)

def crashWriter(funcName, e):
    crash = open("crash.log","a")
    now = datetime.datetime.now()
    date = now.strftime("%d %b %y")
    time = now.strftime("%H:%M:%S")
    crash.write('\n[' + funcName + ' - ' + date + ' ' + time + '] ' + str(e))
    print('\n[' + funcName + ' - ' + date + ' ' + time + '] ' + str(e))


#----------------------------------------------------------------------
signal.signal(signal.SIGHUP, handler)
signal.signal(signal.SIGTERM, handler)
start()
try:
    while (True):        
        nightMode()
        try:
            clock()
        except Exception as e:
            crashWriter("Clock",e)
        nightMode()
        try:
            weather()
        except Exception as e:
           crashWriter("Weather",e)
        nightMode()
        try:
            storm()
        except Exception as e:
            crashWriter("Storm",e)
        nightMode()
        try:        
            piholeStatus()
        except Exception as e:
            crashWriter("PiHole",e)
        nightMode()
        try:
           timetable()
        except Exception as e:
            crashWriter("Timetable",e)
        nightMode()
        try:
            pistatus()
        except Exception as e:
            crashWriter("PiStatus",e)
except KeyboardInterrupt:
    print("\nStopped by KeyboardInterrupt")
except Exception as e:
    crashWriter("Main",e)

