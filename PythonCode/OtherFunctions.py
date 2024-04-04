from Libraries import *

# Other functions

def MinutesAvailableBetween2Times(time_start, time_final):
    hours_start, minutes_start = map(int, time_start.split(':'))
    hours_final, minutes_final = map(int, time_final.split(':'))

    return (hours_final * 60 + minutes_final) - (hours_start * 60 + minutes_start)

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

def AssociatePeriodToSlot(id, days_assignment, times_assignment, all_slots, assignment):

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
            
            possible_slots[jj] = {'ID': id, 'day': days_assignment[i], 'set': list_slots}
            jj += 1

    return possible_slots