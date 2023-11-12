# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 11:19:28 2023

@author: ilinc
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"

# Sample data (replace with a database in a real-world application)
restaurants = [
    {
        "id": 1,
        "name": "Restaurant A",
        "schedule": {
            "Mon": "10 am - 8 pm",
            "Tue": "10 am - 8 pm",
            # ... other days ...
        }
    },
    {
        "id": 2,
        "name": "Restaurant B",
        "schedule": {
            "Mon": "9 am - 9 pm",
            "Tue": "9 am - 9 pm",
            # ... other days ...
        }
    }
]

# Get schedule of a specific restaurant
@app.route('/api/restaurant/<int:restaurant_id>/schedule', methods=['GET'])
def get_schedule(restaurant_id):
    restaurant = next((r for r in restaurants if r["id"] == restaurant_id), None)
    if restaurant:
        return jsonify({"schedule": restaurant["schedule"]})
    else:
        return jsonify({"message": "Restaurant not found"}), 404

# Get list of restaurants opened at a specific time
@app.route('/api/restaurants', methods=['GET'])
def get_restaurants_by_time():
    target_time = request.args.get('time')
    if not target_time:
        return jsonify({"message": "Time parameter is required"}), 400

    open_restaurants = [r["name"] for r in restaurants if target_time in r["schedule"].values()]
    return jsonify({"open_restaurants": open_restaurants})

# Add a new restaurant with custom schedule
@app.route('/api/restaurant', methods=['POST'])
def add_restaurant():
    data = request.get_json()
    new_restaurant = {
        "id": len(restaurants) + 1,
        "name": data["name"],
        "schedule": data["schedule"]
    }
    restaurants.append(new_restaurant)
    return jsonify({"message": "Restaurant added successfully", "restaurant": new_restaurant})

# Update a restaurant details
@app.route('/api/restaurant/<int:restaurant_id>', methods=['PUT'])
def update_restaurant(restaurant_id):
    data = request.get_json()
    restaurant = next((r for r in restaurants if r["id"] == restaurant_id), None)
    if restaurant:
        restaurant["name"] = data["name"]
        restaurant["schedule"] = data["schedule"]
        return jsonify({"message": "Restaurant updated successfully", "restaurant": restaurant})
    else:
        return jsonify({"message": "Restaurant not found"}), 404

# Implement a reservation system using the API (example)
@app.route('/api/reserve', methods=['POST'])
def make_reservation():
    data = request.get_json()
    restaurant_id = data["restaurant_id"]
    time = data["time"]

    restaurant = next((r for r in restaurants if r["id"] == restaurant_id), None)
    if restaurant and time in restaurant["schedule"].values():
        # Implement your reservation logic here
        return jsonify({"message": "Reservation made successfully"})
    else:
        return jsonify({"message": "Invalid restaurant or time"}), 400

if __name__ == '__main__':
    app.run(debug=False)
