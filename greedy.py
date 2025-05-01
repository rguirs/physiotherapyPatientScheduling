import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from globalConsts import LANGUAGE

def greedy(initialDay, planningHorizon, slots, staff, patients, N_i, N_pf, schedule):
    
    s = False
    
    #get patients that doesn't have an associated researcher/fisio
    print("---------- generating patient queue") if LANGUAGE == "en" else print("----- definindo fila de pacientes")
    notAssignedPatients = []
    assignedPatients = []
    for patient in patients.keys():
        if patients[patient]["researcher"] is None or patients[patient]["physio"] is None or schedule[patient]["SD00"] is None:
            notAssignedPatients.append(patient)
        else:
            assignedPatients.append(patient)
            
    #create two lists with researchers and physio separated
    all_researchers = []
    all_physio = []
    for staffMember in staff:
        if staff[staffMember]["Role"] == "A":
            all_researchers.append(staffMember)
        else:
            all_physio.append(staffMember)
    
    #we are going to prioritize the patients
    assignedPatients_sessions, assignedPatients_follows = orderPatients(schedule, assignedPatients)
    
    #schedule the follow-ups of those with the a researcher and physio designated
    print("---------- rescheduling follow-ups") if LANGUAGE == "en" else print("----- re-agendando follow-ups")
    total = 0
    for follow in range(1,-1,-1):
        for patient in assignedPatients_follows[follow]:
            researcher = patients[patient]["researcher"]
            physio = patients[patient]["physio"]
            if not (researcher is None or physio is None):
                total += 1
    total = 1 if total < 1 else total
    done = 0
    for follow in range(1,-1,-1):
        for patient in assignedPatients_follows[follow]:
            print("---------- rescheduling follow-ups") if LANGUAGE == "en" else print(f"----- reagendando follow-ups: {done/total}")
            researcher = patients[patient]["researcher"]
            physio = patients[patient]["physio"]
            if not (researcher is None or physio is None):
                E_researcher, E_physio = generateE(N_i, N_pf, patient, researcher, physio, slots, planningHorizon)
                s, schedule, N_pf = scheduleFollow(N_pf, slots, planningHorizon, patient, researcher, schedule, follow, E_researcher, isReschedule = True)
                if not s:
                    print(f"Unable to assign a new follow-up (the one {90*(follow+1)} days after the beginning) for {patients[patient]['Nome']}") if LANGUAGE == "en" else print(f"Incapaz de definir um novo follow up (após {90*(follow+1)} dias) para paciente {patients[patient]['Nome']}")
                    exit()
                else:
                    done += 1
    done = total
    print(f"---------- rescheduling follow-ups: {done/total}") if LANGUAGE == "en" else print(f"----- reagendando follow-ups: {done/total}")
                    
    #schedule the sessions of those with a staff defined
    print("---------- rescheduling sessions") if LANGUAGE == "en" else print("----- reagendando sessões")
    total = 0
    for session in range(9, -1, -1):
        for patient in assignedPatients_sessions[session]:
            total += 1
    total = 1 if total < 1 else total
    done = 0
    for session in range(9, -1, -1):
        for patient in assignedPatients_sessions[session]:
            print(f"----- rescheduling sessions: {done/total}") if LANGUAGE == "en" else print(f"----- reagendando sessões: {done/total}")
            researcher = patients[patient]["researcher"]
            physio = patients[patient]["physio"]
            
            E_researcher, E_physio = generateE(N_i, N_pf, patient, researcher, physio, slots, planningHorizon)
            s, schedule, N_pf = scheduleSession(N_pf, slots, planningHorizon, patient, researcher, physio, initialDay, schedule, session, E_researcher, E_physio, isReschedule = True)
            if not s:
                print(f"Unable to assign a new session (Session number {(session+1)}) for {patients[patient]['Name']}. The person responsible: researcher ({patients[patient]['researcher']}) and physio ({patients[patient]['physio']})") if LANGUAGE == "en" else print(f"Incapaz de definir uma nova sessão (Sessão número {(session+1)}) para paciente {patients[patient]['Name']}. Responsáveis por paciente: pesquisadorx ({patients[patient]['researcher']}) e fisio ({patients[patient]['physio']})")
                exit()
            else:
                done += 1
    done = total
    print(f"----- rescheduling sessions: {done/total}") if LANGUAGE == "en" else print(f"----- reagendando sessões: {done/total}")
    
    #schedule the new patients
    print("---------- scheduling new patients") if LANGUAGE == "en" else print("----- agendando novos pacientes")
    total = 0
    for patient in notAssignedPatients:
        total += 1
    total = 1 if total < 1 else total
    done = 0
    random.shuffle(notAssignedPatients)
    for patient in notAssignedPatients:
        print(f"----- scheduling new patients: {done/total}") if LANGUAGE == "en" else print(f"----- agendando novos pacientes: {done/total}")
        for interval in range(0, len(planningHorizon)-150, 2):
            s, patients, schedule, N_pf = assignStaff(N_pf, N_i, patients, patient, all_researchers, all_physio, schedule, slots, planningHorizon, initialDay+timedelta(days=interval))
            if s:
                break
        if not s:
            print(f"Unable to schedule the patient {patients[patient]['Name']}") if LANGUAGE == "en" else print(f"Incapaz de agenda paciente com nome {patients[patient]['Name']}")
            exit()
        else:
            done += 1
    done = total
    print(f"----- scheduling new patients: {done/total}") if LANGUAGE == "en" else print(f"----- agendando novos pacientes: {done/total}")
            
    return s, patients, schedule, N_pf
    
