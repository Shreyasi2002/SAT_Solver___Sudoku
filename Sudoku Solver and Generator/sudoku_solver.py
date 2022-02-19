# Importing Libraries
import sys
import csv
import time
from pysat.solvers import Solver

#Import the needed numbers to find which number is required for each row in the grid.
from utils import decoder, build_clauses, print_sudoku

# Global variables
k = 0  # Subgrid dimension
n = 0  # Grid dimension

# Read the clues from the file given as the second argument
def read_sudoku_from_file():
  global k, n, digits
  args = sys.argv
  if len(args) != 3:
    sys.exit(f"Usage : python3 ./{args[0]} dimension(int) input_sudoku_file.csv")

  k = int(args[1])
  n = k * k

  with open(args[-1], "r", encoding='utf-8-sig') as file:
    clues = []
    csvreader = csv.reader(file)
    for row in csvreader:
      clues.append([int(val) for val in row])

  return clues


# Main function
def main():
  sudoku_clues = read_sudoku_from_file()
  print_sudoku(sudoku_clues, k, n)

  # Modelling Solution to DIMACS CNF format
  clauses = build_clauses(sudoku_clues, n, k) 

  start = time.process_time()

  # Solving using "SAT-solver" -> PySAT - Glucose 4.1 SAT solver
  s = Solver(name='g4', bootstrap_with = clauses, use_timer = True)
  s.solve()
  sat_output = s.get_model()
  
  time_taken = time.process_time() - start

  s.delete()

  output = decoder(sat_output, n)
  if output != "None":
    print_sudoku(output, k, n)
  else:
    print("None")

  print(f"\nTime taken - {time_taken}")

if __name__ == '__main__':
  main()