import sys
import os
import glob
import time
import random
import numpy as np
os.chdir("../input/random_unked_sub")

from pysat.solvers import Glucose3



random.seed(64920)

problems_all = []
global_counter = 0
reset = False


np_load_old = np.load
np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)

for file in sorted(list(glob.glob("*.npy")),reverse=True):
    problems_all.extend(np.load(file))
    

for p in problems_all:
    g = Glucose3()
    for l in p:
        g.add_clause(l)
    print(g.solve())



    # for x in range(5):
    #     reset = False
    #     print("Using:",heuristic)
    #     print(x)
    #     program_starts = time.time()
    #     solution = backtracking(clauses, [],heuristic=heuristic) #backtracking_restart_manager(clauses, [],heuristic=heuristic) # $

    #     print("DONE")
    #     if solution:
    #         solution += [x for x in range(1, n_vars + 1) if x not in solution and -x not in solution]
    #         solution.sort(key=abs)
    #         print ('SAT ' + ' '.join([str(x) for x in solution]) + ' 0')
    #     else: print ('UNSAT')

    #     now = time.time()
    #     print("{} seconds elapsed".format(now - program_starts))
    #     print("\n")
    # np.save("random_unked_sub/"+file+"_remove_clauses_data.npy",problems_all)