import sys
import os
import glob
import time
import random
import numpy as np
os.chdir("../input/random_unked_sub_USABLE")

from pysat.solvers import Minisat22



random.seed(64920)

problems_all = []
global_counter = 0
reset = False


np_load_old = np.load
np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)



feature_0 = [] #num clauses
feature_1 = [] #num variables
feature_2 = [] #avg clause length
feature_3 = [] #jwang (2,3,4)
feature_4 = [] #av fequency

labels = []


def most_frequent(formula):
        counter = {}
        for clause in formula:
            for literal in clause:
                if literal in counter:
                    counter[literal] += 1
                else:
                    counter[literal] = 1
        return max(counter, key=counter.get)
 
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


for i,file in enumerate(sorted(list(glob.glob("*_tagged_data.npy")),reverse=True)):
    
    tagged_data = np.load(file)
    for d,l in tagged_data:
    	data.append(d)




    	labels.append(l)







    print("LOADED")