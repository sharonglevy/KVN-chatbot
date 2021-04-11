# -*- coding: utf-8 -*-
"""

Created on Mon Aug  5 14:14:35 2019

"""

#time thingies

import datetime
from datetime import (date, timedelta)
import time

def is_ini_valid(text, fecha):
    print("is_ini_valid")
    today = date.today()
    today = today.strftime("%m/%d/%Y")
    print(fecha)
    print(today)

    now = datetime.datetime.now()
    hh,mm = text.split(":")
    in_time =now.replace(hour=int(hh), minute=int(mm))

    fecha2 = fecha.split("/")
    today2 = today.split("/")

    if fecha2[2] > today2[2]:
        return True

    if (fecha == today):
        if (in_time > now):
            return True
        else:
            return False

    elif (fecha > today):
        print("es menor")
        return True



def is_date_valid(text):
    today = date.today()
    try:
        mm,dd,aaaa = text.split("/")
        in_time = datetime.datetime(int(aaaa),int(mm),int(dd)).date()
        if in_time < today:
            return False
        else:
            return True
    except ValueError:
        return False
    
    
def isTimeFormat(input):
    try:
        time.strptime(input, '%H:%M')
        return True
    except ValueError:
        return False


def isDateFormat(text):
    try:
        datetime.datetime.strptime(text,"%m/%d/%Y")
        return True
    except ValueError:
        return False
    
    
def get_today():
    today = date.today()
    return today


def get_tomorrow():
    today = date.today()
    tmrw = today + timedelta(days=1)
    return tmrw




def is_end_valid(end,ini):
    in_time = datetime.datetime.strptime(ini, '%H:%M')
    print(in_time)
    nd_time = datetime.datetime.strptime(end, '%H:%M')
    print(nd_time)    
    if in_time < nd_time:
        return True
    else:
        return False
    
    
def to_date(text):
    try:
        mm,dd,aaaa = text.split("/")
        out_time = datetime.datetime(int(aaaa),int(mm),int(dd)).date()
        return out_time
    except ValueError as err:
        print(err)