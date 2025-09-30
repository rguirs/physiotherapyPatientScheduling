'''

DONT FORGET TO FIX CURRENT DAY IF YOU ARE RUNNING A REAL WORLD PROBLEM

'''

import pandas as pd
from datetime import datetime

from globalConsts import LANGUAGE

from reading import read_excel_data

from greedy import greedy
from model import model

from runInstance import runTeste
from genOut import generateOutput

from validator import validatorSimple

for instance in range(10, 101):

    if instance in [3, 12, 41, 56, 58, 94]:
        print("colided names")
        continue

    print("##################### ",instance)
    input("go")

    if False:
        print("=================model check")

        file_path, file_path_out, dateStart, dateEnd, initialDay = runTeste(instance, True, True)

        planningHorizon = pd.date_range(start=dateStart, end=dateEnd, freq='D')
        planningHorizon = planningHorizon[planningHorizon.dayofweek < 5]

        initialDay = datetime.strptime(initialDay, "%d/%m/%Y").date()
        initialDay = pd.Timestamp(initialDay)
        slots, staff, patients, N_i, required_N_i, N_pf, required_N_pf, schedule = read_excel_data(initialDay, file_path, planningHorizon)


        #runs an algo to solve the problem
        print("---------- STARTING ALGORITHM") if LANGUAGE == "en" else print("---------- INICIANDO ALGORITMO")
        model(initialDay, planningHorizon, slots, staff, patients, required_N_i, required_N_pf, schedule)

        # if s:

        #     print("---------- PRINTING RESULTS") if LANGUAGE == "en" else print("---------- IMPRIMINDO RESULTADOS")
        #     if generateOutput(file_path_out, file_path, patients, schedule, staff, required_N_pf, slots, planningHorizon):
        #         print("---------- DONE! SUCCESS") if LANGUAGE == "en" else print("\n\n===== CONCLUÍDO COM SUCESSO =====\n")
        #     else:
        #         print("---------- UNEXPECTED FAILURE") if LANGUAGE == "en" else print("FALHA INESPERADA")
    input("Done model check")
    if True:
        print("=================heuristics")

        file_path, file_path_out, dateStart, dateEnd, initialDay = runTeste(instance, False)

        planningHorizon = pd.date_range(start=dateStart, end=dateEnd, freq='D')
        planningHorizon = planningHorizon[planningHorizon.dayofweek < 5]

        initialDay = datetime.strptime(initialDay, "%d/%m/%Y").date()
        initialDay = pd.Timestamp(initialDay)
        slots, staff, patients, N_i, required_N_i, N_pf, required_N_pf, schedule = read_excel_data(initialDay, file_path, planningHorizon)


        #runs an algo to solve the problem
        print("---------- STARTING ALGORITHM") if LANGUAGE == "en" else print("---------- INICIANDO ALGORITMO")
        s, patients, schedule, N_pf = greedy(initialDay, planningHorizon, slots, staff, patients, N_i, N_pf, schedule)
        #s = model(initialDay, planningHorizon, slots, staff, patients, N_i, N_pf, schedule)

        if s:

            print("---------- PRINTING RESULTS") if LANGUAGE == "en" else print("---------- IMPRIMINDO RESULTADOS")
            if generateOutput(file_path_out, file_path, patients, schedule, staff, required_N_pf, slots, planningHorizon):
                print("---------- DONE! SUCCESS") if LANGUAGE == "en" else print("\n\n===== CONCLUÍDO COM SUCESSO =====\n")
            else:
                print("---------- UNEXPECTED FAILURE") if LANGUAGE == "en" else print("FALHA INESPERADA")

            validatorSimple(staff, patients, required_N_i, required_N_pf, schedule)

        else:
            print("heuristics failed")
    input("Done heuristic check")
    if s:
        print("=================model")

        file_path, file_path_out, dateStart, dateEnd, initialDay = runTeste(instance, True)

        planningHorizon = pd.date_range(start=dateStart, end=dateEnd, freq='D')
        planningHorizon = planningHorizon[planningHorizon.dayofweek < 5]

        initialDay = datetime.strptime(initialDay, "%d/%m/%Y").date()
        initialDay = pd.Timestamp(initialDay)
        slots, staff, patients, N_i, required_N_i, N_pf, required_N_pf, schedule = read_excel_data(initialDay, file_path, planningHorizon)


        #runs an algo to solve the problem
        print("---------- STARTING ALGORITHM") if LANGUAGE == "en" else print("---------- INICIANDO ALGORITMO")
        model(initialDay, planningHorizon, slots, staff, patients, required_N_i, required_N_pf, schedule)

        # if s:

        #     print("---------- PRINTING RESULTS") if LANGUAGE == "en" else print("---------- IMPRIMINDO RESULTADOS")
        #     if generateOutput(file_path_out, file_path, patients, schedule, staff, required_N_pf, slots, planningHorizon):
        #         print("---------- DONE! SUCCESS") if LANGUAGE == "en" else print("\n\n===== CONCLUÍDO COM SUCESSO =====\n")
        #     else:
        #         print("---------- UNEXPECTED FAILURE") if LANGUAGE == "en" else print("FALHA INESPERADA")
        input("Done model heuristic check")