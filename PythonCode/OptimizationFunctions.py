from OtherFunctions import *

### Optimization functions

## Main functions
def runOptimizationProgram(assignments, initial_temperature, cooling_rate, max_iterations, num_runs):

    best_solution = RunAnnealingMultipleTimes(assignments, initial_temperature, cooling_rate, max_iterations, num_runs)

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
        current_cost = ObjectiveFunction(current_solution)
        neighbor_cost = ObjectiveFunction(neighbor_solution)
        cost_diff = neighbor_cost - current_cost

        if cost_diff < 0 or random.random() < math.exp(-cost_diff / current_temperature):
            current_solution = neighbor_solution

        if ObjectiveFunction(current_solution) < ObjectiveFunction(best_solution):
            best_solution = current_solution

        current_temperature *= cooling_rate

    return best_solution

def RunAnnealingMultipleTimes(assignments, initial_temperature, cooling_rate, max_iterations, num_runs):
    best_solution = None
    best_cost = float('inf')

    for _ in range(num_runs):
        current_solution = AnnealingAlgorithm(assignments, initial_temperature, cooling_rate, max_iterations)
        current_cost = ObjectiveFunction(assignments)

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

## Cost function
def ObjectiveFunction(assignments):
    return 10

## Constraint functions

# Hard constraints