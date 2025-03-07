import pandas as pd
import random
from warnings import simplefilter
import shutil
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

schedule = False
reschedule = True

def simplifyString(inputStr): #the same as in utils
    return inputStr.upper().replace(" ", "")

###just some random list of star wars names (made with AI, so there might be some allucination) - by the way, I dont know most of them
names = ["Luke Skywalker", "Darth Vader", "Leia Organa", "Han Solo", "Obi-Wan Kenobi", "Yoda", "Chewbacca", "C-3PO", "R2-D2", "Palpatine", "Darth Maul", "Qui-Gon Jinn", "Mace Windu", "Count Dooku", "General Grievous", "Anakin Skywalker", "Padmé Amidala", "Jango Fett", "Boba Fett", "Lando Calrissian", "Wedge Antilles", "Admiral Ackbar", "Mon Mothma", "Grand Moff Tarkin", "Bib Fortuna", "Jabba the Hutt", "Greedo", "Bossk", "IG-88", "Dengar", "4-LOM", "Zuckuss", "Nien Nunb", "Max Rebo", "Sy Snootles", "Salacious Crumb", "Wicket W. Warrick", "Ewok", "Jawas", "Tusken Raider", "Stormtrooper", "Clone Trooper", "Battle Droid", "Super Battle Droid", "Droideka", "Plo Koon", "Kit Fisto", "Ki-Adi-Mundi", "Aayla Secura", "Shaak Ti", "Luminara Unduli", "Barriss Offee", "Commander Cody", "Captain Rex", "Commander Gree", "Commander Bly", "Asajj Ventress", "Cad Bane", "Hondo Ohnaka", "Pre Vizsla", "Bo-Katan Kryze", "Gar Saxon", "Sabine Wren", "Hera Syndulla", "Kanan Jarrus", "Ezra Bridger", "Chopper", "Grand Admiral Thrawn", "Agent Kallus", "The Inquisitor", "Seventh Sister", "Fifth Brother", "Eighth Brother", "Darth Revan", "Darth Malak", "Bastila Shan", "HK-47", "Carth Onasi", "Jolee Bindo", "Mission Vao", "Zaalbar", "Kreia", "Darth Traya", "Darth Nihilus", "Darth Sion", "Meetra Surik", "Atton Rand", "Bao-Dur", "Mira", "Visas Marr", "Cal Kestis", "BD-1", "Cere Junda", "Greef Karga", "The Mandalorian", "Grogu", "Cara Dune", "Kuiil", "Moff Gideon", "Fennec Shand", "Boba Fett", "Ahsoka Tano", "Captain Phasma", "Kylo Ren", "Rey", "Finn", "Poe Dameron", "General Hux", "Rose Tico", "Maz Kanata", "Supreme Leader Snoke", "Jannah", "Zorii Bliss", "Beaumont Kin", "Boolio", "DJ", "Admiral Holdo", "Ben Solo", "Wampa", "Tauntaun", "Eopie", "Bantha", "Nexu", "Acklay", "Reek", "Krayt Dragon", "Porg", "Vulptex", "Thala-siren", "Space Slug", "Dagobah Snake", "Rancor", "Ochi of Bestoon", "Trilla Suduri", "Second Sister", "Ninth Sister", "Taron Malicos", "Saw Gerrera", "Bodhi Rook", "Chirrut Îmwe", "Baze Malbus", "Orson Krennic", "Galen Erso", "Lyra Erso", "Cassian Andor", "K-2SO", "Bistan", "Pao", "Raddus", "Darth Bane", "Darth Zannah", "Darth Plagueis", "Darth Tenebrous", "Darth Andeddu", "Darth Vectivus", "Darth Gravid", "Darth Ramage", "Darth Cognus", "Darth Millennial"]

slot_options = [{"Name": "8h - 10h", "Start": "08:00:00", "End": "09:59:00"},{"Name": "10h - 12h", "Start": "10:00:00", "End": "11:59:00"},{"Name": "14h - 16h", "Start": "14:00:00", "End": "15:59:00"},{"Name": "16h - 18h", "Start": "16:00:00", "End": "17:59:00"},{"Name": "19h - 21h", "Start": "19:00:00", "End": "20:59:00"},{"Name": "21h - 23h", "Start": "21:00:00", "End": "22:59:00"}]
#now we create the instances

