import sys
import os
import glob
import time
import random
import numpy as np
os.chdir("../input")



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

def backtracking(formula, assignment,heuristic):


    def freeman(formula):
        counter = {}
        for clause in formula:
            for literal in clause:
                if literal in counter:
                    if literal > 0:
                        counter[literal] += 1
                    else:
                        counter[-literal] += - 1
                else:
                    if literal > 0:
                        counter[literal] = 1
                    else:
                        counter[-literal] = - 1
        max_p_literal = max(counter, key=counter.get)
        max_n_literal = min(counter, key=counter.get)
        if counter[max_p_literal] >= abs(counter[max_n_literal]):
            return max_p_literal
        return max_n_literal

    def randomly_select(formula):
        counter = {}
        for clause in formula:
            for literal in clause:
                if literal in counter:
                    counter[literal] += 1
                else:
                    counter[literal] = 1
        return random.choice(counter.keys())

    def most_frequent(formula):
        counter = {}
        for clause in formula:
            for literal in clause:
                if literal in counter:
                    counter[literal] += 1
                else:
                    counter[literal] = 1
        return max(counter, key=counter.get)
    
    def spc(formula): #shortest positive literal
        min_len = 1000000 #sys.maxint
        best_literal = 0
        for clause in formula:
            negatives = sum(1 for literal in clause if literal < 0)
            if not negatives and len(clause) < min_len:
                best_literal = clause[0]
                min_len = len(clause)
        if not best_literal:
            return formula[0][0]
        return best_literal

    def jeroslow_wang(formula, weight=2):
        counter = {}
        for clause in formula:
            for literal in clause:
                if literal in counter: counter[literal] += weight ** -len(clause)
                else: counter[literal] = weight ** -len(clause)
        if counter:
            return max(counter, key=counter.get)
        else:
            return None

    def jeroslow_wang_2_sided(formula, weight=2):
        counter = {}
        for clause in formula:
            for literal in clause:
                literal = abs(literal)
                if literal in counter:
                    counter[literal] += weight ** -len(clause)
                else:
                    counter[literal] = weight ** -len(clause)

        return max(counter, key=counter.get)



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
    variable = None

    if heuristic == "jw":
        variable = jeroslow_wang(formula)
    elif heuristic == "jw2":
        variable = jeroslow_wang_2_sided(formula)
    elif  heuristic == "spc":
        variable = spc(formula)
    elif  heuristic == "mf":
        variable = most_frequent(formula)
    elif  heuristic == "rand":
        variable = randomly_select(formula)
    elif  heuristic == "free":
        variable = freeman(formula)




    if variable == None: return []
    # print(variable)
    one_lit = binary_constraint_propagation(formula, variable)
    solution = backtracking(one_lit, assignment + [variable],heuristic)
    if not solution:
        one_lit = binary_constraint_propagation(formula, -variable)
        solution = backtracking(one_lit, assignment + [-variable],heuristic)
    return solution



# def backtracking_restart(formula, assignment,heuristic,counter=1):

#     def randomly_select(formula):
#         counter = {}
#         for clause in formula:
#             for literal in clause:
#                 if literal in counter:
#                     counter[literal] += 1
#                 else:
#                     counter[literal] = 1
#         return random.choice(counter.keys())

#     def most_frequent(formula):
#         counter = {}
#         for clause in formula:
#             for literal in clause:
#                 if literal in counter:
#                     counter[literal] += 1
#                 else:
#                     counter[literal] = 1
#         return max(counter, key=counter.get)
    
#     def spc(formula): #shortest positive literal
#         min_len = 100000
#         best_literal = 0
#         for clause in formula:
#             negatives = sum(1 for literal in clause if literal < 0)
#             if not negatives and len(clause) < min_len:
#                 best_literal = clause[0]
#                 min_len = len(clause)
#         if not best_literal:
#             return formula[0][0]
#         return best_literal

#     def jeroslow_wang(formula, weight=2):
#         counter = {}
#         for clause in formula:
#             for literal in clause:
#                 if literal in counter: counter[literal] += weight ** -len(clause)
#                 else: counter[literal] = weight ** -len(clause)
#         return max(counter, key=counter.get) if len(counter) > 0 else None

