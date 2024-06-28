# Main

## Import files
from Libraries import *
from InterfaceClass import TimetablingApp
from OptimizationFunctions import PlotResults

print("---------------------------------------")
print("\tTIMETABLING PROGRAM")
print("---------------------------------------")
print("\t Process interface")

root = ctk.CTk()
app = TimetablingApp(root)
root.mainloop()

if app.timetabling != None:
    PlotResults(app.timetabling, app.other_conditions)
print("---------------------------------------")
print("-> End program")
print("---------------------------------------")
## Write in the Excel file the results
