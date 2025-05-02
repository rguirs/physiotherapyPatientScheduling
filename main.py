'''

DONT FORGET TO FIX CURRENT DAY IF YOU ARE RUNNING A REAL WORLD PROBLEM

'''

import pandas as pd
from datetime import datetime

from globalConsts import LANGUAGE

from reading import read_excel_data

from greedy import greedy
from model import model

from runInstance import runInstance
from genOut import generateOutput


mockInstance = True
instance = 1
isInstanceReschedule = True

if mockInstance:
    daysToSkipSchedule = 5
    daysToSkipReschedule = 35
    daysToSkip = daysToSkipSchedule if isInstanceReschedule else daysToSkipSchedule
    markIsModel = False
    file_path, file_path_out, dateStart, dateEnd, initialDay = runInstance(instance, isInstanceReschedule, daysToSkipReschedule, markIsModel)

else:
    nameOfFile = f"schedule"
    file_path = f"{nameOfFile}.xlsx"
    file_path_out = f"{nameOfFile}.ot.xlsx"

    dateStart = "01/01/2025"
    dateEnd =   "31/12/2027"


    print("---------- READING EXCEL FILE") if LANGUAGE == "en" else print("---------- LENDO ARQUIVO EXCEL")
    dateStart = pd.to_datetime(dateStart, format="%d/%m/%Y")
    dateEnd = pd.to_datetime(dateEnd, format="%d/%m/%Y")

    '''
    THERE COULD BE A FUNCTION THAT SETS CURRENT DAY TO THE BEST NEAREST DAY OF THE PATIENT'

    For example: if a patient comes on Thursday, it might not be good to assign them to Friday, or even on the next week (if there are slots available)
    '''
    
    initialDay = datetime.today().strftime('%d/%m/%Y')

planningHorizon = pd.date_range(start=dateStart, end=dateEnd, freq='D')
planningHorizon = planningHorizon[planningHorizon.dayofweek < 5]

initialDay = datetime.strptime(initialDay, "%d/%m/%Y").date()
initialDay = pd.Timestamp(initialDay)
slots, staff, patients, N_i, N_pf, required_N_pf, schedule = read_excel_data(initialDay, file_path, planningHorizon)


#runs an algo to solve the problem
print("---------- STARTING ALGORITHM") if LANGUAGE == "en" else print("---------- INICIANDO ALGORITMO")
s, patients, schedule, N_pf = model(initialDay, planningHorizon, slots, staff, patients, N_i, N_pf, schedule)
#s = model(initialDay, planningHorizon, slots, staff, patients, N_i, N_pf, schedule)

if s:

    print("---------- PRINTING RESULTS") if LANGUAGE == "en" else print("---------- IMPRIMINDO RESULTADOS")
    if generateOutput(file_path_out, file_path, patients, schedule, staff, required_N_pf, slots, planningHorizon):
        print("---------- DONE! SUCCESS") if LANGUAGE == "en" else print("\n\n===== CONCLUÍDO COM SUCESSO =====\n")
    else:
        print("---------- UNEXPECTED FAILURE") if LANGUAGE == "en" else print("FALHA INESPERADA")