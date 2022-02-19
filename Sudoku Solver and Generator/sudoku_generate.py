# Importing Libraries
from random import sample, choice
import random
from pprint import pprint
import copy
import time
import csv
from pysat.solvers import Solver

# Importing other essentials
from utils import build_clauses, decoder, print_sudoku

# Get input from user - dimension of sudoku
k = int(input("Enter the dimension of sub-grid in the sudoku : "))
n = k * k   # Dimension of grid

# Pattern for a baseline valid solution
def pattern(r, c):
  return (k * (r % k) + r // k + c) % n

# Randomize rows, columns and numbers (of valid base pattern)
def shuffle(s):
  return sample(s, len(s))

# Create a random sudoku
def rand_sudoku():
  rBase = range(k)
  numbers = list(range(1, n + 1))
  rows = [g * k + r for g in shuffle(rBase) for r in shuffle(rBase)]
  cols = [g * k + c for g in shuffle(rBase) for c in shuffle(rBase)]
  nums = shuffle(numbers)

  nums_2 = []  # for the second pair

  for i in range(n):
    data = numbers.copy()
    if nums[i] in data:
      data.remove(nums[i])
    random.shuffle(data)
    nums_2.append(data[0])
    numbers.remove(nums_2[i])

  # Produce board using randomized baseline pattern
  board_1 = [[nums[pattern(r, c)] for c in cols] for r in rows]
  board_2 = [[nums_2[pattern(r, c)] for c in cols] for r in rows]

  return board_1, board_2


# Remove some of the numbers from the sudoku solution (75%) to create the puzzle
def remove_num(board):
  squares = n * n
  empties = squares * 7 // 10
  for p in sample(range(squares), empties):
    board[p // n][p % n] = 0


# Get solution of the 70% empty sudoku board
# Check if there are more than 1 solution
def check_uniqueness(clauses):  
  # Solving using "SAT-solver" -> PySAT - Glucose 4.1 SAT solver
  s = Solver(name='g4', bootstrap_with=clauses, use_timer=True)
  s.solve()
  sat_output1 = s.get_model()
  s.delete()

  # Append a CNF clause that forbids the above sat_output
  clauses.append([-1 * p for p in sat_output1])

  # Return SAT solution
  s = Solver(name='g3', bootstrap_with=clauses, use_timer=True)
  if s.solve():
    sat_output2 = s.get_model()
    # Append a CNF clause that forbids the above sat_output
    clauses.append([-1 * p for p in sat_output2])
    s.delete()
    return decoder(sat_output1, n), decoder(sat_output2, n)
  else:
    return None, None


# Add numbers back to the board until there is only one way to solve it
# select a position where the solutions differ
def add_numbers(solution, board):
  # Modelling Solution to DIMACS CNF format
  clauses = build_clauses(board, n, k)

  while True:
    sat_output1, sat_output2 = check_uniqueness(clauses)
    if sat_output1 == None:     # the sudoku is unique
        break
    diffPos = [(r, c) for r in range(n * 2) for c in range(n) if sat_output1[r][c] != sat_output2[r][c]]
    if diffPos == []:    # the sudoku is unique
      break
    r, c = choice(diffPos)
    board[r][c] = solution[r][c]

def main():
  soln_1, soln_2 = rand_sudoku()   # Generate random sudokus

  # Create copies of list to avoid conflicts
  # Remove numbers from random locations from both the sudokus
  board_1 = copy.deepcopy(soln_1)
  remove_num(board_1)
  board_2 = copy.deepcopy(soln_2)
  remove_num(board_2)
  board_1.extend(board_2)

  soln_1.extend(soln_2)    # Store the solution of sudoku pair

  start = time.process_time()   # Start timer

  # Add numbers back to board till an unique soln is found
  add_numbers(soln_1, board_1)

  time_taken = time.process_time() - start

  # Print the sudoku board
  print_sudoku(board_1, k, n)
  print(f"\nTime taken - {time_taken}")

  # Write the output to a .csv file
  filename = 'Output Files/' + str(k) + '_dimensional.csv'
  with open(filename, 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the data rows
    csvwriter.writerows(board_1)


if __name__ == '__main__':
  main()
