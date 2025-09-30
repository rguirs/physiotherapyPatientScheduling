import pandas as pd
from datetime import datetime

from globalConsts import LANGUAGE

def simplifyString(inputStr):
    return inputStr.upper().replace(" ", "")

def get_availability_byPreferenceLists(N_availability, data, slots, notSlotColumns, planningHorizon):

    col_names = data.columns
    
    i = 0
    while i < len(data):
        
        user_id = data.index[i]
        
        for j in range(data.shape[1]):
            if not (col_names[j] in notSlotColumns):
                if not pd.isnull(data.iloc[i, j]):
                    
                    try:
                        day = datetime.strptime(data.iloc[i, j], "%Y-%m-%d %H:%M:%S")
                    except:
                        try:
                            day = datetime.strptime(data.iloc[i, j], "%d/%m/%Y")
                        except:
                            print(f"Not possible to read the date {data.iloc[i, j]} of patient {user_id}") if LANGUAGE == "en" else print(f"Impossível ler a data {data.iloc[i, j]} no paciente {user_id}")
                            exit()
                    
                    if day in planningHorizon:
                    
                        slot = None
                        
                        if i+1 < len(data):
                        
                            slot = data.iloc[i+1, j]
                        
                        if pd.isnull(slot):
                            for slot in slots.keys():
                                N_availability[user_id][day][slot] = False
                        else:
                            N_availability[user_id][day][slot] = False
            
        i += 2

    return N_availability
    
def get_availability_byCyclicLists(N_availability, data, slots, planningHorizon, notSlotColumns, sheetName):

    col_names = data.columns
    
    daysOfTheWeek = ["MON", "TUE", "WED", "THU", "FRI"] if LANGUAGE == "en" else ["SEG", "TER", "QUA", "QUI", "SEX"]
    
    i = 0
    while i < len(data):
        
        user_id = data.index[i]
        
        for j in range(data.shape[1]):
            if not (col_names[j] in notSlotColumns):
                if not pd.isnull(data.iloc[i, j]):
                    
                    day = data.iloc[i, j].upper()

                    if day.strip() != "":

                        if not (any (weekday in day for weekday in daysOfTheWeek)):
                            print(f"Week day {day} not known at sheet {sheetName}")if LANGUAGE == "en" else print(f"Dia da semana {day} desconhecido na folha {sheetName}", user_id, i ,j)
                            exit()
                            
                        weekday = None
                        for k in range(5):
                            if daysOfTheWeek[k] in day:
                                weekday = k
                            
                        slot = None
                        slot_focus = []
                        if i+1 < len(data):
                        
                            slot = data.iloc[i+1, j]
                        
                        if pd.isnull(slot):
                            for slot in slots.keys():
                                slot_focus.append(slot)
                        else:
                            slot_focus.append(slot)
                            
                        for slot in slot_focus:
                            for day in planningHorizon:
                                if day.dayofweek == weekday:
                                    N_availability[user_id][day][slot] = False
            
        i += 2

    return N_availability