'''

DONT FORGET TO FIX CURRENT DAY IF YOU ARE RUNNING A REAL WORLD PROBLEM

'''

import pandas as pd
from datetime import datetime

from globalConsts import LANGUAGE

from reading import read_excel_data

from greedy import greedy
from model import model

from runInstance import runTeste, runReal
from genOut import generateOutput

from validator import validatorSimple

instance = 4
runModel = True

if True:
    print("=================model for sure")

    file_path, file_path_out, dateStart, dateEnd, initialDay = runReal((runModel), "1")

    planningHorizon = pd.date_range(start=dateStart, end=dateEnd, freq='D')
    planningHorizon = planningHorizon[planningHorizon.dayofweek < 5]

    initialDay = datetime.strptime(initialDay, "%d/%m/%Y").date()
    initialDay = pd.Timestamp(initialDay)
    slots, staff, patients, N_i, required_N_i, N_pf, required_N_pf, schedule = read_excel_data(initialDay, file_path, planningHorizon)

    print(validatorSimple(staff, patients, required_N_i, required_N_pf, schedule))
    # input("The val")

    #runs an algo to solve the problem
    print("---------- STARTING ALGORITHM") if LANGUAGE == "en" else print("---------- INICIANDO ALGORITMO")
    if runModel:
        s, patients, schedule, N_pf = model(initialDay, planningHorizon, slots, staff, patients, required_N_i, required_N_pf, schedule, True)
    else:
        s, patients, schedule, N_pf = greedy(initialDay, planningHorizon, slots, staff, patients, required_N_i, required_N_pf, schedule)

    if s:

        print("---------- PRINTING RESULTS") if LANGUAGE == "en" else print("---------- IMPRIMINDO RESULTADOS")
        if generateOutput(file_path_out, file_path, patients, schedule, staff, required_N_pf, slots, planningHorizon):
            print("---------- DONE! SUCCESS") if LANGUAGE == "en" else print("\n\n===== CONCLUÍDO COM SUCESSO =====\n")
        else:
            print("---------- UNEXPECTED FAILURE") if LANGUAGE == "en" else print("FALHA INESPERADA")