#it is used to make the greedy algorithm faster, so the available slots are quickly found
def generateE(N_i, N_pf, patient, researcher, physio, slots, planningHorizon):
    
    E_researcher = {}
    E_physio = {}
    for day in planningHorizon:
        E_researcher[day] = {}
        E_physio[day] = {}
        for slot in slots.keys():
            E_researcher[day][slot] = N_i[patient][day][slot] and N_pf[researcher][day][slot]
            E_physio[day][slot] = N_i[patient][day][slot] and N_pf[physio][day][slot]
                
    return E_researcher, E_physio
    
def scheduleFollow(N_pf, slots, planningHorizon, patient, researcher, schedule, followUpNum, E_researcher, isReschedule = False):
    s = False
    bestDay = schedule[patient]["SD00"] + timedelta(days=90*(followUpNum+1))
    
    #defines a range (set) of the best days (in order of "hardcoded preference") to assign the patient
    triesDays = [bestDay]
    for i in range(1, 15):
        nextOption = bestDay + timedelta(days=i)
        triesDays.append(nextOption)
        nextOption = bestDay - timedelta(days=i)
        triesDays.append(nextOption)
    if isReschedule: #extends the range to a wider number of days if rescheduling is happening
        for i in range(15, 105):
            nextOption = bestDay + timedelta(days=i)
            triesDays.append(nextOption)
        
    for day in triesDays:
        s, possible_slots = trySchedule(E_researcher, day, slots, planningHorizon)
        if s:
            slot = random.choice(possible_slots)
            schedule[patient][f"FD0{followUpNum}"] = day
            schedule[patient][f"FH0{followUpNum}"] = slot
            N_pf[researcher][day][slot] = False
            break
    
    return s, schedule, N_pf
    
