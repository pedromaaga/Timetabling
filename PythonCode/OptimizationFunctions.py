from OtherFunctions import getStartPossiblePeriod, getWeekDistribution, day_to_number, sortSolution
from Libraries import *

### Optimization functions

def ParametersOptimizationProgram(excel_file):
    # Store wake time and sleep time
    df_times = pd.read_excel(excel_file, header=None, skiprows=8, nrows=2, usecols="K:Q")
    df_times = df_times.apply(lambda x: x.map(lambda y: y.strftime('%H:%M')))
    wake_time = df_times.iloc[0].tolist()
    sleep_time = df_times.iloc[1].tolist()
    
    # Store technical parameters
    df_parameters = pd.read_excel(excel_file, header=None, skiprows=8, nrows=1, usecols="V:Y")
    tabu_list_size, max_iterations, num_runs, delta_time = df_parameters.iloc[0]

    return wake_time, sleep_time, delta_time, tabu_list_size, max_iterations, num_runs

## Main functions
def runOptimizationProgram(app, assignments, max_iterations, tabu_list_size, num_runs, other_conditions):

    if IsThereNeighboors(assignments):
        best_solution = RunTabuMultipleTimes(app, assignments, max_iterations, tabu_list_size, num_runs, other_conditions)    
    else:
        best_solution = GenerateInitialSolution(assignments)

    return best_solution

def TabuAlgorithm(assignments, max_iterations, tabu_list_size, other_conditions):
    # 1 - Generate initial solution
    current_solution = GenerateInitialSolution(assignments)
    # 2 - Update the best solution
    best_solution = current_solution
    # 3 - Start Tabu list
    tabu_list = []

    max_repetitions = int(0.1*max_iterations)
    if max_repetitions < 50:
        max_repetitions = 50

    repetition = 0
    old_best_cost = None

    for i in range(max_iterations):
        # 4 - Generate a neighbour from the current solution
        neighboors_solution = GenerateNeighborhood(current_solution)

        # 5 - Initialize best_neighbor and best_neighbor_obj
        best_neighbor = None
        best_neighbor_obj = float('inf')  # Initialize with a high value

        # Evaluate neighborhoods and select the best non-tabu solution
        for neighbor in neighboors_solution:
            if not equal_results(neighbor, [s['solution'] for s in tabu_list]):  # Check if neighbor is not in tabu list
                obj_value, _ = ObjectiveFunction(neighbor, other_conditions)
                if obj_value < best_neighbor_obj:
                    best_neighbor = neighbor
                    best_neighbor_obj = obj_value

        # 6 - Evaluate
        # Update current_solution and best_solution
        if best_neighbor is not None:
            current_solution = best_neighbor
            best_cost, _ = ObjectiveFunction(best_solution, other_conditions)

            if best_neighbor_obj < best_cost:
                best_solution = best_neighbor
        
        # Update tabu list
        if best_neighbor is not None:
            tabu_list.append({'solution': best_neighbor, 'value': best_neighbor_obj})
            tabu_list = sorted(tabu_list, key=lambda x: x['value'])
            if len(tabu_list) > tabu_list_size:
                tabu_list.pop(0)  # Remove worst entry from tabu list

        if old_best_cost is not None:
            if old_best_cost == best_cost:
                repetition += 1
            else:
                repetition = 0

        if repetition == max_repetitions:
            break
        
        old_best_cost = best_cost

    return best_solution, i+1

def RunTabuMultipleTimes(app, assignments, max_iterations, tabu_list_size, num_runs, other_conditions):

    app.updateProcess(0/num_runs)
    objective_values = []
    all_solutions = []
    all_iterations = []

    for run in range(num_runs):
        print(f"\tProcess {run+1}/{num_runs}")
        current_solution, iterations = TabuAlgorithm(assignments, max_iterations, tabu_list_size, other_conditions)
        current_cost, _ = ObjectiveFunction(current_solution, other_conditions)

        for assignment in current_solution:
            assignment.setPeriodScheduled(sortSolution(assignment.period_scheduled))

        app.updateProcess((run+1)/num_runs)
        objective_values.append(current_cost)
        all_solutions.append(current_solution)
        all_iterations.append(iterations)

    app.setObjectiveValues(objective_values)
    app.setNumberRuns(num_runs)
    app.setNumberIterations(all_iterations)

    all_best_solutions = getBestSolutions(all_solutions, min(objective_values), other_conditions)

    return all_best_solutions

