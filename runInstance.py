'''
NEEDS TO SEPARATE THE SCHEDULING AND RESCHEDULING
'''
import pandas as pd

from globalConsts import LANGUAGE

def runInstance(instance, isInstanceReschedule, markIsModel = False):

    examplesDir = "examplesEN" if LANGUAGE == "en" else "examplesBR"

    nameOfFile = f"./examples/eg.schedule.{instance}"
    file_path = f"{nameOfFile}.xlsx"
    file_path_out = f"{nameOfFile}.m.ot.xlsx" if markIsModel else f"{nameOfFile}.ot.xlsx"

    dateStarts = ["01/01/2023", "01/01/2024", "01/01/2025", "01/01/2024", "01/01/2023", "01/01/2023"]
    dateEnds =   ["31/07/2024", "31/12/2024", "31/12/2025", "31/12/2025", "31/12/2025", "31/12/2025"]


    print("---------- READING EXCEL FILE") if LANGUAGE == "en" else print("---------- LENDO ARQUIVO EXCEL")
    dateStart = pd.to_datetime(dateStarts[instance-1], format="%d/%m/%Y")
    dateEnd = pd.to_datetime(dateEnds[instance-1], format="%d/%m/%Y")

    CURRENT_DAY = dateStart.strftime('%d/%m/%Y') #datetime.today().strftime('%d/%m/%Y')

    return file_path, file_path_out, dateStart, dateEnd, CURRENT_DAY