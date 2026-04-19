from Shitter import Shitter
from Shit import Shit
from miscellaneous import *

import regex as re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
import json
import os
from typing import List, Dict, Tuple, Optional

'''
This code was written by Valerio Accardo, 
all rights on the shit that will be monitored 
belong to him and him alone
'''
SHITTER_THRESHOLD = 10

class Chat:
    
    def __init__(self, file_path: str = "Chat WhatsApp con cacatorio.txt"):
        self.lines: List[str] = []
        self.shitlines: List[str] = []
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Il file '{file_path}' non è stato trovato.")

        with open(file_path, "r", encoding='utf-8') as file:
            regex_testo = re.compile(r':\s(.*?)$')
            chat_content = file.read()
            self.lines = chat_content.splitlines()

            for line in self.lines:
                match_testo = regex_testo.search(line)
                if match_testo:
                    if "💩" in match_testo.group(1): 
                        self.shitlines.append(line)
    
    def getLines(self) -> List[str]:
        return self.lines
    
    def getShitLines(self) -> List[str]:
        return self.shitlines


class Bathroom:
    
    def __init__(self, data_inizio: datetime, data_fine: datetime, chat: Chat) -> None:
        self.shitters: List[Shitter] = []
        self.data_inizio = data_inizio
        self.data_fine = data_fine
        self.chat = chat

    def getShitters(self) -> List[Shitter]:
        return self.shitters
    
    def getDateStr(self) -> List[str]:
        delta = self.data_fine - self.data_inizio
        return [(self.data_inizio + datetime.timedelta(days=i)).strftime("%d/%m/%y") for i in range(delta.days + 1)]

    def getClassifica(self) -> str:
        mesi_italiani = ["GENNAIO", "FEBBRAIO", "MARZO", "APRILE", "MAGGIO", "GIUGNO", "LUGLIO", "AGOSTO", "SETTEMBRE", "OTTOBRE", "NOVEMBRE", "DICEMBRE"]

        lista_shitter_tuple: List[Tuple[str, int]] = []            
        classifica = f"CLASSIFICA CACATORIA {self.data_inizio.strftime('%d/%m')} - {self.data_fine.strftime('%d/%m')}:\n\n"
        
        for shitter in self.shitters:
            if len(shitter.getShits()) < SHITTER_THRESHOLD:
                continue
            cacate_totali = []
            try:
                for shit in shitter.getShits():
                    dt = shit.getDateTime(string=False)
                    if dt.month == self.data_fine.month and dt.year == self.data_fine.year:
                        cacate_totali.append(shit)
            except:
                continue
                
            lista_shitter_tuple.append((shitter.getName(), len(cacate_totali)))
        
        lista_shitter_tuple.sort(key=lambda x: x[1], reverse=True)
        lista_shitter_tuple = [x for x in lista_shitter_tuple if x[1] != 0]
        
        for classificato in lista_shitter_tuple:
            classifica += f"{classificato[0]} : {classificato[1]}\n"
        
        return classifica

    '''
    This code was written by Valerio Accardo, 
    all rights on the shit that will be monitored 
    belong to him and him alone
    '''
        
    def flush(self) -> None:
        regex_sender = re.compile(r'-(.*?):')
        shits_by_shitter: Dict[str, List[Shit]] = {}

        for line in self.chat.getShitLines():
            match_shitter = regex_sender.search(line)
            if not match_shitter:
                continue

            try:
                timestamp_str = line.split("-")[0].strip()
                shit = Shit(datetime=timestamp_str, shitter=clean_shitter_name(match_shitter.group(1)))
                
                shitter_name = shit.getShitter()
                if shitter_name not in shits_by_shitter:
                    shits_by_shitter[shitter_name] = []
                shits_by_shitter[shitter_name].append(shit)
            except:
                continue
        
        for shitter_name, ownShits in shits_by_shitter.items():
            if len(ownShits) > SHITTER_THRESHOLD:     #threshold per i meno di 10
                shitter = Shitter(name=shitter_name, shits=ownShits)
                self.shitters.append(shitter)
            else:
                print(f"{shitter_name} skipped from competition , shits : {len(ownShits)}")
            
    def createShitRegister(self) -> None:
        shitRegister = {
            "ByShitterFormat": {},
            "ByDateFormat": {}
        }
        
        for shitter in self.getShitters():
            shitter_name = shitter.getName()
            shitRegister["ByShitterFormat"][shitter_name] = {}
            
            curr = self.data_inizio
            while curr <= self.data_fine:
                m_name = curr.strftime("%B")
                if m_name not in shitRegister["ByShitterFormat"][shitter_name]:
                    shitRegister["ByShitterFormat"][shitter_name][m_name] = {}
                
                for data in getMonthDates(m_name, year=curr.year):
                    shitRegister["ByShitterFormat"][shitter_name][m_name][data] = []
                
                if curr.month == 12: curr = curr.replace(year=curr.year+1, month=1)
                else: curr = curr.replace(month=curr.month+1)

        for shitter in self.getShitters():
            shitter_name = shitter.getName()
            for shit in shitter.getShits():
                dt = shit.getDateTime(string=False)
                if self.data_inizio <= dt <= self.data_fine:
                    m_name = getMonthFromDatetime(dt)
                    data = shit.getDate()
                    if m_name in shitRegister["ByShitterFormat"][shitter_name]:
                        if data in shitRegister["ByShitterFormat"][shitter_name][m_name]:
                            shitRegister["ByShitterFormat"][shitter_name][m_name][data].append(shit.getTime())

        curr = self.data_inizio
        while curr <= self.data_fine:
            m_name = curr.strftime("%B")
            if m_name not in shitRegister["ByDateFormat"]:
                shitRegister["ByDateFormat"][m_name] = {}
            
            for data in getMonthDates(m_name, year=curr.year):
                shitRegister["ByDateFormat"][m_name][data] = {}
                for shitter in self.getShitters():
                    shitRegister["ByDateFormat"][m_name][data][shitter.getName()] = []
            
            if curr.month == 12: curr = curr.replace(year=curr.year+1, month=1)
            else: curr = curr.replace(month=curr.month+1)

        for shitter in self.getShitters():
            shitter_name = shitter.getName()
            for shit in shitter.getShits():
                dt = shit.getDateTime(string=False)
                if self.data_inizio <= dt <= self.data_fine:
                    m_name = getMonthFromDatetime(dt)
                    data = shit.getDate()
                    if m_name in shitRegister["ByDateFormat"]:
                        if data in shitRegister["ByDateFormat"][m_name]:
                            shitRegister["ByDateFormat"][m_name][data][shitter_name].append(shit.getTime())

        try:
            with open("shitRegister.json", "w", encoding='utf-8') as file:
                json.dump(shitRegister, file, indent=4)
            print("SHIT REGISTER CREATO CON SUCCESSO")
        except IOError as e:
            print(f"Errore nel salvataggio: {e}")

    def createShitRegisterGlobal(self) -> None:
        shitRegister = {
            "ByShitterFormat": {},
            "ByDateFormat": {}
        }

        for shitter in self.getShitters():
            shitter_name = shitter.getName()
            
            if shitter_name not in shitRegister["ByShitterFormat"]:
                shitRegister["ByShitterFormat"][shitter_name] = {}
                
            for shit in shitter.getShits():
                dt = shit.getDateTime(string=False)
                y_str = str(dt.year)
                m_name = getMonthFromDatetime(dt) 
                data = shit.getDate()
                time = shit.getTime()

                if y_str not in shitRegister["ByShitterFormat"][shitter_name]:
                    shitRegister["ByShitterFormat"][shitter_name][y_str] = {}
                    
                if m_name not in shitRegister["ByShitterFormat"][shitter_name][y_str]:
                    shitRegister["ByShitterFormat"][shitter_name][y_str][m_name] = {}
                    
                if data not in shitRegister["ByShitterFormat"][shitter_name][y_str][m_name]:
                    shitRegister["ByShitterFormat"][shitter_name][y_str][m_name][data] = []
                
                shitRegister["ByShitterFormat"][shitter_name][y_str][m_name][data].append(time)

                if y_str not in shitRegister["ByDateFormat"]:
                    shitRegister["ByDateFormat"][y_str] = {}
                    
                if m_name not in shitRegister["ByDateFormat"][y_str]:
                    shitRegister["ByDateFormat"][y_str][m_name] = {}
                    
                if data not in shitRegister["ByDateFormat"][y_str][m_name]:
                    shitRegister["ByDateFormat"][y_str][m_name][data] = {}
                
                if shitter_name not in shitRegister["ByDateFormat"][y_str][m_name][data]:
                    shitRegister["ByDateFormat"][y_str][m_name][data][shitter_name] = []
                
                #popolo
                shitRegister["ByDateFormat"][y_str][m_name][data][shitter_name].append(time)

        try:
            with open("shitRegisterGlobal.json", "w", encoding='utf-8') as file:
                json.dump(shitRegister, file, indent=4)
            print("SHIT REGISTER GLOBAL CREATO CON SUCCESSO")
        except IOError as e:
            print(f"Errore nel salvataggio: {e}")