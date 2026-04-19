from miscellaneous import *
import datetime

'''
This code was written by Valerio Accardo, 
all rights on the shit that will be monitored 
belong to him and him alone
'''
class Shit():

    def __init__(self,datetime:str, shitter:str):
        self.datetime = datetime.replace(",","").strip()  # format "day/month/year hh/mm"
        self.shitter = shitter
        self.dt_obj = string2DateTime(self.datetime)

    def getShitter(self):
        return self.shitter

    def getDateTime(self, string = True):
        if string == True:
            return self.dt_obj.strftime("%d/%m/%y %H:%M")
        else:
            return self.dt_obj
    
    def getDate(self): #18/01/24
        return self.dt_obj.strftime("%d/%m/%y")
    
    def getHour(self, nozero = True):#18 str
        hour = self.dt_obj.hour
        if hour == 0:
            return "24"
        elif nozero == True:
            return str(hour)
        else:
            return self.dt_obj.strftime("%H")
    
    def getMonth(self, nozero = True):#18 str
        month = self.dt_obj.month
        if nozero == True:
            return str(month)
        else:
            return self.dt_obj.strftime("%m")
    
    def getTime(self): #07:32
        return self.dt_obj.strftime("%H:%M")
        
if __name__ =="__main__":
    shit = Shit(shitter = "Gianni", datetime = "18/01/24, 07:32")
    # print(shit.getDate())
    # print(shit.getTime())
    # print(shit.getDateTime())
    print(shit.getDate()[3:5])