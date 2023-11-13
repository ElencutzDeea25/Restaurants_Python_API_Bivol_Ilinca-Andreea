# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 13:23:07 2023

@author: ilinc
"""
import Day
import Restaurant
import csv
import datetime

#Given the attached CSV file, design a function find_my_lunch(csv_file, open_datetime) which takes as
#parameters a filename and a Python/Ruby/Go datetime object and returns a list of restaurant names which
#are open on that date and time. 

R = [] #vector for the restaurants objects
c = 0 #counter
cnt = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'] #days of the week in proper format

  
def hour (AMPM, H): #transforms from XX:XX AM / PM format into 24 hour format
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
        
def empty_week (schedule): #intitialize a vector od Day object with no schedule
    schedule.append(Day.Day("Mon", "00:00", "00:00"))
    schedule.append(Day.Day("Tue", "00:00", "00:00"))
    schedule.append(Day.Day("Wed", "00:00", "00:00"))
    schedule.append(Day.Day("Thu", "00:00", "00:00"))
    schedule.append(Day.Day("Fri", "00:00", "00:00"))
    schedule.append(Day.Day("Sat", "00:00", "00:00"))
    schedule.append(Day.Day("Sun", "00:00", "00:00"))


def createJSON (csv_file): #creates the JSON file
    
    file_path = "rest.json"
    with open(file_path, 'w') as file:
        file.write ("[\n]")

    with open(csv_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)    
        header = next(csv_reader, None)
    
        for c, row in enumerate(csv_reader): #for each row - creates the Restaurant object and extracts schedule
            name = str (row[0])
            vegan = 0 if row[1] == "no" else 1
            child = 0 if row[2] == "no" else 1
            seats = int(row[3])
            schedule = []
            empty_week(schedule)      
            
            intervals = row[4].split("  / ") #splits the time intervals in the string
            
            for inte in intervals:
                           
                fra = inte.split(" ") #splits the data by day(s), start hour, AM/PM, stop hour, AM/PM
                more = False #more than one day(s) intervals flag
    
                if "-" in fra[0]: #scenario for day interval (Mon-Thu)
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
    
                else: #scenario for single day
                    if "," in fra[0] :
                        fra[0] = fra[0][:-1]
                        more = True
                    
                    i = cnt.index(fra[0])
                    H1 = hour(fra[-4], fra[-5])
                    H2 = hour(fra[-1], fra[-2])
                    schedule[i].setH(H1, H2)
    
                    
                if more == True: #if there are more subintervals eg. Mon, Tue-Fri, repeats the analize for second interval
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
            
            a = [] #creates the vector in right format with each day's schedule
            for i in schedule:
                aa = i.getDays()
                a.append(aa)
            
            rrw = Restaurant.Restaurant(c, name, vegan, child, seats, a, schedule) #creates the Restaurant object for this row
            R.append(rrw) #apends it to the vector
            rrw.print_json() #appends it into the JSON file




    
def find_my_lunch(csv_file, x):
                       
    createJSON(csv_file)
    
    dayS = x.strftime("%w") #extract the number of the day and convers it to Mon = 0 -> Sun = 6
    dayS = int(dayS)
    dayS = dayS - 1 if dayS in range(1, 6) else 6
    hourS = x.strftime("%X") #estracts the hour
    openedNow = []
    hourS = hourS[:-3]
    for rr in R:
        if rr.avbl(dayS, hourS):
            openedNow.append(rr.nameN())
    return openedNow
            
       
def getR (): #returns the Restaurants vector
    return R            


def local_find():

    x = datetime.datetime.now()
    find_my_lunch("restaurants.csv", x)  


local_find()

        

