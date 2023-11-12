import json

class Restaurant:
    def __init__ (self, index, name, vegan, child, seats, schedule, scheduleD):
        self.index = index
        self.name = name
        self.vegan = vegan
        self.child = child
        self.seats = seats
        self.schedule = schedule
        self.scheduleD = scheduleD
        
    def print_r (self):
        with open('output.txt', 'a') as f:
            f.write ("The restaurnt is " + self.name)
            f.write ("\n")
            f.write ("THe restaurant is vegan? " + str(self.vegan))
            f.write ("\n")
            f.write ("THe restaurant is child friendly? " +  str(self.child))
            f.write ("\n")
            f.write ("The restaurant has " + str(self.seats) + " seats")
            f.write ("\n")
            f.write ("The restaurant has the following schedule ")
            f.write ("\n")
            for i in self.scheduleD:
                i.prtDay()
                
    def print_json (self):
        
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
                
    def avbl (self, day, H):
        if self.seats > 0:
            return self.scheduleD[day].fit(H)
    
    def nameN (self):
        return self.name