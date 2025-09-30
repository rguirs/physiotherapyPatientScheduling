import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from globalConsts import LANGUAGE

def validatorSimple(staff, patients, N_i, N_pf, schedule): # it doesnt consider the initial day
    
    staffBusy = {}
    for member in staff:
        staffBusy[member] = []

    patientBusy = {}
    for patient in patients:
        patientBusy[patient] = []

    
    for patient in patients:

        researcher = patients[patient]["researcher"]
        physio = patients[patient]["physio"]

        ##sessions
        for i in range(0,10):

            if schedule[patient][f"SD0{i}"] != None:

                if i > 0:
                    dist = schedule[patient][f"SD0{i}"] - schedule[patient][f"SD0{i-1}"]
                    if dist.days <= 4:
                        print(dist.days)


                thePair = [schedule[patient][f"SD0{i}"], schedule[patient][f"SH0{i}"]]

                if not N_i[patient][thePair[0]][thePair[1]]:
                    print("preference patient", patient, thePair)

                if thePair in patientBusy[patient]:
                    print("!!!!overscheduling patiend",patient,thePair, patients[patient]["Name"])
                patientBusy[patient].append(thePair)

                if i in [0, 9]:


                    if not N_pf[researcher][thePair[0]][thePair[1]]:
                        print("preference researcher", researcher, thePair)

                    if thePair in staffBusy[researcher]:
                        print("!!!!overscheduling researcher",researcher,thePair)
                    staffBusy[researcher].append(thePair)
                else:
                    
                    if not N_pf[physio][thePair[0]][thePair[1]]:
                        print("preference physio", physio, thePair)

                    if thePair in staffBusy[physio]:
                        print("!!!!overscheduling physio",physio,thePair)
                    staffBusy[physio].append(thePair)


        #follows
        for i in range(0,2):

            if schedule[patient][f"FD0{i}"] != None:

                dist = schedule[patient][f"FD0{i}"] - schedule[patient][f"SD00"]
                if dist.days <= 15:
                    print("f",dist.days)


                thePair = [schedule[patient][f"FD0{i}"], schedule[patient][f"FH0{i}"]]
                
                if not N_i[patient][thePair[0]][thePair[1]]:
                    print("preference patient", patient, thePair)

                if thePair in patientBusy[patient]:
                    print("!!!!overscheduling patiend",patient,thePair, patients[patient]["Name"])
                patientBusy[patient].append(thePair)
                
                if not N_pf[researcher][thePair[0]][thePair[1]]:
                    print("preference researcher", researcher, thePair)

                if thePair in staffBusy[researcher]:
                    print("!!!!overscheduling researcher",researcher,thePair)
                staffBusy[researcher].append(thePair)

    print("OK")