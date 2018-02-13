#!/usr/env python
# coding: utf-8

import urllib2 as url
import json

import sys
reload(sys)
sys.setdefaultencoding('utf-8')




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
    return string

def getFahrplan():
    class Plan():
        def __init__(self, train,platform,dest,timeDepart,delay,messages,viaText):
            self.train = train
            self.platform = platform
            self.dest = dest
            self.timeDepart = timeDepart
            self.delay = delay
            self.messages = messages
            self.via = viaText



    plan0 = None
    plan1 = None
    plan2 = None

    try:
        response = url.urlopen('https://dbf.finalrewind.org/Köln%20Hbf?mode=marudor&version=3')

        data = json.load(response)

    except Exception as e:
        print(e)

    else:
        for x in range(0,3):
            try:
                errorData = data['error']#Fehler-Behandlung API
            except:
                pass
            else:
                error = Plan("ERROR","N/A","API-ERROR:","0",0,"++ " + errorData + " ++ ","")
                return error,

            try:
                fData = data['departures'][x]
            except:
                continue

            train = fData['train']
            platform = fData['platform']
            dest = fData['destination']
            timeDepart = fData['scheduledDeparture']
            delay = fData['delayDeparture']
            if not timeDepart:
                timeDepart = fData['scheduledArrival']
                delay = fData['delayArrival']


            if not platform:
                platform = ""

            if not timeDepart:
                timeDepart = "N/A"
                delay = 0

            if not dest:
                dest = ""
            dest = dest.encode('utf-8')

            if not train:
                train = ""

            

            via = fData['via']

            viaText = ""
            if via:
                viaText = "via: "
                for i in range(0, len(via)):
                    viaText += via[i].encode('utf-8')
                    if not (i==(len(via)-1)):
                        viaText += " - "

            if (fData['isCancelled'] == 1):
                cancelled = True
            else:
                cancelled = False
            messages = "++ "

            if cancelled:
                messages = "++ Fahrt faellt aus: "

            delayMessages = fData['messages']['delay']
            if delayMessages:
                for i in range(0,len(delayMessages)):
                    messages += delayMessages[i]['text'].encode('utf-8') + " ++ "

            qosMessages = fData['messages']['qos']
            if qosMessages:
                for i in range(0,len(qosMessages)):
                    messages += qosMessages[i]['text'].encode('utf-8') + " ++ "

            if (messages == "++ "):
                messages = ""
            else:
                messages = messages[:len(messages)-1]

            if(x==0):
                plan0 = Plan(train,platform,umlaute(dest),timeDepart,delay,umlaute(messages),umlaute(viaText))
            if(x==1):
                plan1 = Plan(train,platform,umlaute(dest),timeDepart,delay,umlaute(messages),umlaute(viaText))
            if(x==2):
                plan2 = Plan(train,platform,umlaute(dest),timeDepart,delay,umlaute(messages),umlaute(viaText))

            # print train
            # print platform
            # print dest
            # print timeDepart
            # print delay
            # print messages
            # print viaText
            # print cancelled
            # print '-----------------------'



        if not plan0:
            return None
        if not plan1:
            return plan0,
        if not plan2:
            return plan0, plan1

        return plan0, plan1, plan2 
    


