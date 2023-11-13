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
import re
import requests

#### NOTES, README #####

# Based on the work above, design and write a RESTful API for:
# • get schedule of a specific restaurant
# • get list of restaurants opened at a specific time
# • add a new restaurant with custom schedule
# • update a restaurant details
# • implement a reservation system using the api

#### Please note that the API's were tested with POSTMAN tool
#### Limitations:
    ### seats are decreased as assumed on a day by day basis, the algorithm is hypothetically, demonstrative
    ### the need for R vector in order to check availability but increases performance as no need to re-read the JSON file and extracts data
    ### the update API updates on a JSON file basis in order to keep simplicity in the URL, 
        ### alternatively it can be done trough parameters for specific attribute of a restaurant
        

#initializaion
app = Flask(__name__)
main_script.createJSON("restaurants.csv") #creates the JSON file with CSV data
R = main_script.getR() #creates the Restaurant vector

def get_restaurants(): #updates the restaurants with new JSON data
    with open("rest.json", 'r') as json_file:
        restaurants = json.load(json_file)
    json_file.close()
    return restaurants

def scheduleDay (res): #creates the Day object vector in order modify a Restaurant object and returns it
    restaurants = get_restaurants()
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



#get index mapping of resturants names
@app.route('/api/restaurant/index', methods=['GET'])
def get_index():
    indexes =  []
    restaurants = get_restaurants()
    for r in restaurants:
        indexes.append((r["name"], r["index"]))
    return jsonify({"Mapping": indexes})

#get schedule of a specific restaurant
@app.route('/api/restaurant/<int:restaurant_id>/schedule', methods=['GET'])
def get_schedule(restaurant_id):
    restaurants = get_restaurants()
    restaurant = next((r for r in restaurants if r["index"] == restaurant_id), None)
    if restaurant:
        return jsonify({"schedule": restaurant["schedule"]})
    else:
        return jsonify({"message": "Restaurant not found"}), 404
    
#get list of restaurants opened at a specific time
@app.route('/api/restaurants/<day>/<hour>', methods=['GET'])
def get_restaurants_by_time(day, hour):
    #checks for Day and Hour format provided    
    if day == "Mon": dayS = 0
    elif day == "Tue": dayS = 1
    elif day == "Wed": dayS = 2
    elif day == "Thu": dayS = 3
    elif day == "Fri": dayS = 4
    elif day == "Sat": dayS = 5
    elif day == "Sun": dayS = 6
    else: return jsonify({"message": "Privide the day in standart 3 character format"}), 400

    matched = re.match("[0-9][0-9][:][0-9][0-9]", hour)
    #if the Day format and hour matches, start searching
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
    restaurants = get_restaurants()
    dataNEW = request.files.get('data', '') #imports the JSON provided into API to a local file
    dataNEW.save('dataNEW.json')
    with open('dataNEW.json', 'r') as json_file:
        file_content = json_file.read()
    res = json.loads(file_content)
    res["index"] = len(restaurants)
    restaurants.append(res)
    #adds the new restaurant to R vector
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
    restaurants = get_restaurants()
    dataUPD = request.files.get('data', '')  #imports the JSON provided into API to a local file
    dataUPD.save('dataUPD.json')
    with open('dataUPD.json', 'r') as json_file:
        file_content = json_file.read()
    res = json.loads(file_content)
    #finds the restaurant and updates it
    restaurant = next((r for r in restaurants if r["index"] == restaurant_id), None)
    if restaurant: 
        #updates new dict with the old index
        res["index"] = restaurant_id
        #loads the json data, deletes the old record, replaces it with new
        with open('rest.json', 'r') as file:
            dt = json.load(file)
        file.close()
        
        del dt[restaurant_id]
        dt.append(res)
        
        with open('rest.json', 'w') as json_file:
            json.dump(dt, json_file, indent=4)
        file.close()
        
        #replaces the restaurant in R vector with new data
        rr = scheduleDay(res)
        rrw = Restaurant.Restaurant(res["index"], res["name"], res["vegan"], res["child"], res["seats"], res["schedule"], rr)
        R[restaurant_id] = rrw
        
        return jsonify({"message": "Restaurant updated successfully", "restaurant": res})
        
    else:
        return jsonify({"message": "Restaurant not found"}), 404
 
#implement a reservation system using the api
@app.route('/api/reserve/<int:restaurant_id>/<day>/<hour>/<vegan>/<child>', methods=['PUT'])
def make_reservation(restaurant_id, day, hour, vegan, child):
    restaurants = get_restaurants()
    res = next((r for r in restaurants if r["index"] == restaurant_id), None)
    
    if res in restaurants:
        #checks if the restaurant is available at that hour
        opened = requests.get('http://127.0.0.1:5000//api/restaurants/'+ day + '/' + hour)
        if opened.status_code == 200:
            json_data = opened.json()
            if res["name"] in json_data['open_restaurants']:
                #checks if the vegan / child friendly criterias are matched (if not rquested, it does not matters)
                if (vegan == "no" or vegan == "yes") and (child == "yes" or child == "no"): #checks the format
                
                    vegan = 0 if vegan == "no" else 1
                    child = 0 if child == "no" else 1

                    if ((vegan == 1 and res["vegan"] == 1) or vegan == 0) or ((child == 1 and res["child"] == 1) or child == 0):
                        #hypothetically decreases  the number of seats and updates the data in JSON and R vector
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
                    else: return jsonify({"message": "The restaurant you choose does not meet you criterias"}), 400
                 
                    return jsonify({"message": "Reservation made successfully", "seats_remain": res["seats"]})
                
            else: jsonify({"message": "Provide the format: <restauratn_id>/<day in 3 letter format eg. Mon>/<yes_or_no_for_vegan>/<yes or no for child frendly>"}), 400
    else:
        return jsonify({"message": "Invalid restaurant or time"}), 400

if __name__ == '__main__':
    
    app.run(debug=False)
    
    
    
    
    

