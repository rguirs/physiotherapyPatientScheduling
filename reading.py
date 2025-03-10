import pandas as pd
from datetime import datetime, timedelta
import copy

from globalConsts import *

from utils import simplifyString, get_availability_byPreferenceLists, get_availability_byCyclicLists

'''
don't forget to call the function simplifyString when handling slot ids from input files
'''

def read_excel_data(initialDay, path_file, planningHorizon):
    
    print("----- reading settings and slots") if LANGUAGE == "en" else print("----- lendo configurações de horário")
    
    #reading the slots
    try:   
        df_slot = pd.read_excel(path_file, sheet_name=SHEET_DEFSLOT, index_col = FIELD_DEFSLOT_NAME, dtype = str).dropna(how='all')
    except:
        print("FILE NOT FOUND!!!") if LANGUAGE == "en" else print("Arquivo não encontrado!!!")
        exit()
    df_slot["start"] = pd.to_datetime(df_slot[FIELD_DEFSLOT_START], format='%H:%M:%S')
    df_slot["end"] = pd.to_datetime(df_slot[FIELD_DEFSLOT_END], format='%H:%M:%S')
    
    slots = {}
    for index, row in df_slot.iterrows():
        slots[simplifyString(index)] = {"start": row["start"], "end": row["end"]}
    
    #reading the staff
    print("----- reading staff's info") if LANGUAGE == "en" else print("----- lendo informações do pessoal")
    df_staff = pd.read_excel(path_file, sheet_name=SHEET_STAFF, dtype = str).dropna(how='all')
    df_staff.set_index([FIELD_STAFF_ID], inplace=True)
    
    staff = {}
    for index, row in df_staff.iterrows():
        if row[FIELD_STAFF_ROLE] == "Pesquisa":
            staff[index] = {"Name": row[FIELD_STAFF_NAME], "Role": "A", "Patients": []}
        elif row[FIELD_STAFF_ROLE] == "Fisioterapia":
            staff[index] = {"Name": row[FIELD_STAFF_NAME], "Role": "B", "Patients": []}
        else:
            print(f"Pesquisadorx com nome {row[FIELD_STAFF_NAME]} possui um Tipo desconhecido. Deveria ser ou Fisioterapia ou Pesquisa")
            exit()
            
    #creating the matrix N_pf -> the days and shifts the research/physio aren't available
    print("----- reading staff's availability") if LANGUAGE == "en" else print("----- lendo disponibilidade do pessoal")
    N_pf = {}
    for staffMember in staff.keys():
        N_pf[staffMember] = {}
        for day in planningHorizon:
            N_pf[staffMember][day] = {}
            for slot in slots.keys():
                N_pf[staffMember][day][slot] = True
    df_staffSlotsDays = pd.read_excel(path_file, sheet_name=SHEET_STAFFDAYS, dtype = str).dropna(how='all')
    df_staffSlotsDays = df_staffSlotsDays.set_index(FIELD_STAFF_ID)
    N_pf = get_availability_byPreferenceLists(N_pf, df_staffSlotsDays, slots, [FIELD_STAFF_ID, FIELD_STAFF_NAME], planningHorizon)
    ####GET A CyCLICAL UNAVAILABILITY OF RESEARCHERS
    df_staffSlotsCycle = pd.read_excel(path_file, sheet_name=SHEET_STAFFCYCLIC, dtype = str).dropna(how='all')
    df_staffSlotsCycle = df_staffSlotsCycle.set_index(FIELD_STAFF_ID)
    N_pf = get_availability_byCyclicLists(N_pf, df_staffSlotsCycle, slots, planningHorizon, [FIELD_STAFF_ID, FIELD_STAFF_NAME], SHEET_STAFFCYCLIC)
    required_N_pf = copy.deepcopy(N_pf)
    
    #reading the patients
    print("----- reading patient's info") if LANGUAGE == "en" else print("----- lendo informações dos pacientes")
    df_patients = pd.read_excel(path_file, sheet_name=SHEET_PATIENTS, dtype = str).dropna(how='all')
    df_patients.set_index([FIELD_PATIENTS_ID], inplace=True)
    
    patients = {}
    for index, row in df_patients.iterrows():
        patients[index] = {"Name": row[FIELD_PATIENTS_NAME], "researcher": None, "physio": None}
    
    #creating the matrix N_i -> the days and shifts the patients aren't available
    print("----- reading patient's availability") if LANGUAGE == "en" else print("----- lendo disponibilidade do paciente")
    N_i = {}
    for patient in patients.keys():
        N_i[patient] = {}
        for day in planningHorizon:
            N_i[patient][day] = {}
            for slot in slots.keys():
                if initialDay > day: ##automatically sets days in past as unable to schedule
                    N_i[patient][day][slot] = False
                else:
                    N_i[patient][day][slot] = True
    
    df_patientSlotsDays = pd.read_excel(path_file, sheet_name=SHEET_PATIENTSDAYS, dtype = str).dropna(how='all')
    df_patientSlotsDays = df_patientSlotsDays.set_index(FIELD_PATIENTS_ID)
    N_i = get_availability_byPreferenceLists(N_i, df_patientSlotsDays, slots, [FIELD_PATIENTS_ID, FIELD_PATIENTS_NAME], planningHorizon)
    
    df_patientSlotsCycle = pd.read_excel(path_file, sheet_name=SHEET_PATIENTSCYCLIC, dtype = str).dropna(how='all')
    df_patientSlotsCycle = df_patientSlotsCycle.set_index(FIELD_PATIENTS_ID)
    N_i = get_availability_byCyclicLists(N_i, df_patientSlotsCycle, slots, planningHorizon, [FIELD_PATIENTS_ID, FIELD_PATIENTS_NAME], SHEET_PATIENTSCYCLIC)
    
    #get latest schedule
    print("----- reading previous schedule") if LANGUAGE == "en" else print("----- lendo escala anterior")
    sys_esc = pd.read_excel(path_file, sheet_name=SHEET_SYSESC, dtype = str).dropna(how='all')
    
    sessions = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09"]
    follows = ["00", "01"]
    schedule = {}
    for patient in patients.keys():
        schedule[patient] = {}
        for session in sessions:
            schedule[patient][f"SD{session}"] = None
            schedule[patient][f"SH{session}"] = None
        for follow in follows:
            schedule[patient][f"FD{follow}"] = None
            schedule[patient][f"FH{follow}"] = None
    
    x_columns = ["ID"]
    for session in sessions:
        sys_esc[f"SD{session}"] = pd.to_datetime(sys_esc[f"SD{session}"], format='%d/%m/%Y')
        x_columns.append(f"SD{session}")
        x_columns.append(f"SH{session}")
    for follow in follows:
        sys_esc[f"FD{follow}"] = pd.to_datetime(sys_esc[f"FD{follow}"], format='%d/%m/%Y')
        x_columns.append(f"FD{follow}")
        x_columns.append(f"FH{follow}")
    
    #gets the relations patient-researcher-physio (notice: no consistency is checked)
    df_v = sys_esc[["ID", "Res", "Phy"]]
    df_v.set_index(['ID'], inplace=True)
    for index, row in df_v.iterrows():
        if not pd.isnull(row["Res"]) and not pd.isnull(row["Phy"]):
            patients[index]["researcher"] = row["Res"]
            patients[index]["physio"] = row["Phy"]
            staff[row["Res"]]["Patients"].append(index)
            staff[row["Phy"]]["Patients"].append(index)
    
    x = sys_esc[x_columns]
    x.set_index(['ID'], inplace=True)
    
    for index, row in x.iterrows():
        for session in sessions:
            if not pd.isnull(row[f"SD{session}"]) and not pd.isnull(row[f"SH{session}"]):
                schedule[index][f"SD{session}"] = row[f"SD{session}"]
                schedule[index][f"SH{session}"] = simplifyString(row[f"SH{session}"])
        for follow in follows:
            if not pd.isnull(row[f"FD{follow}"]) and not pd.isnull(row[f"FH{follow}"]):
                schedule[index][f"FD{follow}"] = row[f"FD{follow}"]
                schedule[index][f"FH{follow}"] = simplifyString(row[f"FH{follow}"])
                
    #check if sessions were deleted
    print("----- finishing reading data") if LANGUAGE == "en" else print("----- terminando leitura de dados")
    for patient in patients.keys():
        
        for follow in range(2):
            if df_patients.isnull().at[patient, f"Follow {(90*(follow+1))}"]:
                schedule[patient][f"FD0{follow}"] = None
                schedule[patient][f"FH0{follow}"] = None
        
        empty_sessions = 100
        for session in range(9, -1, -1):
            if df_patients.isnull().at[patient, f"{SESSION_NAME_FOR_USER} {0 if session != 9 else ""}{(session+1)}"]:
                empty_sessions = session
        if empty_sessions < 10:
            for session in range(empty_sessions, 10):
                schedule[patient][f"SD0{session}"] = None
                schedule[patient][f"SH0{session}"] = None
                
    #update N_pf according to days that a patient is designated with an appointment
    for patient in patients.keys():
        for follow in range(2):
            if not schedule[patient][f"FD0{follow}"] is None:
                researcher = patients[patient]["researcher"]
                N_pf[researcher][schedule[patient][f"FD0{follow}"]][schedule[patient][f"FH0{follow}"]] = False
        for session in range(10):
            if not schedule[patient][f"SD0{follow}"] is None:
                if session in [0, 9]:
                    researcher = patients[patient]["researcher"]
                    N_pf[researcher][schedule[patient][f"SD0{follow}"]][schedule[patient][f"SH0{follow}"]] = False
                else:
                    physio = patients[patient]["physio"]
                    N_pf[physio][schedule[patient][f"SD0{follow}"]][schedule[patient][f"SH0{follow}"]] = False
                
    return slots, staff, patients, N_i, N_pf, required_N_pf, schedule