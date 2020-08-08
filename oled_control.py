#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-17 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

from __future__ import unicode_literals

import os
import time
import math

from demo_opts import get_device
from luma.core.virtual import terminal #Aufbauender Text
from PIL import ImageFont

from luma.core.render import canvas

from luma.core.legacy import show_message #SCROLLENDER TEXT
from luma.core.legacy.font import proportional, SINCLAIR_FONT


from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.sprite_system import framerate_regulator

powerTwo = '²'
powerTwo = powerTwo[1:]#Bugfix um Â vor ² zu entfernen

# for fontname, size in [(None, None), ("tiny.ttf", 6), ("ProggyTiny.ttf", 16), ("creep.bdf", 16), ("miscfs_.ttf", 12), ("FreePixel.ttf", 12)]:
STANDARD_FONT = "ProggyTiny.ttf"
STANDARD_FONT_SIZE = 16

#SCROLLING_SPEED = 0.08
SCROLLING_SPEED = 0.04


def make_font(name, size):
    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'fonts', name))
    return ImageFont.truetype(font_path, size)

def println(msg):
    """
    Prints the supplied text to the device, scrolling where necessary.
    The text is always followed by a newline.
    :type text: str
    """
    term.println(msg)

def puts(msg):
    """
    Prints the supplied text, handling special character codes for carriage
    return (\\r), newline (\\n), backspace (\\b) and tab (\\t). ANSI color
    codes are also supported.
    If the ``animate`` flag was set to True (default), then each character
    is flushed to the device, giving the effect of 1970's teletype device.
    :type text: str
    """
    term.puts(msg)

def putch(char):
    """
    Prints the specific character, which must be a valid printable ASCII
    value in the range 32..127 only, or one of carriage return (\\r),
    newline (\\n), backspace (\\b) or tab (\\t).
    """
    term.putch(char)

def clear():
    """
    Clears the display and resets the cursor position to ``(0, 0)``.
    """
    term.clear()

def carriage_return():
    """
    Returns the cursor position to the left-hand side without advancing
    downwards.
    """
    term.carriage_return()

def tab():
    """
    Advances the cursor position to the next (soft) tabstop.
    """
    term.tab()

def newline():
    """
    Advances the cursor position ot the left hand side, and to the next
    line. If the cursor is on the lowest line, the displayed contents are
    scrolled, causing the top line to be lost.
    """
    term.newline()

def backspace():
    """
    Moves the cursor one place to the left, erasing the character at the
    current position. Cannot move beyond column zero, nor onto the
    previous line
    """
    term.backspace()

def erase():
    """
    Erase the contents of the cursor's current position without moving the
    cursor's position.
    """
    term.erase()

def flush():
    """
    Cause the current backing store to be rendered on the nominated device.
    """
    term.flush()


#OWN FUNCTIONS START
def getWidth():
    return term.width

def getHeight():
    return term.height

def center(string):
    """
    Centers String in line
    """
    if(len(string)>=(term.width-1)):
        return string
    diff = int((term.width-len(string))/2)
    leer = ""
    for i in range(0,diff):
        leer += " "
    string = leer + string
    return string

def half(left,right):
    width=getWidth()
    max_size = math.floor(width/2)


    l_left = len(left)
    l_right = len(right)

    d_left=max_size-l_left
    d_right = max_size-l_right

    string = ""

    for i in range(0,math.ceil((d_left/2))):
        string += " "

    string+=left

    for i in range(0,max_size-len(string)):
        string += " "


    string+=" " #Add one blank for center

    for i in range(0,math.ceil((d_right/2))):
        string += " "

    string+=right


    return string

def concat(string1, string2):
    """
    Concatenates two strings. First left-Aligned, second right-aligned
    """
    diff = term.width-(len(string1)+len(string2))
    if(len(string1)+len(string2) >= term.width):
        diff = 1
    leer = ""
    for i in range(0,diff):
        leer += " "
    return (string1 + leer + string2)


def umlaute(string):
    return string

    string = string.replace('InterCityExpress', '')
    string = string.replace('InterCity', '')
    string = string.replace('\\', ' ')
#    string = string.replace('°C'.encode('utf-8'), degreeSymbol)
    return string

