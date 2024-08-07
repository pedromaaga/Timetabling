from Libraries import *

# Other functions
def MinutesAvailableBetween2Times(time_start, time_final):
    hours_start, minutes_start = map(int, time_start.split(':'))
    hours_final, minutes_final = map(int, time_final.split(':'))

    return (hours_final * 60 + minutes_final) - (hours_start * 60 + minutes_start)

def time_to_minutes(time_str):
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes

def day_to_number(day):
    days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    return days_of_week.index(day)

def getStartPossiblePeriod(assignment):

    period_scheduled = {}

    # Select a period id at random
    id_period = random.choice(range(0,len(assignment.periods)))
    available_times = assignment.periods[id_period].available

    # Select the days that happens the activity
    days = []
    for index_time in available_times:
        time = available_times[index_time]
        days.append(time['day'])
    days = list(set(days))

    
    days = random.sample(days, k=int(assignment.qnt_week))

    # Select slots for each day that satisfy the 2 previous conditions 
    for i, day in enumerate(days, start=1):
        list_available_dailyperiod = []
        for index_time in available_times:
            time = available_times[index_time]
            if time['day'] == day:
                list_available_dailyperiod.append(index_time)

        # Select random a period available in that day
        period_scheduled[i] = available_times[random.choice(list_available_dailyperiod)]
    
    # Arange the period schedule in the week days sequence
    period_scheduled_order = dict(sorted(period_scheduled.items(), key=lambda item: day_to_number(item[1]['day'])))

    i = 0
    for index in period_scheduled_order:
        i += 1
        period_scheduled[i] = period_scheduled_order[index]

    return period_scheduled

def getWeekDistribution(assignments):
    # Define the days of the week
    days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    day_index_map = {day: idx for idx, day in enumerate(days_of_week)}
    
    # Initialize assignments count per day
    assignments_a_day = [0] * 7
    
    # Count assignments for each day
    for assignment in assignments:
        time_scheduled = assignment.period_scheduled
        for index in time_scheduled:
            day_assignment = time_scheduled[index]['day']
            if day_assignment in day_index_map:
                assignments_a_day[day_index_map[day_assignment]] += 1
                
    return assignments_a_day

def adjustAssignmentsWeek(assignments):
    
    days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    assignments_dict = {day: [] for day in days_of_week}

    for assignment in assignments:
        time_scheduled = assignment.period_scheduled
        for index in time_scheduled:
            name_assignment = assignment.name
            day_assignment = time_scheduled[index]['day']
            start_assignment = time_scheduled[index]['Time start']
            end_assignment = time_scheduled[index]['Time end']

            assignments_dict[day_assignment].append({
                'name': name_assignment,
                'Time start': start_assignment,
                'Time end': end_assignment
            })
    
    # Ordenar as atribuições dentro de cada dia pelo horário de início
    for day in assignments_dict:
        assignments_dict[day].sort(key=lambda x: x['Time start'])

    return assignments_dict

def sortSolution(time_scheduled):
    week_days_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    sorted_data = sorted(time_scheduled.items(), key=lambda item: (week_days_order.index(item[1]['day']),time_to_minutes(item[1]['Time start'])))

    sorted_data = {i + 1: item[1] for i, item in enumerate(sorted_data)}

    return sorted_data
