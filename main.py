#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2018 Dominik Bieber

import signal
import sys

import oled_control as oled #Modifizierter Display-Treiber

import time
import datetime

from luma.core.render import canvas

import fahrplan as fpl #Fahrplan
import os #Für System Sensorik
import urllib2 as url #Urlopen
import pihole #PiHole Status

INTERVALL = 10
VERSION = '4.0'

degreeSymbol = '°C'
degreeSymbol = degreeSymbol[1:] #Bugfix um Â von ° zu entfernen


def umlaute(string):
    string = string.replace('ä', 'ae')
    string = string.replace('ö', 'oe')
    string = string.replace('ü', 'ue')
    string = string.replace('Ä', 'Ae')
    string = string.replace('Ö', 'Oe')
    string = string.replace('Ü', 'Ue')
    string = string.replace('ß', 'ss')
    string = string.replace('Ã¼', 'ue')
    string = string.replace('é', 'e')
    string = string.replace('è', 'e')
    string = string.replace('ê', 'e')
    string = string.replace('InterCityExpress', '')
    string = string.replace('InterCity', '')
    string = string.replace('GLAeTTE', 'GLAETTE')
    string = string.replace('\\', ' ')
    string = string.replace('°C', degreeSymbol)
    return string

def start():
    oled.println("".join(chr(i) for i in range(32, 127)))
    time.sleep(2)


    oled.clear()
    oled.println(oled.center("StatusPi"))
    oled.println(oled.center("Version: " + VERSION + "\n"))
    oled.println(oled.center("Starting..."))
    for mill in range(0, 10001, 25):
        oled.puts(oled.center("\rPercent: {0:0.1f} %").format(mill / 100.0))
        oled.flush()
    time.sleep(2)

#Clock by luma.oled examples
def clock():
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


#Wetter
def weather():
    try:
        w_in = open("weather.wtd","r")
        
        #Wetter 1
        name1 = oled.center("")
        temp1 = w_in.readline().rstrip()
        condition1 = oled.center(umlaute(w_in.readline().rstrip()))
        #Wetter 2
        name2 = oled.center("")
        temp2 = w_in.readline().rstrip()
        condition2 = oled.center(umlaute(w_in.readline().rstrip()))
        w_in.close()
        if not condition1:
            condition1 = oled.center("Fehler!")
        if not condition2:
            condition2 = oled.center("Fehler!")

        oled.oPrint(oled.center("Wetter") + "\n\n" + name1 + "\n" + condition1 + "\n" + oled.center(temp1 + degreeSymbol))
        time.sleep(INTERVALL/2)
        oled.oPrint(oled.center("Wetter") + "\n\n" + name2 + "\n" + condition2 + "\n" + oled.center(temp2 + degreeSymbol))
        time.sleep(INTERVALL/2)
    except Exception as e:
        print(e)
        oled.oPrint("\n" + oled.center("Wetter") + "\n" + oled.center("Fehler"))
        time.sleep(INTERVALL)


#Unwetter
def storm():
    try:
        u_in = open("storm.wtd","r")
    except:
        oled.oPrint("\n" + oled.center("Fehler Unwetter") + "\n" + oled.center("O"))
        w_in.close()
    else:


        #Amtliche Warnung
        try:
            w_count = u_in.readline().rstrip()
        except Exception as e:
            oled.oPrint("\n" + oled.center("Fehler Unwetter") + "\n" + oled.center(str(e)))
            time.sleep(INTERVALL)
        else:          
            if w_count > 0:
                try:
                    w_region = umlaute(u_in.readline().rstrip())
                    for i in range(0,int(w_count)):
                        w_headline = umlaute(u_in.readline().rstrip())
                        w_description = umlaute(u_in.readline().rstrip())
                        oled.oPrint(w_region + "\n\n" + w_headline + "\n" + w_description + "\n\n(" + str(i+1) + "|" + w_count + ")")
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
            if v_count > 0:
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
           

#PiHole Status
def piholeStatus():
    device = oled.getDevice()
    with canvas(device, dither=None) as draw:
        queries = pihole.getQueries()
        blocked = pihole.getBlocked()
        percentage = pihole.getPercentage()


        if pihole.getStatus():
            ph_status = "(Running)"
        else:
            ph_status = "(Stopped)"
        if ((queries==-1) or (blocked==-1) or (percentage==-1)):
            oled.oPrint(oled.center("PiHole") + "\n\n" +
                oled.center("Fehler"))
        else:
            fnt = oled.getFont()
            draw.text((0,0), font = fnt, text = oled.center("PiHole " + ph_status))

            draw.text((0,20), font = fnt, text = oled.concat("Queries:", queries))
            draw.text((0,30), font = fnt, text = oled.concat("Blocking:", blocked))
            draw.text((0,40), font = fnt, text = oled.concat("Percent:", str(percentage) + "%"))

            pct_bar=127*(percentage/100)
            draw.rectangle((pct_bar, 63, 0, 50), fill="white")
            draw.rectangle((127, 63, 0, 50), outline="grey")

    time.sleep(INTERVALL)


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


#Fahrplan Auskunft
def timetable():
    haltestelle = "Koeln Hbf"
    try:
        fplan = fpl.getFahrplan()
    except Exception as e:
        oled.oPrint("\n" + oled.center("FEHLER (Fahrplan)") + "\n" + str(e))
        time.sleep(INTERVALL)
    else:
        if fplan:
            for i in range(0,len(fplan)):
                if ((fplan[i].dest == "") or (fplan[i].train == "")):#Fehlerhafte Daten nicht anzeigen
                    continue

                depart = fplan[i].timeDepart
                if(fplan[i].delay > 0):
                    depart = "(+" + str(fplan[i].delay) + ")" + fplan[i].timeDepart
                oled.oPrint(oled.concat(haltestelle,fplan[i].platform) + 
                    "\n---------------------\n" +
                    oled.concat(fplan[i].train, depart) + "\n" + 
                    fplan[i].via +"\n" + 
                    fplan[i].dest + "\n" + 
                    fplan[i].messages)
                time.sleep(INTERVALL/2)
        else:
            oled.oPrint(haltestelle + 
                "\n---------------------\n\n" +
                oled.center("Keine Abfahrten") + "\n" + oled.center("gefunden!"))
            time.sleep(INTERVALL/2)



#Raspberry Pi Status 
def pistatus():
    temp = os.popen('vcgencmd measure_temp').read()
    tempprint = temp[(temp.rfind("=")+1):]
    tempprint = tempprint[:4]

    try:
        ip = url.urlopen('http://api.ipify.org').read()
    except:
        ip = "Offline"

    temp = os.popen('vcgencmd measure_volts').read()
    voltprint = temp[(temp.rfind("=")+1):]
    voltprint = voltprint[:7]
    oled.oPrint(oled.center("Pi Status") + "\n\n" + oled.concat("CPU-Temp: ", str(tempprint + degreeSymbol)) + "\n" + oled.concat("CPU-Volt: ", str(voltprint)) + "\n" + oled.concat("IP: ", str(ip)))            
    time.sleep(INTERVALL)


def handler(signum, frame):
    oled.clear()
    sys.exit(0)


#----------------------------------------------------------------------
signal.signal(signal.SIGHUP, handler)
start()
try:
    while (True):
        clock()
        weather()
        storm()
        piholeStatus()
        timetable()
        pistatus()
except KeyboardInterrupt:
    print("\nStopped by KeyboardInterrupt")
