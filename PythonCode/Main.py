# Main

# Import files
from Libraries import *
from StoreDataFunctions import *
from Classes import *

# Read input table
excel_file = 'C:\\Users\\pedro\\OneDrive\\Documentos\\Projects\\Timetabling\\InputTable.xlsx'
df_assignments = DataFrameData(excel_file)
assignments = CreateObjectAssignments(df_assignments)

# Think about how to do the optimization