instances = [i for i in range(1, 7)]

numberOfSlots = [2, 4, 6, 4, 4, 4]

numberOfPacients = [50, 50, 50, 100, 150, 150]
numberOfResearchers = [1, 2, 2, 2, 2, 2]
numberOfPhysio = [1, 1, 2, 2, 2, 3]

patientUnavailabilityPreference = [10, 20, 30, 30, 40, 50]
patientUnavailabilityPreference[:] = [x / 300 for x in patientUnavailabilityPreference]
patientUnavailabilityCiclic = [1, 2, 2, 3, 3, 3]
patientUnavailabilityCiclic[:] = [x / 5 for x in patientUnavailabilityCiclic]
patientUnavailabilitySlot = [0.25, 0.4, 0.4, 0.4, 0.5, 0.6]
patientUnavailabilitySlot[:] = [patientUnavailabilitySlot[i] / numberOfSlots[i] for i in range(len(patientUnavailabilitySlot))]

staffUnavailabilityPreference = [5, 5, 10, 10, 20, 25]
staffUnavailabilityPreference[:] = [x / 300 for x in staffUnavailabilityPreference]

holydays2023 = "01/01/2023", "20/02/2023", "21/02/2023", "07/04/2023", "21/04/2023", "01/05/2023", "08/06/2023", "07/09/2023", "12/10/2023", "02/11/2023", "15/11/2023", "20/11/2023", "25/12/2023"
holydays2024 = "01/01/2024", "12/02/2024", "13/02/2024", "29/03/2024", "21/04/2024", "01/05/2024", "30/05/2024", "07/09/2024", "12/10/2024", "02/11/2024", "15/11/2024", "20/11/2024", "25/12/2024"
holydays2025 = "01/01/2025", "03/03/2025", "04/03/2025", "18/04/2025", "21/04/2025", "01/05/2025", "19/06/2025", "07/09/2025", "12/10/2025", "02/11/2025", "15/11/2025", "20/11/2025", "25/12/2025"

dateStarts = ["01/01/2023", "01/01/2024", "01/01/2025", "01/01/2024", "01/01/2023", "01/01/2023"]
dateEnds =   ["31/07/2024", "31/12/2024", "31/12/2025", "31/12/2025", "31/12/2025", "31/12/2025"]
holydays = [holydays2023, holydays2024, holydays2025, holydays2024 + holydays2025, holydays2023 + holydays2024 + holydays2025, holydays2023 + holydays2024 + holydays2025]

sessions_userNames = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]

