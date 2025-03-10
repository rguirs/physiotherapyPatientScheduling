'''
NEEDS TO SEPARATE THE SCHEDULING AND RESCHEDULING
'''

from globalConsts import LANGUAGE

def runInstance(instance, isInstanceReschedule):


    nameOfFile = f"./examples/eg.schedule.{instance}"
    FILE_PATH = f"{nameOfFile}.xlsx"
    FILE_PATH_OUT = f"{nameOfFile}.m.ot.xlsx"

    dateStarts = ["01/01/2023", "01/01/2024", "01/01/2025", "01/01/2024", "01/01/2023", "01/01/2023"]
    dateEnds =   ["31/07/2024", "31/12/2024", "31/12/2025", "31/12/2025", "31/12/2025", "31/12/2025"]


    print("---------- READING EXCEL FILE") if LANGUAGE == "en" else print("---------- LENDO ARQUIVO EXCEL")
    dateStart = pd.to_datetime(dateStarts[instance-1], format="%d/%m/%Y")
    dateEnd = pd.to_datetime(dateEnds[instance-1], format="%d/%m/%Y")

    CURRENT_DAY = dateStart.strftime('%d/%m/%Y') #datetime.today().strftime('%d/%m/%Y')

    