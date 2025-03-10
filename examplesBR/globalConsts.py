LANGUAGE = "pt" ## "en" or "pt-br"

if LANGUAGE == "en":
    SHEET_PATIENTS = "Patients"
    FIELD_PATIENTS_ID = "ID"
    FIELD_PATIENTS_NAME = "Name"
    
    SHEET_PATIENTSDAYS = "Patients|DAYS"
    SHEET_PATIENTSCYCLIC = "Patients|Cycle"
    
    SHEET_STAFF = "Staff"
    FIELD_STAFF_ID = "ID"
    FIELD_STAFF_ROLE = "Role"
    ROLES_RESEARCHER = "Research"
    ROLES_PHYSIO = "Physio"
    FIELD_STAFF_NAME = "Name"
    
    SHEET_STAFFDAYS = "Staff|DAYS"
    SHEET_STAFFCYCLIC = "Staff|Cycle"
    SHEET_STAFFSCHEDULE = "SCHEDULE|"
    SHEET_SCHEDULEMAIN = "Schedule"
    
    SHEET_DEFSLOT = "DefSlot"
    FIELD_DEFSLOT_NAME = "Slot Name"
    FIELD_DEFSLOT_START = "Start Time"
    FIELD_DEFSLOT_END = "End Time"

    SESSION_NAME_FOR_USER = "Session"
    FOLLOW_NAME_FOR_USER = "Follow"
    SHEET_SYSESC = "sysEsc"
else:
    SHEET_PATIENTS = "Pacientes"
    FIELD_PATIENTS_ID = "ID"
    FIELD_PATIENTS_NAME = "Nome"

    SHEET_PATIENTSDAYS = "Pacientes|Dias"
    SHEET_PATIENTSCYCLIC = "Pacientes|Ciclo"
    
    SHEET_STAFF = "Pessoal"
    FIELD_STAFF_ID = "ID"
    FIELD_STAFF_ROLE = "Tipo"
    ROLES_RESEARCHER = "Pesquisa"
    ROLES_PHYSIO = "Fisioterapia"
    FIELD_STAFF_NAME = "Nome"

    SHEET_STAFFDAYS = "Pessoal|Dias"
    SHEET_STAFFCYCLIC = "Pessoal|Ciclo"
    SHEET_STAFFSCHEDULE = "ESCALA|"
    SHEET_SCHEDULEMAIN = "Escala"
    
    SHEET_DEFSLOT = "DefSlot"
    FIELD_DEFSLOT_NAME = "Nome Slot"
    FIELD_DEFSLOT_START = "Início Slot"
    FIELD_DEFSLOT_END = "Fim Slot"
    
    SESSION_NAME_FOR_USER = "Sessão"
    FOLLOW_NAME_FOR_USER = "Follow"
    SHEET_SYSESC = "sysEsc"