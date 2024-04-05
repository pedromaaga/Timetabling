# Main

# Import files
from StoreDataFunctions import *
from Classes import *
from OtherFunctions import *
from OptimizationFunctions import *

# Input Parameters - Vai ser coisa do excel, depois implementar
delta_time = 10            # [minutes] Time minimum of the grid

wake_time = ['6:00','6:00','6:00','6:00','6:00','6:00','6:00']
sleep_time = ['20:00','20:00','20:00','20:00','20:00','20:00','20:00']

initial_temperature = 1000
cooling_rate = 0.99
max_iterations = 20000
num_runs = 5

# Create time slots
all_slots = CreatSlots(wake_time,sleep_time,delta_time)

# Read assignments from excel file
excel_file = 'C:\\Users\\pedro\\OneDrive\\Documentos\\Projects\\Timetabling\\InputTable.xlsx'
df_assignments = DataFrameData(excel_file)
assignments = CreateObjectAssignments(df_assignments,all_slots)


# Think about how to do the optimization
TimeTabling = runOptimizationProgram(assignments, initial_temperature, cooling_rate, max_iterations, num_runs)

Z, overview = ObjectiveFunction(TimeTabling)
print(Z)
for overview_HC in overview:
    
    for string in overview_HC:
        print(string)
    print('\n')