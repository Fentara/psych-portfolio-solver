import ortools.linear_solver as pywraplp    
from staff_management import Staff

def create_optimization_model():
    # Create the solver
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Define sets
    P = []  # Psychologists
    S = []  # Schools
    Pr = []  # Programs

    # Define parameters (data)
    distance = {}  # Distance between schools
    fte_weight_school = 1  # Example weight
    fte_weight_program = {}  # FTE weight for each program
    optimal_fte = {}  # Optimal FTE for each psychologist
    allowed_program_types = {}  # Allowed program types for each psychologist
    school_programs = {}  # Programs offered at each school
    area = {}  # Primary area for each psychologist
    school_area = {}  # Area of each school
    same_area_bonus = 1  # Bonus for same area assignment
    school_preference = {}  # Preference score for schools
    program_preference = {}  # Preference score for programs

    # Decision Variables
    x = {}  # x[p, s]: Binary variable for psychologist p assigned to school s
    y = {}  # y[p, pr]: Binary variable for psychologist p assigned to program pr

    # Create decision variables
    for p in P:
        for s in S:
            x[(p, s)] = solver.BoolVar(f'x[{p},{s}]')
        for pr in Pr:
            y[(p, pr)] = solver.BoolVar(f'y[{p},{pr}]')

    # Constraints
    # Each school is supported by one psychologist
    for s in S:
        solver.Add(solver.Sum(x[(p, s)] for p in P) == 1)

    # Each program is supported by one psychologist
    for pr in Pr:
        solver.Add(solver.Sum(y[(p, pr)] for p in P) == 1)

    # Each psychologist supports only allowed program types
    for p in P:
        for pr in Pr:
            if pr not in allowed_program_types[p]:
                solver.Add(y[(p, pr)] == 0)

    # Objective Function
    objective = solver.Objective()
    
    # Minimize distance between schools
    for p in P:
        for s1 in S:
            for s2 in S:
                if s2 > s1:
                    objective.SetCoefficient(x[(p, s1)] * x[(p, s2)], distance[s1, s2])

    # Add other components to the objective function as per the original comments

    # Solve the model
    solver.Solve()

    # Return results
    return {p: [s for s in S if x[(p, s)].solution_value() == 1] for p in P}
 