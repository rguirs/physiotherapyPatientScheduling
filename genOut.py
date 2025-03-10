import pandas as pd
import numpy as np

from globalConsts import LANGUAGE

import shutil

def generateOutput(file_path, file_path_input, patients, schedule, staff, required_N_pf, slots, planningHorizon):
    
    shutil.copyfile(file_path_input, file_path)
    
    print("---------- creating patient's schedule table") if LANGUAGE == "en" else print("----- gerando tabela dos pacientes")
    output_patients = pd.DataFrame(dtype = str)
    output_patients["ID"] = patients.keys()
    
    output_patients[" "] = np.nan
    
    output_patients["Nome"] = pd.Series("")
    for patient in patients.keys():
        output_patients.loc[output_patients["ID"] == patient, "Nome"] = patients[patient]["Name"]
    
    output_patients["  "] = np.nan
    
    sessionNames = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]
    for i in range(10):
        output_patients[f"Sessão {sessionNames[i]}"] = pd.Series("")
        for patient in patients.keys():
            output_patients.loc[output_patients["ID"] == patient, f"Sessão {sessionNames[i]}"] = schedule[patient][f"SD0{i}"].strftime('%d/%m/%Y') + " " + schedule[patient][f"SH0{i}"]
    for i in range(2):
        output_patients[f"Follow {(90*(i+1))}"] = pd.Series("")
        for patient in patients.keys():
            output_patients.loc[output_patients["ID"] == patient, f"Follow {(90*(i+1))}"] = schedule[patient][f"FD0{i}"].strftime('%d/%m/%Y') + " " + schedule[patient][f"FH0{i}"]
    
    with pd.ExcelWriter(file_path, mode="a", if_sheet_exists="replace", engine="openpyxl") as writer:
        output_patients.to_excel(writer, sheet_name="Pacientes", index=False)
    
    planningHorizon_asDate = [asDate.strftime("%m/%d/%Y") for asDate in planningHorizon]
    
    output_appointmentsStaff = pd.DataFrame(index = slots.keys(), columns = planningHorizon, dtype = str)
    output_appointmentsStaff = output_appointmentsStaff.fillna("")
    
    ###create table for each staff member
    print("---------- creating a schedule table for each reseracher/physio") if LANGUAGE == "en" else print("----- gerando tabela de cada pesquisadorx/fisio")
    total = len(staff.keys())
    total = 1 if total < 1 else total
    done = 0
    for staffMember in staff:
        print(f"---------- creating a schedule table for each researcher/physio: {done/total}") if LANGUAGE == "en" else print(f"----- gerando tabela de cada pesquisadorx/fisio: {done/total}")
        output_staffMember = pd.DataFrame(index = slots.keys(), columns = planningHorizon)
        for day in planningHorizon:
            for slot in slots.keys():
                if not required_N_pf[staffMember][day][slot]:
                    output_staffMember.at[slot, day] = "OFF"
        for patient in patients.keys():
            if patients[patient]["researcher"] == staffMember:
                for follow in range(2):
                    output_staffMember.at[schedule[patient][f"FH0{follow}"], schedule[patient][f"FD0{follow}"]] = patients[patient]["Name"]
                    output_appointmentsStaff.at[schedule[patient][f"FH0{follow}"], schedule[patient][f"FD0{follow}"]] += f"({schedule[patient][f"FH0{follow}"]}) {staff[staffMember]["Name"]}:\n{patients[patient]["Name"]}\n"
                for session in [0, 9]:
                    output_staffMember.at[schedule[patient][f"SH0{session}"], schedule[patient][f"SD0{session}"]] = patients[patient]["Name"]
                    output_appointmentsStaff.at[schedule[patient][f"SH0{session}"], schedule[patient][f"SD0{session}"]] += f"({schedule[patient][f"SH0{session}"]}) {staff[staffMember]["Name"]}:\n{patients[patient]["Name"]}\n"
            elif patients[patient]["physio"] == staffMember:
                for session in range(1, 9):
                    output_staffMember.at[schedule[patient][f"SH0{session}"], schedule[patient][f"SD0{session}"]] = patients[patient]["Name"]
                    output_appointmentsStaff.at[schedule[patient][f"SH0{session}"], schedule[patient][f"SD0{session}"]] += f"({schedule[patient][f"SH0{session}"]}) {staff[staffMember]["Name"]}:\n{patients[patient]["Name"]}\n"
        output_staffMember.columns = planningHorizon_asDate
        done += 1
        with pd.ExcelWriter(file_path, mode="a", if_sheet_exists="replace", engine="openpyxl") as writer:
            output_staffMember.to_excel(writer, sheet_name=f"Escala|{staffMember}")
    done = total
    print(f"----- creating a schedule table for each researcher/physio: {done/total}") if LANGUAGE == "en" else print(f"----- gerando tabela de cada pesquisadorx/fisio: {done/total}")
            
    print("----- creating main schedule table") if LANGUAGE == "en" else print("----- gerando tabela geral")
    output_appointmentsStaff.columns = planningHorizon_asDate
    with pd.ExcelWriter(file_path, mode="a", if_sheet_exists="replace", engine="openpyxl") as writer:
            output_appointmentsStaff.to_excel(writer, sheet_name=f"Escala")
    
    ###create sysEsc
    print("----- creating system table (sysEsc)") if LANGUAGE == "en" else print("----- gerando tabela do sistema (sysEsc)")
    sysEsc = pd.DataFrame(dtype = str)
    sysEsc["ID"] = patients.keys()
    sysEsc["Pesq"] = pd.Series("")
    sysEsc["Fisio"] = pd.Series("")
    for i in range(10):
        sysEsc[f"SD0{i}"] = pd.Series("")
        sysEsc[f"SH0{i}"] = pd.Series("")
    for i in range(2):
        sysEsc[f"FD0{i}"] = pd.Series("")
        sysEsc[f"FH0{i}"] = pd.Series("")
    for patient in patients.keys():
        sysEsc.loc[sysEsc["ID"] == patient, "Pesq"] = patients[patient]["researcher"]
        sysEsc.loc[sysEsc["ID"] == patient, "Fisio"] = patients[patient]["physio"]
        for i in range(2):
            sysEsc.loc[sysEsc["ID"] == patient, f"FD0{i}"] = schedule[patient][f"FD0{i}"].strftime("%d/%m/%Y")
            sysEsc.loc[sysEsc["ID"] == patient, f"FH0{i}"] = schedule[patient][f"FH0{i}"]
        for i in range(10):
            sysEsc.loc[sysEsc["ID"] == patient, f"SD0{i}"] = schedule[patient][f"SD0{i}"].strftime("%d/%m/%Y")
            sysEsc.loc[sysEsc["ID"] == patient, f"SH0{i}"] = schedule[patient][f"SH0{i}"]
            
    sysEsc.rename(columns={"ID": "Pac"}, inplace=True)
    with pd.ExcelWriter(file_path, mode="a", if_sheet_exists="replace", engine="openpyxl") as writer:
        sysEsc.to_excel(writer, sheet_name=f"sysEsc", index=False)
        
    return True