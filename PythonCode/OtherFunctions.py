from Libraries import *

# Other functions

def MinutesAvailableBetween2Times(time_start, time_final):
    hours_start, minutes_start = map(int, time_start.split(':'))
    hours_final, minutes_final = map(int, time_final.split(':'))

    return (hours_final * 60 + minutes_final) - (hours_start * 60 + minutes_start)

def day_to_number(day):
    days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    return days_of_week.index(day)

def getNewPossiblePeriod(assignment):

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



    