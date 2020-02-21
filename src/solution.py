import sys
import time

def check_solution(clauses,solution):
    #A validation script that takes a problem and solution, and confirms that the solution is valid

    def var_to_literal(var,assignment):
        assert assignment == 'true' or assignment == 'false' #Check that variable was assigned valid value
        return var if assignment == 'true' else -1 * var

    number_vars_in_solution = int(len(solution)/2) #number of variables in the solution
    true_literals = []
    for i in range(number_vars_in_solution):
        true_literals.append(var_to_literal(solution[2*i],solution[2*i+1]))

    true_literals_unique = set(true_literals) #unique true literals
    assert len(true_literals) == len(true_literals_unique) #checks that no literals are assigned twice

    unique_vars_in_problem = set()
    for c in clauses:
        for v in c:
            unique_vars_in_problem.add(abs(v))
            if not (v in true_literals_unique or -1*v in true_literals_unique):
                print(v)
                print(true_literals_unique)
            assert v in true_literals_unique or -1*v in true_literals_unique #check that every variable or its negation appears in solution

    assert len(unique_vars_in_problem) == number_vars_in_solution #check that the problem and solution hhave same number of variables

    success = False
    for c in clauses:
        for v in c:
            if v in true_literals_unique:
                success = True
                break
        assert success #check that every clause has a true literal



def parse(filename):
    clauses = []
    all_vars = set()
    for line in open(filename):
        if line.startswith('c'): continue
        if line.startswith('p'):
            n_vars = int(line.split()[2])
            continue
        clause = []
        for x in line[:-2].split():
            clause.append(int(x))
            all_vars.add(int(x))
        clauses.append(clause)
    return clauses, n_vars, all_vars


def binary_constraint_propagation(formula, unit):
    modified = []
    for clause in formula:
        if unit in clause: continue
        new_clause = []
        if -unit in clause:
            for x in clause:
                if x != -unit: new_clause.append(x)
            if not new_clause: return -1
            modified.append(new_clause)
        else: modified.append(clause)
    return modified

def backtracking(formula, assignment):

    def unit_propagation(formula):
        assignment = []
        unit_clauses = [c for c in formula if len(c) == 1]
        while unit_clauses:
            unit = unit_clauses[0]
            formula = binary_constraint_propagation(formula, unit[0])
            assignment += [unit[0]]
            if formula == -1: return -1, []
            if not formula: return formula, assignment
            unit_clauses = []
            for c in formula:
                if len(c) == 1: unit_clauses.append(c)
        return formula, assignment

    formula, unit_assignment = unit_propagation(formula)
    assignment = assignment + unit_assignment
    if formula == - 1: return []
    if not formula: return assignment
    #Jeroslow Wang Heuristic
    counter = {}
    weight = 2
    for clause in formula:
        for literal in clause:
            if literal in counter: counter[literal] += weight ** -len(clause)
            else: counter[literal] = weight ** -len(clause)
    if counter: variable = max(counter, key=counter.get)
    else: return unit_assignment
    one_lit = binary_constraint_propagation(formula, variable)
    solution = backtracking(one_lit, assignment + [variable])
    if not solution:
        one_lit = binary_constraint_propagation(formula, -variable)
        solution = backtracking(one_lit, assignment + [-variable])
    return solution


clauses, n_vars, all_vars = parse(sys.argv[1])
start = time.time()
solution = backtracking(clauses, [])
end = time.time() - start
if solution:
    for x in range(1, n_vars+1):
        if x not in solution and -x not in solution:
            if x in all_vars or -x in all_vars:
                solution.append(x)
    # solution += [x for x in range(1, n_vars + 1) if x not in solution and -x not in solution]
    solution.sort(key=abs)
    result = []
    t = 0
    for i in solution:
        result.append(i)
        if i > 0:
            result.append("true")
        else:
            result.append("false")
        result[t] = abs(int(result[t]))
        t += 2
    check_solution(clauses,result)
    result = ' '.join([str(x) for x in result])
    print("Instance: {0} Time: {1} Result: SAT Solution {2}".format(sys.argv[1], end, result))
else: 
    end = time.time() - start
    print("Instance: {0} Time: {1} Result: {2}".format(sys.argv[1], end, "UNSAT"))
