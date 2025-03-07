'''

criar exemplos

'''

import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from reading import read_excel_data

from greedy import greedy

from genOut import generateOutput

for instance in range(1,7):

    nameOfFile = f"./examples/eg.schedule.{instance}.rs"
    FILE_PATH = f"{nameOfFile}.xlsx"
    FILE_PATH_OUT = f"{nameOfFile}.ot.xlsx"
    reschedule = True

    dateStarts = ["01/01/2023", "01/01/2024", "01/01/2025", "01/01/2024", "01/01/2023", "01/01/2023"]
    dateEnds =   ["31/07/2024", "31/12/2024", "31/12/2025", "31/12/2025", "31/12/2025", "31/12/2025"]


    print("---------- LENDO ARQUIVO EXCEL")
    dateStart = pd.to_datetime(dateStarts[instance-1], format="%d/%m/%Y")
    dateEnd = pd.to_datetime(dateEnds[instance-1], format="%d/%m/%Y")
    CURRENT_DAY = dateStart.strftime('%d/%m/%Y') #datetime.today().strftime('%d/%m/%Y')
    planningHorizon = pd.date_range(start=dateStart, end=dateEnd, freq='D')
    planningHorizon = planningHorizon[planningHorizon.dayofweek < 5]

    initialDay = datetime.strptime(CURRENT_DAY, "%d/%m/%Y").date() + (relativedelta(month=(3)) if reschedule else timedelta(days=0))
    initialDay = pd.Timestamp(initialDay)
    slots, staff, patients, N_i, N_pf, required_N_pf, schedule = read_excel_data(initialDay, FILE_PATH, planningHorizon)

    #THERE MUST BE A FUNCTION THAT SETS CURRENT DAY TO THE BEST NEAREST DAY OF THE PATIENT


    #runs an algo to solve the problem
    print("---------- INICIANDO ALGORITMO")
    s, patientes, schedule, N_pf = greedy(initialDay, planningHorizon, slots, staff, patients, N_i, N_pf, schedule)
    #model(initialDay, def_slot, staff, patients, constrPatients, v, x, N_i, N_pf, planningHorizon)

    if s:

        print("---------- IMPRIMINDO RESULTADOS")
        if generateOutput(FILE_PATH_OUT, FILE_PATH, patients, schedule, staff, required_N_pf, slots, planningHorizon):
            print("\n\n===== CONCLUÍDO COM SUCESSO =====\n")
        else:
            print("FALHA INESPERADA")