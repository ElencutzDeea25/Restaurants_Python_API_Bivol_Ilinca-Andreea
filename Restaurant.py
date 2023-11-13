import json

class Restaurant:
    def __init__ (self, index, name, vegan, child, seats, schedule, scheduleD):
        self.index = index #ID of restaurant
        self.name = name #Name of the restaurant
        self.vegan = vegan #Is it vegan or no
        self.child = child #Is it child friendly
        self.seats = seats #Number of seats
        self.schedule = schedule #schedule of restaurant in dict format
        self.scheduleD = scheduleD #schedule of restaurant in Day object format
                        
    def print_json (self): #writes the restaurant with all the values into a json format into a json file
        
        data = {
            "index": self.index,
            "name": self.name,
            "vegan": self.vegan,
            "child": self.child,
            "seats": self.seats,
            "schedule": [
                    self.schedule[0],
                    self.schedule[1],
                    self.schedule[2],
                    self.schedule[3],
                    self.schedule[4],
                    self.schedule[5],
                    self.schedule[6]
                ]
        }
        
        file_path = "rest.json"
        
        
        with open(file_path, 'r') as json_file:
            existing_data = json.load(json_file)
            
        existing_data.append(data)
        
        with open(file_path, 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)
                
    def avbl (self, day, H): #checks the availability for a given day of the week and hour
        if self.seats > 0:
            return self.scheduleD[day].fit(H)
    
    def nameN (self): #returns the name of the restaurant
        return self.name
    
    def indexN (self): #returns the index of the restaurant
        return self.index