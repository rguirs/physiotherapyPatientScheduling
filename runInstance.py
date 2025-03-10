'''
NEEDS TO SEPARATE THE SCHEDULING AND RESCHEDULING
'''
import pandas as pd
from datetime import timedelta

from globalConsts import LANGUAGE

def runInstance(instance, isInstanceReschedule, daysToSkipReschedule = 60, markIsModel = False):

    examplesDir = "examplesEN" if LANGUAGE == "en" else "examplesBR"

    nameOfFile = f"./{examplesDir}/eg.schedule.{instance}"
    file_path = f"{nameOfFile}.rs.xlsx" if isInstanceReschedule else f"{nameOfFile}.xlsx"
    modelMark = ".m" if markIsModel else ""
    file_path_out = f"{nameOfFile}.rs{modelMark}.ot.xlsx" if isInstanceReschedule else f"{nameOfFile}{modelMark}.ot.xlsx"

    dateStarts = ["01/01/2023", "01/01/2024", "01/01/2025", "01/01/2024", "01/01/2023", "01/01/2023"]
    dateEnds =   ["31/07/2024", "31/12/2024", "31/12/2025", "31/12/2025", "31/12/2025", "31/12/2025"]


    print("---------- READING EXCEL FILE") if LANGUAGE == "en" else print("---------- LENDO ARQUIVO EXCEL")
    dateStart = pd.to_datetime(dateStarts[instance-1], format="%d/%m/%Y")
    dateEnd = pd.to_datetime(dateEnds[instance-1], format="%d/%m/%Y")

    CURRENT_DAY = (dateStart + timedelta(days=daysToSkipReschedule)).strftime('%d/%m/%Y')

    return file_path, file_path_out, dateStart, dateEnd, CURRENT_DAY