#deprecated
def oPrint(msg):
    #msg = umlaute(msg)
    line1 = None
    line2 = None
    line3 = None
    line4 = None
    line5 = None
    line6 = None

    if "\n" in msg:
        line2 = msg[(msg.find("\n")+1):]
        line1 = msg[:(msg.find("\n"))]
        if "\n" in line2:
            line3 = line2[(line2.find("\n")+1):]
            line2 = line2[:(line2.find("\n"))]
            if "\n" in line3:
                line4 = line3[(line3.find("\n")+1):]
                line3 = line3[:(line3.find("\n"))]
                if "\n" in line4:
                    line5 = line4[(line4.find("\n")+1):]
                    line4 = line4[:(line4.find("\n"))]
                    if "\n" in line5:
                        line6 = line5[(line5.find("\n")+1):]
                        line5 = line5[:(line5.find("\n"))]
    else:
        line1 = msg
        line2 = None
        line3 = None
        line4 = None
        line5 = None
        line6 = None

    scPrint(line1,line2,line3,line4,line5,line6)

    # diff1 = len(line1)-term.width
    # diff2 = len(line2)-term.width
    # diff3 = len(line3)-term.width
    # diff4 = len(line4)-term.width
    # diff5 = len(line5)-term.width
    # diff6 = len(line6)-term.width

    # orig1 = line1
    # orig2 = line2
    # orig3 = line3
    # orig4 = line4
    # orig5 = line5
    # orig6 = line6

    # max_diff = max(diff1,diff2,diff3,diff4,diff5,diff6)


    # clear()
    # if(max_diff <= 0):
    #     puts(line1 + "\n" + line2 + "\n" + line3 + "\n" + line4 + "\n" + line5 + "\n" + line6)
    #     flush()
    #     time.sleep(0.8)
    # else:
    #     puts(line1[:term.width] + "\n" + line2[:term.width] + "\n" + line3[:term.width] + "\n" + line4[:term.width] + "\n" + line5[:term.width] + "\n" + line6[:term.width])
    #     flush()
    #     time.sleep(1.2)

    #     for i in range(0,max_diff):
    #         if(diff1 > 0):
    #             orig1 = orig1[1:]
    #             string1 = orig1[:term.width]
    #             setColumn(0)
    #             carriage_return()
    #             puts(string1)
    #             diff1 -= 1
    #         if(diff2 > 0):
    #             orig2 = orig2[1:]
    #             string2 = orig2[:term.width]
    #             setColumn(1)
    #             carriage_return()
    #             puts(string2)
    #             diff2 -= 1
    #         if(diff3 > 0):
    #             orig3 = orig3[1:]
    #             string3 = orig3[:term.width]
    #             setColumn(2)
    #             carriage_return()
    #             puts(string3)
    #             diff3 -= 1
    #         if(diff4 > 0):
    #             orig4 = orig4[1:]
    #             string4 = orig4[:term.width]
    #             setColumn(3)
    #             carriage_return()
    #             puts(string4)
    #             diff4 -= 1
    #         if(diff5 > 0):
    #             orig5 = orig5[1:]
    #             string5 = orig5[:term.width]
    #             setColumn(4)
    #             carriage_return()
    #             puts(string5)
    #             diff5 -= 1
    #         if(diff6 > 0):
    #             orig6 = orig6[1:]
    #             string6 = orig6[:term.width]
    #             setColumn(5)
    #             carriage_return()
    #             puts(string6)
    #             diff6 -= 1
    #         flush()
    #         time.sleep(SCROLLING_SPEED)


