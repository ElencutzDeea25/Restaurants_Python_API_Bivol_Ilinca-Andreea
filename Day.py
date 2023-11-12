class Day:
    def __init__ (self, dow, Hstart, Hstop):
        self.dow = dow
        self.Hstart = Hstart
        self.Hstop = Hstop
        
    def fit (self, H):
        if str_hour(self.Hstart) < str_hour(self.Hstop) :
            if (str_hour(self.Hstart) <= str_hour(H) and str_hour(H) <= str_hour(self.Hstop)):
                return True
            else: return False
        else:
            if (str_hour(self.Hstart) <= str_hour(H) and str_hour(H) <= 24) or (str_hour(self.Hstop) >= str_hour(H) and str_hour(H) >= 0):
                return True
            else: return False
        
    def setH (self, H1, H2):
        self.Hstart = H1
        self.Hstop = H2
    
    def prtDay (self):
        with open('output.txt', 'a') as f:
            f.write ("For " + self.dow + " Hours " + self.Hstart + " - " + self.Hstop)
            f.write ("\n")
            
    def getDays (self):
        
        dayOftheweek = {
            self.dow:{
                "Hstart" : self.Hstart,
                "Hstop": self.Hstop
            }
        }

        return dayOftheweek
            
def str_hour (H):
    if ":" in H:
        h, m = H.split(":")
        return float(h) + float(m) / 60
    else:
        return float(H)