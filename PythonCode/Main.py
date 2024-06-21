# Main

## Import files
from StoreDataFunctions import *
from Classes import *
from OtherFunctions import *
from OptimizationFunctions import *

## Input Parameters
# Excel file
excel_file = 'C:\\Users\\pedro\\OneDrive\\Documentos\\Projects\\Timetabling\\InputTable.xlsx'

# Parameters of the optimization program
wake_time, sleep_time, delta_time, tabu_list_size, max_iterations, num_runs = ParametersOptimizationProgram(excel_file)
other_conditions = OtherConditions(excel_file)

# Create time slots
all_slots = CreatSlots(wake_time,sleep_time,delta_time)

# Read assignments from excel file
df_assignments = Excelfile2Dataframe(excel_file)
assignments = CreateObjectAssignments(df_assignments,all_slots)

## Optimization program
TimeTabling = runOptimizationProgram(assignments, max_iterations, tabu_list_size, num_runs, other_conditions)
PlotResults(TimeTabling, other_conditions)

## Write in the Excel file the results
