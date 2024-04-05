from OtherFunctions import *

### Optimization functions

## Main functions
def runOptimizationProgram(assignments, initial_temperature, cooling_rate, max_iterations, num_runs):

    if IsThereNeighboors(assignments):
        best_solution = RunAnnealingMultipleTimes(assignments, initial_temperature, cooling_rate, max_iterations, num_runs)    
    else:
        best_solution = GenerateInitialSolution(assignments)

    return best_solution

def AnnealingAlgorithm(assignments, initial_temperature, cooling_rate, max_iterations):
    # 1 - Generate initial solution
    current_solution = GenerateInitialSolution(assignments)
    # 2 - Update the best solution
    best_solution = current_solution
    # 3 - Update temperature
    current_temperature = initial_temperature

    for i in range(max_iterations):
        # 4 - Generate a neighbour from the current solution
        neighbor_solution = GenerateNeighboors(current_solution)
        # 5 - Evaluate
        current_cost, _ = ObjectiveFunction(current_solution)
        neighbor_cost, _ = ObjectiveFunction(neighbor_solution)
        cost_diff = neighbor_cost - current_cost

        if cost_diff < 0 or random.random() < math.exp(-cost_diff / current_temperature):
            current_solution = neighbor_solution

        current_cost, _ = ObjectiveFunction(current_solution)
        best_cost, _ = ObjectiveFunction(neighbor_solution)

        if current_cost < best_cost:
            best_solution = current_solution

        current_temperature *= cooling_rate

    return best_solution

def RunAnnealingMultipleTimes(assignments, initial_temperature, cooling_rate, max_iterations, num_runs):
    best_solution = None
    best_cost = float('inf')

    for _ in range(num_runs):
        current_solution = AnnealingAlgorithm(assignments, initial_temperature, cooling_rate, max_iterations)
        current_cost, _ = ObjectiveFunction(assignments)

        if current_cost < best_cost:
            best_solution = current_solution
            best_cost = current_cost

    return best_solution

## Functions to generate solutions
def GenerateNeighboors(assignments):
    
    flag = 0
    while flag == 0:
        # Select a random assignment
        i_assignment = random.choice(range(0,len(assignments)))

        period = getNewPossiblePeriod(assignments[i_assignment])
        
        # Verify if the solution is the same of the previous one
        if period != assignments[i_assignment].period_scheduled:
            flag = 1
    
    assignments[i_assignment].period_scheduled = period
    return assignments

def GenerateInitialSolution(assignments):
    for assignment in assignments:
        period = getNewPossiblePeriod(assignment)
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
    W_HC = [1000, 1000]
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
            
            if any(slot in flatten_slots_next for slot in flatten_slots_current):
                overviewHC2.append(f'Violation: Overlapping slots between assignments {current_assignment.name} and {next_assignment.name}')
                sum += 1

    if sum == 0:
        overviewHC2.append('No overlapping intervals between assessments.')

    return sum, overviewHC2



