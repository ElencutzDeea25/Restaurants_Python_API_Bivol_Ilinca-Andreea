class Day:
    def __init__ (self, dow, Hstart, Hstop):
        self.dow = dow #Day of the week
        self.Hstart = Hstart #Starting hour 
        self.Hstop = Hstop #Closing hour
        
    def fit (self, H): #Checks if in the object's day, the given hour is part of the schedule
        if str_hour(self.Hstart) < str_hour(self.Hstop) :
            if (str_hour(self.Hstart) <= str_hour(H) and str_hour(H) <= str_hour(self.Hstop)):
                return True
            else: return False
        else:
            if (str_hour(self.Hstart) <= str_hour(H) and str_hour(H) <= 24) or (str_hour(self.Hstop) >= str_hour(H) and str_hour(H) >= 0):
                return True
            else: return False
        
    def setH (self, H1, H2): #resets the hours with new values
        self.Hstart = H1
        self.Hstop = H2
                
    def getDays (self): #transforms the day - hours values into dictionary format 
        
        dayOftheweek = {
            self.dow:{
                "Hstart" : self.Hstart,
                "Hstop": self.Hstop
            }
        }

        return dayOftheweek
            
def str_hour (H): #transforms the string into a float hur format
    if ":" in H:
        h, m = H.split(":")
        return float(h) + float(m) / 60
    else:
        return float(H)