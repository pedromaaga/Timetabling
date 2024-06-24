# Main

## Import files
from Libraries import *
from InterfaceClass import TimetablingApp

print("---------------------------------------")
print("\tTIMETABLING PROGRAM")
print("---------------------------------------")
print("\t Process interface")

root = tk.Tk()
app = TimetablingApp(root)
root.mainloop()

menu_option = 2

while menu_option != 2:
    menu_option = 2

print("---------------------------------------")
print("-> End program")
print("---------------------------------------")
## Write in the Excel file the results