def scPrint(l1=None, l2=None, l3=None, l4=None, l5=None, l6=None):
    MAX_LENGTH = getWidth()

    regulator = framerate_regulator()

    if l1==None and l2==None and l3==None and l4==None and l5==None and l6==None:
        return

    line1=line2=line3=line4=line5=line6=""

    diff1=diff2=diff3=diff4=diff5=diff6=0

    a=b=c=d=e=f=0

    if(l1!=None):
        diff1 = (len(l1)-MAX_LENGTH)*6
        line1 = l1
    if(l2!=None):
        diff2 = (len(l2)-MAX_LENGTH)*6
        line2 = l2
    if(l3!=None):
        diff3 = (len(l3)-MAX_LENGTH)*6
        line3 = l3
    if(l4!=None):
        diff4 = (len(l4)-MAX_LENGTH)*6
        line4 = l4
    if(l5!=None):
        diff5 = (len(l5)-MAX_LENGTH)*6
        line5 = l5
    if(l6!=None):
        diff6 = (len(l6)-MAX_LENGTH)*6
        line6 = l6


    max_diff = max(diff1,diff2,diff3,diff4,diff5,diff6)


    if(max_diff <= 0):
            with canvas(device) as draw:
                draw.text((0,0), font=font, text = line1)
                draw.text((0,10), font=font, text = line2)
                draw.text((0,20), font=font, text = line3)
                draw.text((0,30), font=font, text = line4)
                draw.text((0,40), font=font, text = line5)
                draw.text((0,50), font=font, text = line6)
    else:

        distance= max_diff# + MAX_LENGTH*6
        with regulator:
            for x in range(0,distance):
                with canvas(device) as draw:
                    draw.text((a,0), font=font, text = line1)
                    draw.text((b,10), font=font, text = line2)
                    draw.text((c,20), font=font, text = line3)
                    draw.text((d,30), font=font, text = line4)
                    draw.text((e,40), font=font, text = line5)
                    draw.text((f,50), font=font, text = line6)

                if(x==0): #Don't scroll in the first seconds, for enough time to read
                    time.sleep(2)

                if(diff1>0):
                    a-=1
                    diff1-=1
                if(diff2>0):
                    b-=1
                    diff2-=1
                if(diff3>0):
                    c-=1
                    diff3-=1
                if(diff4>0):
                    d-=1
                    diff4-=1
                if(diff5>0):
                    e-=1
                    diff5-=1
                if(diff6>0):
                    f-=1
                    diff6-=1

def setColumn(c):
    if(c>5):
        c=5
    term._cy=c*term._ch

def posn(angle, arm_length):
    dx = int(math.cos(math.radians(angle)) * arm_length)
    dy = int(math.sin(math.radians(angle)) * arm_length)
    return (dx, dy)

def getDevice():
    return device

def getFont():
    return font


def textsize(txt, font=None):
    """
    Calculates the bounding box of the text, as drawn in the specified font.
    This method is most useful for when the
    :py:class:`~luma.core.legacy.font.proportional` wrapper is used.
    :param txt: the text string to calculate the bounds for
    :type txt: str
    :param font: the font (from :py:mod:`luma.core.legacy.font`) to use
    """
    font = font or DEFAULT_FONT
    src = [c for ascii_code in txt for c in font[ord(ascii_code)]]
    return (len(src), 8)


def text(draw, xy, txt, fill=None, font=None):
    """
    Draw a legacy font starting at :py:attr:`x`, :py:attr:`y` using the
    prescribed fill and font.
    :param draw: a valid canvas to draw the text onto.
    :type draw: PIL.ImageDraw
    :param txt: the text string to display (must be ASCII only)
    :type txt: str
    :param xy: an (x, y) tuple denoting the top-left corner to draw the text
    :type xy: tuple
    :param fill: the fill color to use (standard Pillow color name or RGB tuple)
    :param font: the font (from :py:mod:`luma.core.legacy.font`) to use
    """
    font = font or DEFAULT_FONT
    x, y = xy
    for ch in txt:
        for byte in font[ord(ch)]:
            for j in range(8):
                if byte & 0x01 > 0:
                    draw.point((x, y + j), fill=fill)

                byte >>= 1
            x += 1

def scroll_message(msg, y_offset=0, fill=None, scroll_delay=0.03):
    """
    Scrolls a message right-to-left across the devices display.
    :param device: the device to scroll across
    :param msg: the text message to display (must be ASCII only)
    :type msg: str
    :param y_offset: the row to use to display the text
    :type y_offset: int
    :param fill: the fill color to use (standard Pillow color name or RGB tuple)
    :param font: the font (from :py:mod:`luma.core.legacy.font`) to use
    :param scroll_delay: the number of seconds to delay between scrolling
    :type scroll_delay: float
    """

    device=getDevice()
    font=proportional(SINCLAIR_FONT)

    fps = 0 if scroll_delay == 0 else 1.0 / scroll_delay
    regulator = framerate_regulator(fps)
    #font = font or DEFAULT_FONT
    with canvas(device) as draw:
        w, h = textsize(msg, font)

    x = device.width
    virtual = viewport(device, width=w + x + x, height=(device.height/2))

    with canvas(virtual) as draw:
        text(draw, (x, y_offset), msg, font=font, fill=fill)

    
    
    time.sleep(3)

    i = 0
    while i <= w + x:
        with regulator:
            virtual.set_position((i, 0))
            i += 1



#OWN FUNCTIONS END

#----------------------------------------------------------

try:
    device = get_device()
except:
    print("[Error] Couldn't find device!")
else:
    font = make_font(STANDARD_FONT, STANDARD_FONT_SIZE)
    term = terminal(device, font, color="white", animate=False)