##now, we are creating sheduling examples
if schedule:
    for i in range(len(instances)):
        
        print(f"------ generating instance {instances[i]}")
        
        file_path = f"eg.schedule.{instances[i]}.xlsx"
        
        dateStart = pd.to_datetime(dateStarts[i], format="%d/%m/%Y")
        dateEnd = pd.to_datetime(dateEnds[i], format="%d/%m/%Y")
        planningHorizon = pd.date_range(start=dateStart, end=dateEnd, freq='D')
        planningHorizon = planningHorizon[planningHorizon.dayofweek < 5]
        planningHorizon = [day.strftime("%d/%m/%Y") for day in planningHorizon]
        
        names_patients = random.choices(names, k=numberOfPacients[i])
        names_researchers = random.choices(names, k=numberOfResearchers[i])
        names_physio = random.choices(names, k=numberOfPhysio[i])
        
        #just to guarantee no id is identical (we are using id based on name for the staff)
        all_staffNames = names_researchers + names_physio
        if len(all_staffNames) != len(set(all_staffNames)):
            print("WARNING, RUN AGAIN, NAMES COLLIDED IN STAFF")
        
        slots = {}
        for j in range(numberOfSlots[i]):
            slots[simplifyString(slot_options[j]["Name"])] = {"Name": slot_options[j]["Name"], "start": slot_options[j]["Start"], "end": slot_options[j]["End"]}
        
        patients = {}
        for j in range(len(names_patients)):
            patients[str(j+1)] = {"Name": names_patients[j], "researcher": None, "physio": None}
            
        ##generate sheet "sysEsc"
        print("sheet sysEsc")
        columns_sysEsc = ["Pac", "Pesq", "Fisio", "SD00", "SH00", "SD01", "SH01", "SD02", "SH02", "SD03", "SH03", "SD04", "SH04", "SD05", "SH05", "SD06", "SH06", "SD07", "SH07", "SD08", "SH08", "SD09", "SH09", "FD00", "FH00", "FD01", "FH01"]
        df_sysEsc = pd.DataFrame(columns = columns_sysEsc)
        with pd.ExcelWriter(file_path, mode="a", if_sheet_exists="replace", engine="openpyxl") as writer:
            df_sysEsc.to_excel(writer, sheet_name=f"sysEsc", index=False)
        
        ##generate sheet "DefSlot"
        print("sheet defSlot")
        columns_defSlot = ["Nome Slot", " ", "Início Slot", "Fim Slot"]
        df_defSlot = pd.DataFrame(columns = columns_defSlot)
        for j in range(numberOfSlots[i]):
            df_defSlot.loc[slot_options[j]["Name"], "Nome Slot"] = slot_options[j]["Name"]
            df_defSlot.loc[slot_options[j]["Name"], "Início Slot"] = slot_options[j]["Start"]
            df_defSlot.loc[slot_options[j]["Name"], "Fim Slot"] = slot_options[j]["End"]
        with pd.ExcelWriter(file_path, mode="a", if_sheet_exists="replace", engine="openpyxl") as writer:
            df_defSlot.to_excel(writer, sheet_name=f"DefSlot", index=False)
            
        ##generate sheet "Pacientes"
        print("sheet pacientes")
        columns_patients = ["ID", " ", "Nome"] + [f"Sessão {sessions_userNames[j]}" for j in range(10)] + [f"Follow {(90*j)}" for j in range(1,3)]
        df_patients = pd.DataFrame(columns = columns_patients)
        for patient in patients.keys():
            df_patients.loc[patient, "ID"] = patient
            df_patients.loc[patient, "Nome"] = patients[patient]["Name"]
        
        with pd.ExcelWriter(file_path, mode="a", if_sheet_exists="replace", engine="openpyxl") as writer:
            df_patients.to_excel(writer, sheet_name=f"Pacientes", index=False)
            
        ##generate sheet "Pessoal"
        print("sheet pessoal")
        columns_pessoal = ["ID", " ", "Tipo", " ", "Nome"]
        df_pessoal = pd.DataFrame(columns = columns_pessoal)
        for j in range(len(names_researchers)):
            name = names_researchers[j]
            df_pessoal.loc[simplifyString(name), "ID"] = simplifyString(name)
            df_pessoal.loc[simplifyString(name), "Tipo"] = "Pesquisa"
            df_pessoal.loc[simplifyString(name), "Nome"] = name
        for j in range(len(names_physio)):
            name = names_physio[j]
            df_pessoal.loc[simplifyString(name), "ID"] = simplifyString(name)
            df_pessoal.loc[simplifyString(name), "Tipo"] = "Fisioterapia"
            df_pessoal.loc[simplifyString(name), "Nome"] = name
            
        with pd.ExcelWriter(file_path, mode="a", if_sheet_exists="replace", engine="openpyxl") as writer:
            df_pessoal.to_excel(writer, sheet_name=f"Pessoal", index=False)
        
        ##cyclical preferences
        print("sheet cyclical")
        df_patientPreferenceCyclic = pd.DataFrame(columns = ["ID", "Nome"])
        j = 1
        for patient in patients.keys():
            k = 4
            df_patientPreferenceCyclic.loc[j, "ID"] = patient
            df_patientPreferenceCyclic.loc[j, "Nome"] = patients[patient]["Name"]
            df_patientPreferenceCyclic.loc[j+1, " "] = " "
            
            N_i = []
            
            w = 0
            for weekday in ["Seg", "Ter", "Qua", "Qui", "Sex"]:
                if random.random() < patientUnavailabilityCiclic[i]:
                    N_i.append([1 for i in range(numberOfSlots[i])])
                else:
                    N_i.append([0 for i in range(numberOfSlots[i])])
                    l = 0
                    for slot in slots:
                        if random.random() < patientUnavailabilitySlot[i]:
                            N_i[w][l] = 1
                        l += 1
                w += 1
            if sum(sum(N_i, [])) >= 0.95*5*numberOfSlots[i]:
                previous = sum(sum(N_i, []))
                weekdays = [0, 1, 2, 3, 4]
                random.shuffle(weekdays)
                for w in range(5):
                    if sum(N_i[weekdays[w]]) >= 0.5*numberOfSlots[i]:
                        N_i[weekdays[w]] = [0 for i in range(numberOfSlots[i])]
                        if random.random() > patientUnavailabilityCiclic[i]:
                            break
                
            w = 0
            for weekday in ["Seg", "Ter", "Qua", "Qui", "Sex"]:
                if sum(N_i[w]) == numberOfSlots[i]:
                    df_patientPreferenceCyclic.loc[j, k] = weekday
                    k += 1
                else:
                    l = 0
                    for slot in slots:
                        if N_i[w][l]:
                            df_patientPreferenceCyclic.loc[j, k] = weekday
                            df_patientPreferenceCyclic.loc[j+1, k] = slots[slot]["Name"]
                            k += 1
                        l += 1
                w += 1
                
            j += 2
                            
        with pd.ExcelWriter(file_path, mode="a", if_sheet_exists="replace", engine="openpyxl") as writer:
            df_patientPreferenceCyclic.to_excel(writer, sheet_name=f"Pacientes|Ciclo", index=False)
        
        all_weekDays = ["Seg", "Ter", "Qua", "Qui", "Sex"]
        df_staffPreferenceCyclic = pd.DataFrame(columns = ["ID", "Nome"])
        j = 1
        random.shuffle(names_researchers)
        isFirst = True
        for name in names_researchers:
            if not isFirst:
                k = 4
                
                df_staffPreferenceCyclic.loc[j, "ID"] = simplifyString(name)
                df_staffPreferenceCyclic.loc[j, "Nome"] = name
                df_staffPreferenceCyclic.loc[j+1, " "] = " "
                slot = random.choice(list(slots.keys()))
                day = random.choice(["Seg", "Ter", "Qua", "Qui", "Sex"])
                for w in range(5):
                    if all_weekDays[w] == day:
                        df_staffPreferenceCyclic.loc[j, k] = all_weekDays[w]
                    else:
                        df_staffPreferenceCyclic.loc[j, k] = all_weekDays[w]
                        df_staffPreferenceCyclic.loc[j+1, k] = slot
                    k += 1
            else:
                isFirst = False
        
            j += 2
        random.shuffle(names_physio)
        isFirst = True
        for name in names_physio:
            if not isFirst:
                k = 4
                
                df_staffPreferenceCyclic.loc[j, "ID"] = simplifyString(name)
                df_staffPreferenceCyclic.loc[j, "Nome"] = name
                df_staffPreferenceCyclic.loc[j+1, " "] = " "
                slot = random.choice(list(slots.keys()))
                day = random.choice(["Seg", "Ter", "Qua", "Qui", "Sex"])
                for w in range(5):
                    if all_weekDays[w] == day:
                        df_staffPreferenceCyclic.loc[j, k] = all_weekDays[w]
                    else:
                        df_staffPreferenceCyclic.loc[j, k] = all_weekDays[w]
                        df_staffPreferenceCyclic.loc[j+1, k] = slot
                    k += 1
            else:
                isFirst = False
        
            j += 2
            
        with pd.ExcelWriter(file_path, mode="a", if_sheet_exists="replace", engine="openpyxl") as writer:
            df_staffPreferenceCyclic.to_excel(writer, sheet_name=f"Pessoal|Ciclo", index=False)
        
        ##specific preferences
        print("sheet days")
        df_patientPreference = pd.DataFrame(columns = ["ID", "Nome"])
        j = 1
        for patient in patients.keys():
            k = 4
            df_patientPreference.loc[j, "ID"] = patient
            df_patientPreference.loc[j, "Nome"] = patients[patient]["Name"]
            df_patientPreference.loc[j+1, " "] = " "
            for day in planningHorizon:
                if random.random() < patientUnavailabilityPreference[i]:
                    if random.random() > patientUnavailabilitySlot[i]:
                        df_patientPreference.loc[j, k] = day
                        df_patientPreference.loc[j+1, k] = random.choice(list(slots.keys()))
                    else:
                        df_patientPreference.loc[j, k] = day
                    k += 1
            j += 2
        
        with pd.ExcelWriter(file_path, mode="a", if_sheet_exists="replace", engine="openpyxl") as writer:
            df_patientPreference.to_excel(writer, sheet_name=f"Pacientes|Dias", index=False)
            
        df_staffPreference = pd.DataFrame(columns = ["ID", "Nome"])
        j = 1
        for name in all_staffNames:
            k = 4
            df_staffPreference.loc[j, "ID"] = simplifyString(name)
            df_staffPreference.loc[j, "Nome"] = name
            df_staffPreference.loc[j+1, " "] = " "
            for day in planningHorizon:
                if day in holydays[i]:
                    df_staffPreference.loc[j, k] = day
                    k += 1
                else:
                    if random.random() < staffUnavailabilityPreference[i]:
                        if random.random() > patientUnavailabilitySlot[i]:
                            df_staffPreference.loc[j, k] = day
                            df_staffPreference.loc[j+1, k] = random.choice(list(slots.keys()))
                        else:
                            df_staffPreference.loc[j, k] = day
                        k += 1
            j += 2
        
        with pd.ExcelWriter(file_path, mode="a", if_sheet_exists="replace", engine="openpyxl") as writer:
            df_staffPreference.to_excel(writer, sheet_name=f"Pessoal|Dias", index=False)
        
        
        