def scheduleSession(N_pf, slots, planningHorizon, patient, researcher, physio, initialDay, schedule, sessionNum, E_researcher, E_physio, isReschedule = False):
    
    if sessionNum >= 10:
        return True, schedule, N_pf
    
    s = False
    
    if sessionNum == 0:
        bestDay = initialDay
    else:
        bestDay = schedule[patient][f"SD0{(sessionNum-1)}"] + timedelta(days=7)
        
    triesDays = [bestDay]
    for i in range(1, 4):
        nextOption = bestDay + timedelta(days=i)
        triesDays.append(nextOption)
        nextOption = bestDay - timedelta(days=i)
        triesDays.append(nextOption)
    for i in range(4, 14):
        nextOption = bestDay + timedelta(days=i)
        triesDays.append(nextOption)
    if isReschedule:
        for i in range(14, 104):
            nextOption = bestDay + timedelta(days=i)
            triesDays.append(nextOption)
            
    for day in triesDays:
        if sessionNum in [0, 9]:
            s, possible_slots = trySchedule(E_researcher, day, slots, planningHorizon)
        else:
            s, possible_slots = trySchedule(E_physio, day, slots, planningHorizon)
            
        if s:
            slot = random.choice(possible_slots)
            schedule[patient][f"SD0{sessionNum}"] = day
            schedule[patient][f"SH0{sessionNum}"] = slot
            if sessionNum in [0, 9]:
                N_pf[researcher][day][slot] = False
            else:
                N_pf[physio][day][slot] = False
               
            if sessionNum == 0:
                for follow in range(1,-1,-1):
                    s, schedule, N_pf = scheduleFollow(N_pf, slots, planningHorizon, patient, researcher, schedule, follow, E_researcher)
                    if not s:
                        N_pf, schedule = unschedule(schedule, patient, researcher, N_pf, "FD00", "FH00")
                        N_pf, schedule = unschedule(schedule, patient, researcher, N_pf, "FD01", "FH01")
                        break
                if not s:
                    N_pf, schedule = unschedule(schedule, patient, researcher, N_pf, "SD00", "SH00")
            
            if s:
                s, schedule, N_pf = scheduleSession(N_pf, slots, planningHorizon, patient, researcher, physio, initialDay, schedule, sessionNum+1, E_researcher, E_physio)
                
                if not s:
                    if sessionNum == 0:
                        N_pf, schedule = unschedule(schedule, patient, researcher, N_pf, "FD00", "FH00")
                        N_pf, schedule = unschedule(schedule, patient, researcher, N_pf, "FD01", "FH01")
                            
                    for session in range(sessionNum, 10):
                        if session in [0, 9]:
                            N_pf, schedule = unschedule(schedule, patient, researcher, N_pf, f"SD0{session}", f"SH0{session}")
                        else:
                            N_pf, schedule = unschedule(schedule, patient, physio, N_pf, f"SD0{session}", f"SH0{session}")
                else:
                    break
    
    if not s:
        ##unschedule the following sessions
        for session in range(sessionNum, 10):
            if session in [0, 9]:
                N_pf, schedule = unschedule(schedule, patient, researcher, N_pf, f"SD0{session}", f"SH0{session}")
            else:
                N_pf, schedule = unschedule(schedule, patient, physio, N_pf, f"SD0{session}", f"SH0{session}")
            
        ##if needed, unschedule the follow-ups
        if sessionNum == 0:
            N_pf, schedule = unschedule(schedule, patient, researcher, N_pf, "FD00", "FH00")
            N_pf, schedule = unschedule(schedule, patient, researcher, N_pf, "FD01", "FH01")
    
    
    return s, schedule, N_pf
    
def unschedule(schedule, patient, staffMember, N_pf, nameTag_day, nameTag_slot):
    if schedule[patient][nameTag_day]:
        day = schedule[patient][nameTag_day]
        slot = schedule[patient][nameTag_slot]
        N_pf[staffMember][day][slot] = True
        schedule[patient][nameTag_day] = None
        schedule[patient][nameTag_slot] = None
    return N_pf, schedule
    
def trySchedule(E, day, slots, planningHorizon):
    possible_slots = []
    if day.weekday() < 5 and day in planningHorizon:
        for slot in slots.keys():
            if E[day][slot]:
                possible_slots.append(slot)
    return len(possible_slots) > 0, possible_slots
    
def assignStaff(N_pf, N_i, patients, patient, all_researchers, all_physio, schedule, slots, planningHorizon, initialDay):
    
    random.shuffle(all_researchers)
    random.shuffle(all_physio)
    
    s = False
    for researcher in all_researchers:
        for physio in all_physio:
            E_researcher, E_physio = generateE(N_i, N_pf, patient, researcher, physio, slots, planningHorizon)
            s, schedule, N_pf = scheduleSession(N_pf, slots, planningHorizon, patient, researcher, physio, initialDay, schedule, 0, E_researcher, E_physio)
            if s:
                patients[patient]["researcher"] = researcher
                patients[patient]["physio"] = physio
                break
        if s:
            break
            
    if not s:
        patients[patient]["researcher"] = None
        patients[patient]["physio"] = None
    
    return s, patients, schedule, N_pf
    
def orderPatients(schedule, ids):
    
    unscheduledPatientsByNumberOfScheduledSessions = {sessionName: [] for sessionName in range(10)}
    unscheduledPatientsByFollowups = {followupName: [] for followupName in range(2)}
    
    for patient in ids:
        for session in range(10):
            if schedule[patient][f"SD0{session}"] is None:
                unscheduledPatientsByNumberOfScheduledSessions[session].append(patient)
                break
        for follow in range(2):
            if schedule[patient][f"FD0{follow}"] is None:
                unscheduledPatientsByFollowups[follow].append(patient)
    
    for session in range(10):
        random.shuffle(unscheduledPatientsByNumberOfScheduledSessions[session])
    for follow in range(2):
        random.shuffle(unscheduledPatientsByFollowups[follow])
        
    return unscheduledPatientsByNumberOfScheduledSessions, unscheduledPatientsByFollowups