#     def jeroslow_wang_prob(formula, weight=2):
#         counter = {}
#         for clause in formula:
#             for literal in clause:
#                 if literal in counter: counter[literal] += weight ** -len(clause)
#                 else: counter[literal] = weight ** -len(clause)

#         total_score = sum([v for k,v in counter.items()])
#         literals = list(counter.keys())

#         return np.random.choice(literals,p=[counter[k]/total_score for k in literals]) if len(counter) > 0 else None

#     def jeroslow_wang_2_sided(formula, weight=2):
#         counter = {}
#         counter_orig = {}
#         for clause in formula:
#             for literal in clause:
#                 # literal_orig = literal
#                 literal = abs(literal)


#                 # if literal_orig in counter_orig:
#                 #     counter_orig[literal_orig] += weight ** -len(clause)
#                 # else:
#                 #     counter_orig[literal_orig] = weight ** -len(clause)

#                 if literal in counter:
#                     counter[literal] += weight ** -len(clause)
#                 else:
#                     counter[literal] = weight ** -len(clause)
#         # if len(counter) > 0: return (1,[]) #May need to fix this behavior

#         best_literal = max(counter, key=counter.get)

#         return best_literal #max((best_literal,best_literal*-1), key=counter_orig.get) 


#     def unit_propagation(formula):
#         assignment = []
#         unit_clauses = [c for c in formula if len(c) == 1]
#         while unit_clauses:
#             unit = unit_clauses[0]
#             formula = binary_constraint_propagation(formula, unit[0])
#             assignment += [unit[0]]
#             if formula == -1: return -1, []
#             if not formula: return formula, assignment
#             unit_clauses = []
#             for c in formula:
#                 if len(c) == 1: unit_clauses.append(c)
#         return formula, assignment

#     if counter <= 0: return (0,[])

#     formula, unit_assignment = unit_propagation(formula)
#     assignment = assignment + unit_assignment
#     if formula == - 1: return (1,[])
#     if not formula: return (1,assignment)
#     variable = None

#     if heuristic == "jw":
#         variable = jeroslow_wang_prob(formula)
#     elif heuristic == "jw2":
#         variable = jeroslow_wang_2_sided(formula)
#     elif  heuristic == "spc":
#         variable = spc(formula)
#     elif  heuristic == "mf":
#         variable = most_frequent(formula)
#     elif  heuristic == "rand":
#         variable = randomly_select(formula)



#     if variable == None: return (1,[])
#     # print(variable)
#     one_lit = binary_constraint_propagation(formula, variable)
#     solution = backtracking_restart(one_lit, assignment + [variable],heuristic,counter-1)
#     if solution == (1,[]):
#         one_lit = binary_constraint_propagation(formula, -variable)
#         solution = backtracking_restart(one_lit, assignment + [-variable],heuristic,counter-1)
#     # elif solution == (0,[]):
#     #     return (0,[])
#     return solution




# def backtracking_restart_manager(formula, assignment,heuristic):
#     result = []
#     finished = 0
#     restarts = 0

#     while finished == 0:
#         finished, result = backtracking_restart(formula, assignment,heuristic,2**restarts)
#         restarts+=1
#         print(restarts)
#     return result
    



for file in sorted(list(glob.glob("*.cnf")),reverse=True):
    print(file)
    clauses, n_vars = parse(file) #sys.argv[1])
    for heuristic in ["jw","spc","mf","rand","free"]:#"jw2"
        print("Using:",heuristic)
        program_starts = time.time()
        solution = backtracking(clauses, [],heuristic=heuristic) #backtracking_restart_manager(clauses, [],heuristic=heuristic) # $
        print("DONE")
        if solution:
            solution += [x for x in range(1, n_vars + 1) if x not in solution and -x not in solution]
            solution.sort(key=abs)
            print ('SAT ' + ' '.join([str(x) for x in solution]) + ' 0')
        else: print ('UNSAT')

        now = time.time()
        print("{} seconds elapsed".format(now - program_starts))
        print("\n")