## Functions to generate solutions
def GenerateNeighborhood(assignments):
    Neighbors = []

    for index, assignment in enumerate(assignments):
        # Seleciona um período aleatório para alterar
        set_period = random.choice(assignment.periods)
        available_times = set_period.available
        
        # Extrai dias únicos dos tempos disponíveis
        days = list(set(time['day'] for time in available_times.values()))
        
        # Gera todas as combinações possíveis do número necessário de dias
        days_combinations = list(itertools.combinations(days, int(assignment.qnt_week)))
        
        # Seleciona uma combinação de dias aleatoriamente
        days_combination = random.choice(days_combinations)
        
        all_daily_periods = []
        for day in days_combination:
            list_available_dailyperiod = [index_time for index_time, time in available_times.items() if time['day'] == day]
            all_daily_periods.append(list_available_dailyperiod)
        
        # Gera as combinações de períodos para os dias selecionados
        periods_combinations = list(itertools.product(*all_daily_periods))
        
        # Seleciona uma combinação de períodos aleatoriamente
        periods = random.choice(periods_combinations)
        
        period_scheduled = {}
        for i, p in enumerate(periods, start=1):
            period_scheduled[i] = available_times[p]
        
        # Arranja o período agendado na sequência dos dias da semana
        period_scheduled = dict(sorted(period_scheduled.items(), key=lambda item: day_to_number(item[1]['day'])))
        
        if period_scheduled != assignment.period_scheduled:
            new_solution = deepcopy(assignments)
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
def ObjectiveFunction(assignments, other_conditions):
    # Weights
    W_HC = [100000, 100000]
    W_SC = [100, 100, 100]
    all_overview = []
    # Hard Constraints
    _, Z_HC_1, overviewHC1 = HardConstraint1(assignments)
    all_overview.append(overviewHC1)
    _, Z_HC_2, overviewHC2 = HardConstraint2(assignments)
    all_overview.append(overviewHC2)

    Z_HC = W_HC[0]*Z_HC_1 + W_HC[1]*Z_HC_2

    # Soft Constraints
    Z_SC_1 = SoftConstraint1(assignments, other_conditions)
    Z_SC_2 = SoftConstraint2(assignments, other_conditions)
    Z_SC_3 = SoftConstraint3(assignments, other_conditions)
    Z_SC = W_SC[0]*Z_SC_1 + W_SC[1]*Z_SC_2 + W_SC[2]*Z_SC_3
    Z = Z_HC + Z_SC

    return Z, all_overview

def getBestSolutions(all_solutions, best_objective, other_conditions):
    best_solutions = []
    for solution in all_solutions:
        cost, overview = ObjectiveFunction(solution, other_conditions)
        if cost == best_objective:
            if not equal_results(solution, best_solutions):
                best_solutions.append(solution)

    return best_solutions

def equal_results(solution, list_solutions):
    for existing_solution in list_solutions:
        if solutions_are_equal(solution, existing_solution):
            return True
    return False

def solutions_are_equal(solution1, solution2):
    if len(solution1) != len(solution2):
        return False
    for assignment1, assignment2 in zip(solution1, solution2):
        if assignment1.period_scheduled != assignment2.period_scheduled:
            return False
    return True

## Constraint functions

# Hard constraints
# 1 - All assignments needs to be scheduled
def HardConstraint1(assignments):

    overviewHC1 = ['Overview Hard Constraint 1']
    value_Z = 0
    flag = 0
    for assignment in assignments:
        if assignment.period_scheduled == 0:   # 0 is the default value
            overviewHC1.append(f'Violation - {assignment.name} is not scheduled')
            flag += 1
            value_Z += assignment.getPriority()
    if flag == 0:
        overviewHC1.append('All assignments are scheduled.')
    
    return flag, value_Z, overviewHC1

# 2 - Only one assignment must be scheduled in a specific set of slots
def HardConstraint2(assignments):

    overviewHC2 = ['Overview Hard Constraint 2']
    value_Z = 0
    flag = 0
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
                flag += 1
                value_Z += current_assignment.getPriority()

    if flag == 0:
        overviewHC2.append('No overlapping intervals between assessments.')

    return flag, value_Z, overviewHC2

# Soft constraints
# 1 - Priorities in week distribution
def SoftConstraint1(assignments, other_conditions):
    # Get week distribution
    week_distribution = getWeekDistribution(assignments)

    free_days = np.sum(week_distribution[week_distribution==0])
    condition1 = (7 - free_days)/7*other_conditions[0]
    
    Z_SC = condition1
    return Z_SC

# 2 - Priorities in week distribution
def SoftConstraint2(assignments, other_conditions):
    # Get week distribution
    week_distribution = getWeekDistribution(assignments)

    coef_variation = np.std(week_distribution)/np.mean(week_distribution) # Calculate the coefficient of variation
    condition2 = coef_variation*other_conditions[1]
    
    Z_SC = condition2
    return Z_SC

# 3 - Priorities in week distribution
def SoftConstraint3(assignments, other_conditions):
    # Get week distribution
    week_distribution = getWeekDistribution(assignments)

    weekend_assign = np.sum(week_distribution[4:6])
    condition3 = weekend_assign/np.sum(week_distribution)*other_conditions[2]
    
    Z_SC = condition3
    return Z_SC

## Plot results
def PlotResults(TimeTabling, other_conditions):
    Z, overview = ObjectiveFunction(TimeTabling, other_conditions)
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


