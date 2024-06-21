from Classes import *
from OtherFunctions import *

# Functions to read the excel content

def Excelfile2Dataframe(excel_file):
    columns = ['ID', 'Assignment', 'Type', 'Priority', 'Quantity per week', 'Specific slot time?', 'Task Time [min]', 'ID Period', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

    df = pd.read_excel(excel_file, skiprows=10, usecols=columns)
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

def StoreSetSlot(days_assignment, times_assignment, all_slots, assignment):

    possible_slots = {}
    interval = timedelta(minutes=assignment.iloc[0, assignment.columns.get_loc('Task Time [min]')])
    jj = 1

    for i in range(len(times_assignment)):
        slots_inside = []

        assignment_start, assignment_end = times_assignment[i].split(' - ')
        initial_time_task = datetime.strptime(assignment_start, '%H:%M')
        end_time_task = datetime.strptime(assignment_end, '%H:%M')

        for index_s in all_slots:
            s = all_slots[index_s]
            time_start_s = datetime.strptime(s['start'], '%H:%M')
            time_end_s = datetime.strptime(s['end'], '%H:%M')

            if (initial_time_task <= time_start_s < end_time_task) and (initial_time_task < time_end_s <= end_time_task) and s['day'] == days_assignment[i]:
                slots_inside.append(index_s)

        for index_s in slots_inside:
            s = all_slots[index_s]
            time_start_s = datetime.strptime(s['start'], '%H:%M')
            time_end_s = datetime.strptime(s['end'], '%H:%M')

            current_time = time_start_s + interval

            if current_time > end_time_task:
                break

            j = index_s
            list_slots = []
            while time_end_s <= current_time:
                s = all_slots[j]
                time_end_s = datetime.strptime(s['end'], '%H:%M')
                list_slots.append(j)
                j += 1
            
            possible_slots[jj] = {'day': days_assignment[i], 'Time start': time_start_s.strftime('%H:%M'), 'Time end': current_time.strftime('%H:%M'),'set': list_slots}
            jj += 1

    return possible_slots

def StorePeriods(assignment,all_slots):
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

        set_slots = StoreSetSlot(days_assignment, times_assignment, all_slots, assignment)

        period_object = Periods(id, set_slots)
        periods_list.append(period_object)

    return periods_list

def CreateObjectAssignments(df_assignments,all_slots):
    assignment_list = []

    for assignment in df_assignments:
        id = assignment.iloc[0, assignment.columns.get_loc('ID')]
        name = assignment.iloc[0, assignment.columns.get_loc('Assignment')]
        type = assignment.iloc[0, assignment.columns.get_loc('Type')]
        priority = assignment.iloc[0, assignment.columns.get_loc('Priority')]
        qnt_week = assignment.iloc[0, assignment.columns.get_loc('Quantity per week')]
        specific_slottime = assignment.iloc[0, assignment.columns.get_loc('Specific slot time?')]
        task_time = assignment.iloc[0, assignment.columns.get_loc('Task Time [min]')]
        periods = StorePeriods(assignment,all_slots)

        assignment_object = Assignment(id,name,type,priority,qnt_week,specific_slottime,task_time,periods)
        assignment_list.append(assignment_object)

    return assignment_list

def CreatSlots(wake_time, sleep_time, delta_time):

    slot_index = 0
    slots = {}
    days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    for index, day in enumerate(days):
        
        initial_time = datetime.strptime(wake_time[index], '%H:%M')
        end_time = datetime.strptime(sleep_time[index], '%H:%M')

        interval = timedelta(minutes=delta_time)

        current_time = initial_time
        while current_time < end_time:
            slot_index += 1
            slots[slot_index] = {'day': day, 'start': current_time.strftime('%H:%M'), 'end': (current_time+interval).strftime('%H:%M')}
            current_time += interval

    return slots

def OtherConditions(excel_file):
    conditions = []
    df_conditions = pd.read_excel(excel_file, header=None, skiprows=13, nrows=5, usecols="Y")
    for index, row in df_conditions.iterrows():
        if pd.notnull(row.iloc[0]):
            conditions.append(row.iloc[0])
    return conditions