from Libraries import *
from Classes import *

# Functions for read the excel
def DataFrameData(excel_file):
    columns = ['ID', 'Assignment', 'Type', 'Priority', 'Quantity per week', 'Specific slot time?', 'Task Time [min]', 'ID Period', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

    df = pd.read_excel(excel_file, skiprows=2, usecols=columns)
    df.dropna(axis=0, how='all', inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Iterate over the rows of the DataFrame
    current_assignment = 1
    index_start = None
    index_end = None
    df_assignments = []

    for index, row in df.iterrows():
        if pd.notnull(row.iloc[0]):
            ID_assignment = row.iloc[0]
            
            if ID_assignment == current_assignment + 1:
                current_assignment = ID_assignment
                index_end = index
                if index_start != index_end:
                    df_assignment = df.iloc[index_start:index_end]
                else:
                    df_assignment = df.iloc[index_start]
                df_assignments.append(df_assignment)
            
            if ID_assignment == current_assignment:
                index_start = index

        if index == df.shape[0] - 1:
            index_end = index + 1
            if index_start != index_end:
                df_assignment = df.iloc[index_start:index_end]
            else:
                df_assignment = df.iloc[index_start]
            df_assignments.append(df_assignment)

    return df_assignments

def CreatePeriods(assignment):
    days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

    periods_list = []
    for index, row in assignment.iterrows():
        id = row.iloc[assignment.columns.get_loc('ID Period')]
        days_assignment = []
        times_assignment = []
        for day in days:
            if pd.notnull(row.iloc[assignment.columns.get_loc(day)]):
                days_assignment.append(day)
                times_assignment.append(row.iloc[assignment.columns.get_loc(day)])

        period_object = Periods(id,days_assignment,times_assignment)
        periods_list.append(period_object)
    return periods_list

def CreateObjectAssignments(df_assignments):
    
    assignment_list = []

    for assignment in df_assignments:
        id = assignment.iloc[0, assignment.columns.get_loc('ID')]
        name = assignment.iloc[0, assignment.columns.get_loc('Assignment')]
        type = assignment.iloc[0, assignment.columns.get_loc('Type')]
        priority = assignment.iloc[0, assignment.columns.get_loc('Priority')]
        qnt_week = assignment.iloc[0, assignment.columns.get_loc('Quantity per week')]
        specific_slottime = assignment.iloc[0, assignment.columns.get_loc('Specific slot time?')]
        task_time = assignment.iloc[0, assignment.columns.get_loc('Task Time [min]')]
        periods = CreatePeriods(assignment)

        assignment_object = Assignments(id,name,type,priority,qnt_week,specific_slottime,task_time,periods)
        assignment_list.append(assignment_object)

    return assignment_list