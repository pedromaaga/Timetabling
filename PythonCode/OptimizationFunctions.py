from OtherFunctions import *

### Optimization functions

## Main functions
def runOptimizationProgram(assignments, max_iterations, tabu_list_size, num_runs):

    if IsThereNeighboors(assignments):
        best_solution = RunTabuMultipleTimes(assignments, max_iterations, tabu_list_size, num_runs)    
    else:
        best_solution = GenerateInitialSolution(assignments)

    return best_solution

def TabuAlgorithm(assignments, max_iterations, tabu_list_size):
    # 1 - Generate initial solution
    current_solution = GenerateInitialSolution(assignments)
    # 2 - Update the best solution
    best_solution = current_solution
    # 3 - Start Tabu list
    tabu_list = []

    for i in range(max_iterations):
        # 4 - Generate a neighbour from the current solution
        neighboors_solution = GenerateNeighborhood(current_solution)

        # 5 - Initialize best_neighbor and best_neighbor_obj
        best_neighbor = None
        best_neighbor_obj = float('inf')  # Initialize with a high value

        # Evaluate neighborhoods and select the best non-tabu solution
        for neighbor in neighboors_solution:
            if neighbor not in tabu_list:  # Check if neighbor is not in tabu list
                obj_value, _ = ObjectiveFunction(neighbor)
                if obj_value < best_neighbor_obj:
                    best_neighbor = neighbor
                    best_neighbor_obj = obj_value

        # 6 - Evaluate
        # Update current_solution and best_solution
        if best_neighbor is not None:
            current_solution = best_neighbor
            best_cost, _ = ObjectiveFunction(best_solution)
            if best_neighbor_obj < best_cost:
                best_solution = best_neighbor
        
        # Update tabu list
        if best_neighbor is not None:
            tabu_list.append(best_neighbor)
            if len(tabu_list) > tabu_list_size:
                tabu_list.pop(0)  # Remove oldest entry from tabu list

    return best_solution

def RunTabuMultipleTimes(assignments, max_iterations, tabu_list_size, num_runs):
    best_solution = None
    best_cost = float('inf')

    for _ in range(num_runs):
        current_solution = TabuAlgorithm(assignments, max_iterations, tabu_list_size)
        current_cost, _ = ObjectiveFunction(assignments)

        if current_cost < best_cost:
            best_solution = current_solution
            best_cost = current_cost

    return best_solution

## Functions to generate solutions
def GenerateNeighborhood(assignments):
    Neighbors = []

    for index, assignment in enumerate(assignments):
        for set_period in assignment.periods:
            available_times = set_period.available

            # Extract unique days from available times
            days = set(time['day'] for time in available_times.values())

            # Generate all possible combinations of required number of days
            days_combinations = combinations(days, int(assignment.qnt_week))

            for days_combination in days_combinations:
                all_daily_periods = []
                for day in days_combination:
                    list_available_dailyperiod = [index_time for index_time, time in available_times.items() if time['day'] == day]
                    all_daily_periods.append(list_available_dailyperiod)

                # Generate the period for each combination of periods
                periods_combinations = list(itertools.product(*all_daily_periods))
                for periods in periods_combinations:
                    period_scheduled = {}
                    for i, p in enumerate(periods, start=1):
                        period_scheduled[i] = available_times[p]

                    # Arrange the period schedule in the week days sequence
                    period_scheduled = dict(sorted(period_scheduled.items(), key=lambda item: day_to_number(item[1]['day'])))

                    if period_scheduled != assignment.period_scheduled:
                        new_solution = assignments.copy()
                        new_solution[index].period_scheduled = period_scheduled 
                        Neighbors.append(new_solution)
    
    return Neighbors

def GenerateInitialSolution(assignments):
    for assignment in assignments:
        period = getStartPossiblePeriod(assignment)
        assignment.period_scheduled = period
    return assignments

def IsThereNeighboors(assignments):

    for assignment in assignments:
        qnt_setslots = 0
        for i in range(0,len(assignment.periods)):
            qnt_setslots = qnt_setslots + len(assignment.periods[i].available)
        
        if qnt_setslots > assignment.qnt_week:
            return True

    return False

## Cost function
def ObjectiveFunction(assignments):
    # Weights
    W_HC = [1000, 2000]
    all_overview = []
    # Hard Constraints
    Z_HC_1, overviewHC1 = HardConstraint1(assignments)
    all_overview.append(overviewHC1)
    Z_HC_2, overviewHC2 = HardConstraint2(assignments)
    all_overview.append(overviewHC2)

    Z_HC = W_HC[0]*Z_HC_1 + W_HC[1]*Z_HC_2
    Z = Z_HC

    return Z, all_overview

## Constraint functions

# Hard constraints
# 1 - All assignments needs to be scheduled
def HardConstraint1(assignments):

    overviewHC1 = ['Overview Hard Constraint 1']
    sum = 0
    for assignment in assignments:
        if assignment.period_scheduled == 0:   # 0 is the default value
            overviewHC1.append(f'Violation - {assignment.name} is not scheduled')
            sum = sum + 1
    if sum == 0:
        overviewHC1.append('All assignments are scheduled.')
    
    return sum, overviewHC1

# 2 - Only one assignment must be scheduled in a specific set of slots
def HardConstraint2(assignments):

    overviewHC2 = ['Overview Hard Constraint 2']
    sum = 0
    for index, current_assignment in enumerate(assignments):
        slots_current_assignment = []
        for key, value in current_assignment.period_scheduled.items():
            slots_current_assignment.append(value['set'])
        
        for i in range(index+1,len(assignments)):
            slots_next_assignment = []
            next_assignment = assignments[i]
            for key, value in next_assignment.period_scheduled.items():
                slots_next_assignment.append(value['set'])

            # Check for overlap between sets
            flatten_slots_current = [slot for sublist in slots_current_assignment for slot in sublist]
            flatten_slots_next = [slot for sublist in slots_next_assignment for slot in sublist]
            
            qnt = 0
            for s_current in flatten_slots_current:
                for s_next in flatten_slots_next:
                    if s_next == s_current:
                        qnt = qnt + 1 

            if qnt > 1:
                overviewHC2.append(f'Violation: Overlapping slots between assignments {current_assignment.name} and {next_assignment.name}')
                sum += 1

    if sum == 0:
        overviewHC2.append('No overlapping intervals between assessments.')

    return sum, overviewHC2

# Soft constraints
# 1 - 

## Plot results

def PlotResults(TimeTabling):
    print('----------------')
    Z, overview = ObjectiveFunction(TimeTabling)

    print('------------------------------------------------------')
    print('---------------- Overview constraints ----------------')
    print(f'Objective Function = {Z}')
    for overview_HC in overview:
        print('')
        for string in overview_HC:
            print(string)
    print('------------------------------------------------------')
    print('-------------------- Timetabling ---------------------')
    for assignment in TimeTabling:
        print(f'Name: {assignment.name}')
        time_scheduled = assignment.period_scheduled
        for index in time_scheduled:
            time = time_scheduled[index]
            print(f'\tDay: {time['day']}\t Start: {time['Time start']}\t End: {time['Time end']}')


