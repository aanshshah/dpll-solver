import numpy as np
import itertools
from tqdm import tqdm 
from scipy.sparse import csr_matrix

def parse(filename, mode=None):
  with open(filename) as f:
    lines = f.read().splitlines()
    clause_counter = 0
    delete_rows = []
    for line in lines:
      if len(line) == 0: continue
      if line[0] == 'c':
        pass
      elif line[0] == 'p':
        line = line.split()
        num_variables = int(line[2])
        num_clauses = int(line[3])
        matrix = np.zeros(shape=(num_clauses, num_variables))
      else:
        line = line[:-1].split()
        exists = set()
        duplicated = False
        for variable in line:
          var = int(variable)
          if var * -1 in exists:
            matrix[clause_counter, :] = 0
            delete_rows.append(clause_counter)
            break
          exists.add(var)
          matrix[clause_counter][abs(var) - 1] = -1 if var < 0 else 1
        clause_counter += 1
  matrix = np.delete(matrix,delete_rows,0)
  return matrix


def best_ranked_var(problem):
  counts = np.sum(np.abs(problem),axis=0)
  best = np.argmax(counts)
  return best,counts[best]

def jeroslow_wang(problem,weight=2):
    clause_scores = weight ** (- 1 * np.sum(np.abs(problem),axis=1))
    variable_scores = np.dot(clause_scores,np.abs(problem))
    best = np.argmax(variable_scores)
    return best,variable_scores[best]

def update_problem(chosen_var,problem,literal):
  rows_to_delete = []

  for r in range(problem.shape[0]):
    if problem[r][chosen_var] == literal:
        rows_to_delete.append(r)

  new_problem = np.delete(problem,rows_to_delete,0)


  for r in range(new_problem.shape[0]):
    if new_problem[r][chosen_var] != 0: new_problem[r][chosen_var] = 0

    if not np.any(new_problem[r]):
        return None
  return new_problem

def dpll(problem,depth=0):
  chosen_var,count = jeroslow_wang(problem)
  print(chosen_var)
  # print(problem.shape[0])
  if count == 0: return [True]
  for literal in [1,-1]:
    new_problem = update_problem(chosen_var,problem,literal)
    store_problem = csr_matrix(problem)
    del problem 
    if new_problem is not None: 
      config = dpll(new_problem,depth+1)
      if config is not None: 
        del new_problem
        return [literal] + config
    del new_problem
    problem = store_problem.toarray()
    del store_problem

  return None
  




def selector_dpll(problem):
  # variables = np.arange(0,problem.shape[1])
  # np.random.shuffle(variables) #replace with sort
  print(dpll(problem))

  
problem1 = parse("input/C1597_081.cnf")

# print(valid_rows)
selector_dpll(problem1)
