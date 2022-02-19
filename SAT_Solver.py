'''
  SAT Solver based on Davis–Putnam–Logemann–Loveland (DPLL) algorithm
  Uses Jersolow-Wang 2-sided method (consider only positive literals)

  Returns -
  * SATISFIABLE followed by the model if the formula is satisfiable
  * UNSATISFIABLE if the formula is unsatisfiable
'''

# Import necessary libraries
import argparse
import os
import textwrap
import time


# Parse the clauses in the input DIMACs file and store them in a list
def parse_dimacs(filename):
  '''
    Argument(s) : filename - name of the DIMACs CNF file
    Return value : a tuple consisting of a list - the clauses in 
                   the input file and the number of variables
  '''
  clauses = []

  for line in open(filename):
    if line.startswith('c'):
      continue
    if line.startswith('p'):
      n_vars = line.split()[2]  # Number of variables present
      continue
    clause = [int(x) for x in line[:-2].split()]
    clauses.append(clause)

  return clauses, int(n_vars)


# Jersolow-Wang 2-sided method considers only positive literals
# This is faster than Jersolow-Wang method by 50% improvement in speed

# Calculating Literal Weights
def get_weighted_abs_counter(formula, weight=2):
  counter = {}

  for clause in formula:
    for literal in clause:
      if abs(literal) in counter:
        counter[abs(literal)] += weight ** -len(clause)
      else:
        counter[abs(literal)] = weight ** -len(clause)

  return counter

# JW2S method implementation
def jeroslow_wang_2_sided(formula):
  counter = get_weighted_abs_counter(formula)
  return max(counter, key=counter.get)


# Boolean Constrain Propagation
# We set unit to true and so we need to update the cnf by the following rules:
# - Clauses that contain unit are removed (due to "or")
# - Update clauses by removing -unit from them if it exist (due to "or")
def bcp(formula, unit):
  modified = []

  for clause in formula:
    if unit in clause:
      continue
    if -unit in clause:
      new_clause = [x for x in clause if x != -unit]
      # Base case: Conjunct containing an empty disjunct so False
      # but we should continue later because there might be another path
      if not new_clause:
        return -1
      modified.append(new_clause)
    else:
      modified.append(clause)

  return modified


# The DPLL algorithm works by choosing an assignment of true or false 
# for a variable, simplifying the formula based on that choice, then 
# recursively checking the satisfiability of the simplified formula.

# Perform unit propagation - formula simplification
'''
  If a clause is a unit clause (one with only one variable), 
  then the only way for the formula to be satisfiable is for 
  that variable to be assigned consistently with its sign in 
  that clause. Thus, we know that variable must take on that 
  assignment, which tells us that all other clauses with that 
  literal are now satisfied. In addition, we know that clauses 
  with the literal's negation will not be satisfied by that 
  component, so we can remove the negation from all clauses.
'''
def unit_propagation(formula):
  assignment = []
  unit_clauses = [c for c in formula if len(c) == 1]

  # Iterate through all unit clauses
  while unit_clauses:
    unit = unit_clauses[0]
    formula = bcp(formula, unit[0])
    assignment += [unit[0]]
    if formula == -1:
      return -1, []
    if not formula:   # If no more unit clauses are present, return current formula
      return formula, assignment
    unit_clauses = [c for c in formula if len(c) == 1]
  
  return formula, assignment


# Implement the DPLL algorithm - recursive backtracking
'''
  The algorithm "guesses" a variable to be true, recursively 
  determines if that subproblem is satisfiable; if it is not, 
  the algorithm then "guesses" the variable to be false and 
  tries again.
'''
def backtracking(formula, assignment):
  formula, unit_assignment = unit_propagation(formula)
  assignment = assignment + unit_assignment

  if formula == - 1:
    return []
  if not formula:
    return assignment

  variable = jeroslow_wang_2_sided(formula)
  solution = backtracking(bcp(formula, variable), assignment + [variable])
  # If no solution when assigning to True, try to assign to False
  if not solution:
    solution = backtracking(bcp(formula, -variable), assignment + [-variable])

  return solution


##### Utilities function #####

# Benchmarks Tester
# Test a folder of CNF formulas and get the average time with the SAT-solver
def run_benchmarks(fname, folder):
  print('Running on benchmarks...')

  start_time = time.time()   # Start the Timer

  with open(fname, 'w') as out_file:
    for filename in os.listdir(folder):
      clauses, n_vars = parse_dimacs(os.path.join(folder, filename))  # Get the clauses
      solution = backtracking(clauses, [])
      
      out_file.write(filename + ' : ')   # Write the filename for clarity
      if solution:
        solution += [x for x in range(1, n_vars + 1) if x not in solution and -x not in solution]
        solution.sort(key=abs)  # Sort based on absolute value
        out_file.write('SAT')
        out_file.write('  [')
        for cl in solution:
          out_file.write(f'{cl},')
        out_file.write(']')
      else:
        out_file.write('UNSAT')
      out_file.write('\n')

  end_time = time.time()  # Stop the Timer

  print('Execution time: %.2f seconds' % (end_time - start_time))


# Main Function
def main():
  # Command-line interfaces
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''\
    SAT Solver based on DPLL Algorithm
    -----------------------------------
    Returns
    1. A model if the formula is satisfiable
    2. Reports that the formula is unsatisfiable'''))
  parser.add_argument('--input_file', default=None, 
    help='runs the sat solver over the input file (must be in DIMACs format)')
  parser.add_argument('--run_benchmarks', default=None, 
    help='runs the sat solver over all files in the input folder (provide only the folder name)')
  args = parser.parse_args()

  if args.run_benchmarks is not None:
    # Runs the SAT Solver over all the files and creates a log
    run_benchmarks('benchmarks-results.log', args.run_benchmarks)
  
  elif args.input_file is not None:
    f = args.input_file
    assert os.path.exists(f), '{} does not exists'.format(f)

    start_time = time.time()   # Start the Timer

    clauses, n_vars = parse_dimacs(f)
    solution = backtracking(clauses, [])  # Check for solution
    if solution:
        solution += [x for x in range(1, n_vars + 1) if x not in solution and -x not in solution]
        solution.sort(key=abs)
        print ('s SATISFIABLE')
        print ('v ' + ' '.join([str(x) for x in solution]) + ' 0')
    else:
        print ('s UNSATISFIABLE')

    end_time = time.time()  # Stop the Timer

    print('Execution time: %.2f seconds' % (end_time - start_time))
  else:
    print('Please either choose an input file or run the benchmarks. Type --help or --h for more details')


if __name__ == '__main__':
  main()