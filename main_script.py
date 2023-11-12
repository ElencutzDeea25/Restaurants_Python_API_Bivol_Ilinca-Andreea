# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 13:23:07 2023

@author: ilinc
"""
import Day
import Restaurant
import csv

import datetime



R = []
c = 0
cnt = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

  
def hour (AMPM, H):
    if (AMPM == "am"):
        return H
    else:
        if (":" in H):
            h, m = H.split(":")
            h = int(h)
            h = h + 12
            h = str(h) 
            H1 = h + ":" + m
            return H1
        else:
            h = int(H)
            h = h + 12
            H1 = str(h)
            return H1
        
def empty_week (schedule):
    schedule.append(Day.Day("Mon", "00:00", "00:00"))
    schedule.append(Day.Day("Tue", "00:00", "00:00"))
    schedule.append(Day.Day("Wed", "00:00", "00:00"))
    schedule.append(Day.Day("Thu", "00:00", "00:00"))
    schedule.append(Day.Day("Fri", "00:00", "00:00"))
    schedule.append(Day.Day("Sat", "00:00", "00:00"))
    schedule.append(Day.Day("Sun", "00:00", "00:00"))


def createJSON (csv_file):
    with open(csv_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)    
        header = next(csv_reader, None)
    
        for c, row in enumerate(csv_reader):
            name = str (row[0])
            vegan = 0 if row[1] == "no" else 1
            child = 0 if row[2] == "no" else 1
            seats = int(row[3])
            schedule = []
            empty_week(schedule)      
            
            intervals = row[4].split("  / ")
            
            for inte in intervals:
                           
                fra = inte.split(" ")
                more = False
    
                if "-" in fra[0]:
                    days = []
                    da = fra[0].split("-")
                    if "," in da[1] :
                        da[1] = da[1][:-1]
                        more = True
                    d1 = cnt.index(da[0])
                    d2 = cnt.index(da[1])
                    H1 = "00:00"
                    H2 = "00:00"
                    
                    for i in range(d1, d2 + 1):
                        H1 = hour(fra[-4], fra[-5])
                        H2 = hour(fra[-1], fra[-2])
                        schedule[i].setH(H1, H2)
    
                else:
                    if "," in fra[0] :
                        fra[0] = fra[0][:-1]
                        more = True
                    
                    i = cnt.index(fra[0])
                    H1 = hour(fra[-4], fra[-5])
                    H2 = hour(fra[-1], fra[-2])
                    schedule[i].setH(H1, H2)
    
                    
                if more == True:
                    if "-" in fra[1]:
                        days = []
                        da = fra[1].split("-")
                        if "," in da[1] :
                            da[1] = da[1][:-1]
                            more = True
                        d1 = cnt.index(da[0])
                        d2 = cnt.index(da[1])
                        H1 = "00:00"
                        H2 = "00:00"
                        
                        for i in range(d1, d2 + 1):                       
                            H1 = hour(fra[-4], fra[-5])
                            H2 = hour(fra[-1], fra[-2])
                            schedule[i].setH(H1, H2)
    
                            
                    else:
                        if "," in fra[1] :
                            fra[1] = fra[1][:-1]
                            more = True                    
                        i = cnt.index(fra[1])                    
                        H1 = hour(fra[-4], fra[-5])
                        H2 = hour(fra[-1], fra[-2])
                        schedule[i].setH(H1, H2)
            
            a = []
            for i in schedule:
                aa = i.getDays()
                a.append(aa)
            
            rrw = Restaurant.Restaurant(c, name, vegan, child, seats, a, schedule) 
            rrw.print_r()
            R.append(rrw)
            rrw.print_json()




    
def find_my_lunch(csv_file, x):
                       
    createJSON(csv_file)
    
    dayS = x.strftime("%w")
    dayS = int(dayS)
    dayS = dayS - 1 if dayS in range(1, 6) else 6
    print (dayS)
    hourS = x.strftime("%X")
    
    hourS = hourS[:-3]
    #print (hourS)
    #print (dayS, " ", hourS)
    for rr in R:
        if rr.avbl(dayS, hourS):
            print (rr.nameN())
            
       
def getR ():
    return R            
       
x = datetime.datetime.now()

file_path = "rest.json"
with open(file_path, 'w') as file:
    file.write ("[\n]")
    
find_my_lunch("restaurants.csv", x)  




        

