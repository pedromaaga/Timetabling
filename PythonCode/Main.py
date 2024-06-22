# Main

## Import files
from StoreDataFunctions import CreatSlots, Excelfile2Dataframe, CreateObjectAssignments, OtherConditions
from OtherFunctions import menuOptions, select_excel_file
from OptimizationFunctions import *

print("---------------------------------------")
print("\tTIMETABLING PROGRAM")
print("---------------------------------------")
print("\t Process interface")

menu_option = menuOptions()

while menu_option != 2:
    # Excel file
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
        print("\n-> Running the optimization program  (...)")
        TimeTabling = runOptimizationProgram(assignments, max_iterations, tabu_list_size, num_runs, other_conditions)
        print("\tProgram completed!")
        print("\n-> Results")
        PlotResults(TimeTabling, other_conditions)
    
    menu_option = menuOptions()

print("---------------------------------------")
print("-> End program")
print("---------------------------------------")
## Write in the Excel file the results
