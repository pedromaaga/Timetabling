# Main

## Import files
from StoreDataFunctions import *
from Classes import *
from OtherFunctions import *
from OptimizationFunctions import *

## Input Parameters
# Excel file
print("\n\n------------------------------------------------------")
print("\t\tTimeTabling program")
print("------------------------------------------------------")
print("\n-> Select the excel file")
excel_file = select_excel_file()

if excel_file != None:
    print("\tExcel file selected!")
    print(f"\tName: {os.path.basename(excel_file)}")

    # Parameters of the optimization program
    print("\n-> Reading the data  (...)")
    wake_time, sleep_time, delta_time, tabu_list_size, max_iterations, num_runs = ParametersOptimizationProgram(excel_file)
    other_conditions = OtherConditions(excel_file)

    # Create time slots
    all_slots = CreatSlots(wake_time,sleep_time,delta_time)

    # Read assignments from excel file
    df_assignments = Excelfile2Dataframe(excel_file)
    assignments = CreateObjectAssignments(df_assignments,all_slots)
    print("\tData read!")
    ## Optimization program
    print("\n-> Running the optimization program (...)")
    TimeTabling = runOptimizationProgram(assignments, max_iterations, tabu_list_size, num_runs, other_conditions)
    print("\tProgram completed!")
    print("\n-> Results")
    PlotResults(TimeTabling, other_conditions)

print("\n------------------------------------------------------")
print("-> End program")
print("------------------------------------------------------")
## Write in the Excel file the results
