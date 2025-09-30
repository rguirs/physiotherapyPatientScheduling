'''
NEEDS TO SEPARATE THE SCHEDULING AND RESCHEDULING
'''
import pandas as pd
from datetime import timedelta

from globalConsts import LANGUAGE

def runTeste(instance, model, check = False):

    instancesData = {
        1: {"start": "01/01/2025", "end": "31/07/2025"},
    }

    #examplesDir = "examplesEN" if LANGUAGE == "en" else "examplesBR"
    examplesDir = "testes"

    nameOfFile = f"./{examplesDir}/eg.schedule.{instance}"
    file_path = f"{nameOfFile}.xlsx" if not model else f"{nameOfFile}.ot.xlsx"
    if check:
        file_path = f"{nameOfFile}.xlsx"
    print("---->", file_path)
    modelMark = ".m" if model else ""
    file_path_out = f"{nameOfFile}{modelMark}.ot.xlsx"

    print("---------- READING EXCEL FILE") if LANGUAGE == "en" else print("---------- LENDO ARQUIVO EXCEL")
    dateStart = pd.to_datetime("01/01/2024", format="%d/%m/%Y")
    dateEnd = pd.to_datetime("31/12/2025", format="%d/%m/%Y")

    CURRENT_DAY = (dateStart).strftime('%d/%m/%Y')

    return file_path, file_path_out, dateStart, dateEnd, CURRENT_DAY

def runReal(model, instancia):

    #examplesDir = "examplesEN" if LANGUAGE == "en" else "examplesBR"
    examplesDir = "testes"

    # nameOfFile = f"./{examplesDir}/eg.schedule.{instancia}"
    nameOfFile = f"./{examplesDir}/desajustado"
    file_path = f"{nameOfFile}.xlsx" if not model else f"{nameOfFile}.ot.xlsx"
    
    print("---->", file_path)
    modelMark = ".m" if model else ""
    file_path_out = f"{nameOfFile}{modelMark}.ot.xlsx"

    print("---------- READING EXCEL FILE") if LANGUAGE == "en" else print("---------- LENDO ARQUIVO EXCEL")
    dateStart = pd.to_datetime("01/01/2025", format="%d/%m/%Y")
    dateEnd = pd.to_datetime("31/12/2025", format="%d/%m/%Y")

    CURRENT_DAY = (dateStart).strftime('%d/%m/%Y')

    return file_path, file_path_out, dateStart, dateEnd, CURRENT_DAY