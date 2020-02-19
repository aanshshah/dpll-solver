import sys
import time

def parse(filename):
    clauses = []
    for line in open(filename):
        if line.startswith('c'): continue
        if line.startswith('p'):
            n_vars = int(line.split()[2])
            continue
        clause = []
        for x in line[:-2].split():
            clause.append(int(x))
        clauses.append(clause)
    return clauses, n_vars


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


clauses, n_vars = parse(sys.argv[1])
start = time.time()
solution = backtracking(clauses, [])
end = time.time() - start
if solution:
    solution += [x for x in range(1, n_vars + 1) if x not in solution and -x not in solution]
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
    result = ' '.join([str(x) for x in result])
    print("Instance: {0} Time: {1} Result: SAT Solution {2}".format(sys.argv[1], end, result))
else: 
    end = time.time() - start
    print("Instance: {0} Time: {1} Result: {2}".format(sys.argv[1], end, "UNSAT"))
