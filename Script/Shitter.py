from datetime import datetime
import numpy as np
import matplotlib as plt
from miscellaneous import merge_dictionaries
from Shit import Shit

class Shitter():

    def __init__(self,name:str,shits:list[Shit]):
        self.name = name
        self.shits = sorted(shits, key=lambda x: x.getDateTime(string=False))

    def getName(self):
        return self.name

    '''
This code was written by Valerio Accardo, 
all rights on the shit that will be monitored 
belong to him and him alone
'''
    def getShits(self):
        return self.shits
    
    def getShitsNumber(self):
        return len(self.shits)