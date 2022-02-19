# Helper Functions

# Get the Dimacs CNF variable number for the variable v_{r,c,v}
# encoding the fact that the cell at (r,c) has the value v

from pprint import pprint


def dimac_cnf_var(n, r, c, v):
  # assert(1 <= r and r <= n * 2 and 1 <= c and c <= n and 1 <= v and v <= n)
  return (r - 1) * n * n + (c - 1) * n + (v - 1) + 1


# Build the clauses in a list
def build_clauses(sudoku_clues, n, k):
  clauses = []  # The clauses: a list of integer lists

  for r in range(1, n * 2 + 1):    # the number of rows ranges from 1 to 2n
    for c in range(1, n + 1):      # the number of columns ranges from 1 to n
      # The clues must be respected
      if sudoku_clues[r - 1][c - 1] in range(1, n + 1):
        clauses.append([dimac_cnf_var(n, r, c, sudoku_clues[r - 1][c - 1])])
      # The cell at (r, c) has at least 1 value
      clauses.append([dimac_cnf_var(n, r, c, v) for v in range(1, n + 1)])
      # The cell at (r, c) has at most 1 value
      for v in range(1, n + 1):
        for w in range(v + 1, n + 1):
          clauses.append([-dimac_cnf_var(n, r, c, v), -dimac_cnf_var(n, r, c, w)])

  for v in range(1, n + 1):
    # Each row (in both the sudokus) has the value v
    for r in range(1, n * 2 + 1):
      clauses.append([dimac_cnf_var(n, r, c, v) for c in range(1, n + 1)])

    for c in range(1, n + 1):
      # Each column has the value v (for the first sudoku)
      clauses.append([dimac_cnf_var(n, r, c, v) for r in range(1, n + 1)])
      # Each column has the value v (for the second sudoku)
      clauses.append([dimac_cnf_var(n, r, c, v) for r in range(n + 1, n * 2 + 1)])
      # Considering the sudoku pairs, S1(r, c) != S2(r, c)
      for r in range(1, n + 1):
        clauses.append([-dimac_cnf_var(n, r, c, v), -dimac_cnf_var(n, r + n, c, v)])

    # Each subgrid has the value v
    for sr in range(0, k * 2):
      for sc in range(0, k):
        clauses.append([dimac_cnf_var(n, sr * k + rd, sc * k + cd, v) 
                        for rd in range(1, k + 1) for cd in range(1, k + 1)])       

  return clauses


# Decode SAT output
def decoder(sat_out, n):
  output = [[] for i in range(n * 2)]  # to store the solved sudoku
  if sat_out != None:
    for x in range(n * 2):
      for y in range(n):
        for z in range(n):
          if sat_out[x * n * n + y * n + z] >= 0:
            output[x].append(z + 1)
            break     
  else:
    output = "None"
  
  return output


# To make a nice print of the sudoku board
def expandLine(line, k):
    return line[0]+line[5 : 9].join([line[1 : 5] * (k - 1)] * k) + line[9 : 13]

# Print the sudoku in a beautiful grid format
def print_sudoku(sudoku, k, n):
  line0  = expandLine("╔═══╤═══╦═══╗", k)
  line1  = expandLine("║ . │ . ║ . ║", k)
  line2  = expandLine("╟───┼───╫───╢", k)
  line3  = expandLine("╠═══╪═══╬═══╣", k)
  line4  = expandLine("╚═══╧═══╩═══╝", k)

  nums   = [[""]+[str(n) if n > 0 else ' ' for n in row] for row in sudoku]
  print("1st Sudoku")
  print(line0)
  for r in range(1, n + 1):
    line_seg = line1.split(".")
    prin_str = ''
    for i in range(n + 1):
      if nums[r - 1][i] != ' ' and nums[r - 1][i] != '' and int(nums[r - 1][i]) > 9:
        line_seg[i] = line_seg[i][1:]
      prin_str += nums[r - 1][i] + line_seg[i]
    print(prin_str)
    print([line2, line3, line4][(r % n == 0)+(r % k == 0)]) 

  print("\n2nd Sudoku")
  print(line0)
  for r in range(n + 1, n * 2 + 1):
    line_seg = line1.split(".")
    prin_str = ''
    for i in range(n + 1):
      if nums[r - 1][i] != ' ' and nums[r - 1][i] != '' and int(nums[r - 1][i]) > 9:
        line_seg[i] = line_seg[i][1:]
      prin_str += nums[r - 1][i] + line_seg[i]
    print(prin_str)
    print([line2, line3, line4][(r % n == 0)+(r % k == 0)]) 