##now, we are creating rescheduling examples
if reschedule:
    for i in range(len(instances)):
        
        file_path = f"eg.schedule.{instances[i]}.ot.xlsx"
        file_path_reschedule = f"eg.schedule.{instances[i]}.rs.xlsx"
        
        shutil.copyfile(file_path, file_path_reschedule)
        
        print(f"------ generating reschedule instance {instances[i]}")
        df_patients = pd.read_excel(file_path_reschedule, sheet_name="Pacientes", dtype = str).dropna(how='all')
        df_sysEsc = pd.read_excel(file_path_reschedule, sheet_name="sysEsc", dtype = str).dropna(how='all')
        df_patientSlotsDays = pd.read_excel(file_path_reschedule, sheet_name="Pacientes|Dias", dtype = str).dropna(how='all')
        
        N_i_limit = df_patientSlotsDays.shape[1]
        
        ###selects random appointments -> if they must be rescheduled, the whole day is consider as not available for the patient
        for j in range(numberOfPacients[i]):
            for k in range(10):
                if random.random() < 1/20:
                    df_patients.loc[j, f"Sessão {sessions_userNames[k]}"] = ""
                    day = df_sysEsc.loc[j, f"SD0{k}"]
                    df_patientSlotsDays.loc[i*2, N_i_limit+k] = day
            for k in range(1,3):
                if random.random() < 1/20:
                    df_patients.loc[j, f"Follow {(k*90)}"] = ""
                    day = df_sysEsc.loc[j, f"FD0{(k-1)}"]
                    df_patientSlotsDays.loc[i*2, N_i_limit+10+k] = day
        
        with pd.ExcelWriter(file_path_reschedule, mode="a", if_sheet_exists="replace", engine="openpyxl") as writer:
            df_patients.to_excel(writer, sheet_name=f"Pacientes", index=False)
        with pd.ExcelWriter(file_path_reschedule, mode="a", if_sheet_exists="replace", engine="openpyxl") as writer:
            df_patientSlotsDays.to_excel(writer, sheet_name=f"Pacientes|Dias", index=False)