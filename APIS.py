# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 15:36:46 2023

@author: ilinc
"""

from flask import Flask, request, jsonify
import json
import main_script
import Restaurant
import Day
import datetime
import re
import requests



app = Flask(__name__)
R = main_script.getR()

def scheduleDay (res):
    scheduleD = []
    main_script.empty_week (scheduleD)
    scheduleD[0].setH(res["schedule"][0]["Mon"]["Hstart"], res["schedule"][0]["Mon"]["Hstop"])
    scheduleD[1].setH(res["schedule"][1]["Tue"]["Hstart"], res["schedule"][1]["Tue"]["Hstop"])
    scheduleD[2].setH(res["schedule"][2]["Wed"]["Hstart"], res["schedule"][2]["Wed"]["Hstop"])
    scheduleD[3].setH(res["schedule"][3]["Thu"]["Hstart"], res["schedule"][3]["Thu"]["Hstop"])
    scheduleD[4].setH(res["schedule"][4]["Fri"]["Hstart"], res["schedule"][4]["Fri"]["Hstop"])
    scheduleD[5].setH(res["schedule"][5]["Sat"]["Hstart"], res["schedule"][5]["Sat"]["Hstop"])
    scheduleD[6].setH(res["schedule"][6]["Sun"]["Hstart"], res["schedule"][6]["Sun"]["Hstop"])
    return scheduleD
    
    rrw = Restaurant.Restaurant(len(restaurants), res["name"], res["vegan"], res["child"], res["child"], res["schedule"], scheduleD)
    return rrw

with open("rest.json", 'r') as json_file:
    restaurants = json.load(json_file)
json_file.close()

#get schedule of a specific restaurant
@app.route('/api/restaurant/<int:restaurant_id>/schedule', methods=['GET'])
def get_schedule(restaurant_id):
    restaurant = next((r for r in restaurants if r["index"] == restaurant_id), None)
    if restaurant:
        return jsonify({"schedule": restaurant["schedule"]})
    else:
        return jsonify({"message": "Restaurant not found"}), 404
    
#get list of restaurants opened at a specific time
@app.route('/api/restaurants/<day>/<hour>', methods=['GET'])
def get_restaurants_by_time(day, hour):
        
    if day == "Mon": dayS = 0
    elif day == "Tue": dayS = 1
    elif day == "Wed": dayS = 2
    elif day == "Thu": dayS = 3
    elif day == "Fri": dayS = 4
    elif day == "Sat": dayS = 5
    elif day == "Sun": dayS = 6
    else: return jsonify({"message": "Privide the day in standart 3 character format"}), 400

    matched = re.match("[0-9][0-9][:][0-9][0-9]", hour)
    if bool(matched):
        hourS = hour
        open_restaurants =[]
        for rr in R:
            if rr.avbl(dayS, hourS):
                open_restaurants.append(rr.nameN())            
        return jsonify({"open_restaurants": open_restaurants})
    else: return jsonify({"message": "Privide the hour in XX:XX format"}), 400

#add a new restaurant with custom schedule
@app.route('/api/restaurant', methods=['POST'])
def add_restaurant():
    dataNEW = request.files.get('data', '')
    dataNEW.save('dataNEW.json')
    with open('dataNEW.json', 'r') as json_file:
        file_content = json_file.read()
    res = json.loads(file_content)
    res["index"] = len(restaurants)
    restaurants.append(res)
    # print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # print (res["schedule"][1]['Tue']['Hstart'])
    rr = scheduleDay(res)
    rrw = Restaurant.Restaurant(res["index"], res["name"], res["vegan"], res["child"], res["seats"], res["schedule"], rr)
    R.append(rrw)
    
    with open("rest.json", 'w') as json_file:
            json.dump(restaurants, json_file, indent=4)
    json_file.close()
    return jsonify({"message": "Restaurant added successfully", "restaurant": res})

#update a restaurant details
@app.route('/api/restaurant/<int:restaurant_id>', methods=['PUT'])
def update_restaurant(restaurant_id):
    dataUPD = request.files.get('data', '')
    dataUPD.save('dataUPD.json')
    with open('dataUPD.json', 'r') as json_file:
        file_content = json_file.read()
    res = json.loads(file_content)
    restaurant = next((r for r in restaurants if r["index"] == restaurant_id), None)
    if restaurant: 
        res["index"] = restaurant_id
        with open('rest.json', 'r') as file:
            dt = json.load(file)
        file.close()
        
        del dt[restaurant_id]
        dt.append(res)
        
        with open('rest.json', 'w') as json_file:
            json.dump(dt, json_file, indent=4)
        file.close()
        
        rr = scheduleDay(res)
        rrw = Restaurant.Restaurant(res["index"], res["name"], res["vegan"], res["child"], res["seats"], res["schedule"], rr)
        R[restaurant_id] = rrw
        
        return jsonify({"message": "Restaurant updated successfully", "restaurant": restaurant})
        
    else:
        return jsonify({"message": "Restaurant not found"}), 404
 
#implement a reservation system using the api
@app.route('/api/reserve/<int:restaurant_id>/<day>/<hour>', methods=['POST'])
def make_reservation(restaurant_id, day, hour):

    res = next((r for r in restaurants if r["index"] == restaurant_id), None)
    if res in restaurants:
        opened = requests.get('http://127.0.0.1:5000//api/restaurants/'+ day + '/' + hour)
        if opened.status_code == 200:
            # Extract data from the JSON response
            json_data = opened.json()

            if res["name"] in json_data['open_restaurants']:
                
                res["seats"] = res["seats"] - 1
                
                with open('rest.json', 'r') as file: 
                    dt = json.load(file)
                file.close()
                
                del dt[restaurant_id]
                dt.append(res)
                
                with open('rest.json', 'w') as json_file:
                    json.dump(dt, json_file, indent=4)
                file.close()
                
                rr = scheduleDay(res)
                rrw = Restaurant.Restaurant(res["index"], res["name"], res["vegan"], res["child"], res["seats"], res["schedule"], rr)
                R[restaurant_id] = rrw
            
                return jsonify({"message": "Reservation made successfully", "seats_remain": res["seats"]})
    else:
        return jsonify({"message": "Invalid restaurant or time"}), 400

if __name__ == '__main__':
    
    app.run(debug=False)