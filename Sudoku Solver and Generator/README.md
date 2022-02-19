# Sudoku Pair – Solving and Generation

A k-sudoku puzzle pair solver and generator implemented by encoding the problem to propositional logic and solving it via SAT solver (PySAT).

Given a sudoku puzzle pair S1, S2 (both of dimension k) as input, the sudoku pair solver should fill the empty cells of both sudokus such that it satisfies the following constraints –

- Individual sudoku properties should hold.
- For each empty cell 𝑺𝟏[𝒊, 𝒋] ≠ 𝑺𝟐[𝒊, 𝒋], where i is row and j is column.

The k-sudoku puzzle pair generator must return a sudoku pair which is maximal (have the largest number of holes possible) and has a unique solution.


## Sudoku Pair Solver – Implementation

We can reduce the problem of solving Sudokus to the propositional satisfiability problem and the workflow looks like this –

<img src="https://github.com/Shreyasi2002/SAT_Solver___Sudoku/blob/main/Sudoku%20Solver%20and%20Generator/Sudoku%20Solver%20Workflow.png"/>

### Encoding Sudoku Pair in CNF

We are given a Sudoku puzzle pair and thus must build a propositional formula ∅ such that –
- the Sudoku pair has a solution if and only if the formula is satisfiable
- from a satisfying assignment for ∅, we can easily decode a solution for the sudoku grid.

To obtain such a formula, we introduce a variable x<sub>r,c,v</sub> for each row r = 1, ..., 2n, and column c = 1, ..., n and value = 1, ..., n. The intuition is that if x<sub>r,c,v</sub> is true, then the grid element at row r and column c has the value v.

To enforce that the values of the variables x<sub>r,c,v</sub> model solutions to the Sudoku puzzle, the formula **∅ = 𝐶<sub>1</sub>∧𝐶<sub>2</sub>∧𝐶<sub>3</sub>∧𝐶<sub>4</sub>∧𝐶<sub>5</sub>∧𝐶<sub>6</sub>∧𝐶<sub>7</sub>** is built by introducing sets of clauses that model different aspects of Sudoku solutions (consider n = k<sup>2</sup>):




To get the Dimacs CNF variable number for the variable x<sub>r,c,v</sub> (encoding the fact that the cell at (r, c) has the value v, the following formula is used
–
```
(r - 1) * n * n + (c - 1) * n + (v - 1) + 1
```

The above clauses are passed to the **PySAT - Glucose 4.1 SAT solver** which generates a model if the formula is satisfiable, else returns None.

The generated model is then passed to a decoder to get the output in the form of a sudoku grid.

Example :<br/>

Sudoku Pair Input and Output Grids for k = 3
```
1st Sudoku                                                     1st Sudoku
╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗                          ╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗
║   │   │   ║ 6 │   │   ║   │   │ 2 ║                          ║ 9 │ 8 │ 7 ║ 6 │ 4 │ 5 ║ 3 │ 1 │ 2 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢                          ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║   │ 5 │ 2 ║   │   │   ║ 7 │ 9 │   ║                          ║ 4 │ 5 │ 2 ║ 8 │ 1 │ 3 ║ 7 │ 9 │ 6 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢                          ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ 6 │   │   ║   │   │ 7 ║   │   │ 8 ║                          ║ 6 │ 3 │ 1 ║ 9 │ 2 │ 7 ║ 5 │ 4 │ 8 ║
╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣                          ╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣
║   │ 7 │   ║ 3 │   │ 1 ║   │ 5 │   ║                          ║ 2 │ 7 │ 8 ║ 3 │ 6 │ 1 ║ 4 │ 5 │ 9 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢                          ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ 1 │   │   ║   │ 5 │   ║ 8 │   │   ║                          ║ 1 │ 4 │ 6 ║ 2 │ 5 │ 9 ║ 8 │ 3 │ 7 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢                          ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║   │   │ 5 ║   │   │   ║   │ 2 │   ║                          ║ 3 │ 9 │ 5 ║ 4 │ 7 │ 8 ║ 6 │ 2 │ 1 ║
╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣                          ╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣
║ 7 │   │   ║   │ 9 │   ║   │   │ 4 ║                          ║ 7 │ 2 │ 3 ║ 5 │ 9 │ 6 ║ 1 │ 8 │ 4 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢                          ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║   │ 1 │   ║ 7 │   │   ║   │   │   ║                          ║ 8 │ 1 │ 4 ║ 7 │ 3 │ 2 ║ 9 │ 6 │ 5 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢                          ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║   │   │ 9 ║   │ 8 │   ║   │   │ 3 ║                          ║ 5 │ 6 │ 9 ║ 1 │ 8 │ 4 ║ 2 │ 7 │ 3 ║
╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝                          ╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝

2nd Sudoku                                                     2nd Sudoku
╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗                          ╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗
║   │   │   ║ 4 │   │   ║   │   │ 5 ║                          ║ 6 │ 2 │ 9 ║ 4 │ 7 │ 3 ║ 1 │ 8 │ 5 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢                          ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║   │ 3 │ 5 ║   │   │   ║ 9 │ 6 │   ║                          ║ 7 │ 3 │ 5 ║ 2 │ 8 │ 1 ║ 9 │ 6 │ 4 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢                          ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ 4 │   │   ║   │   │ 9 ║   │   │ 2 ║                          ║ 4 │ 1 │ 8 ║ 6 │ 5 │ 9 ║ 3 │ 7 │ 2 ║
╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣                          ╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣
║   │ 9 │   ║ 1 │   │ 8 ║   │ 3 │   ║                          ║ 5 │ 9 │ 2 ║ 1 │ 4 │ 8 ║ 7 │ 3 │ 6 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢                          ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ 8 │   │   ║   │ 3 │   ║ 2 │   │   ║                          ║ 8 │ 7 │ 4 ║ 5 │ 3 │ 6 ║ 2 │ 1 │ 9 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢                          ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║   │   │ 3 ║   │   │   ║   │ 5 │   ║                          ║ 1 │ 6 │ 3 ║ 7 │ 9 │ 2 ║ 4 │ 5 │ 8 ║
╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣                          ╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣
║ 9 │   │   ║   │ 6 │   ║   │   │ 7 ║                          ║ 9 │ 5 │ 1 ║ 3 │ 6 │ 4 ║ 8 │ 2 │ 7 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢                          ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║   │ 8 │   ║ 9 │   │   ║   │   │   ║                          ║ 2 │ 8 │ 7 ║ 9 │ 1 │ 5 ║ 6 │ 4 │ 3 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢                          ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║   │   │ 6 ║   │ 2 │   ║   │   │ 1 ║                          ║ 3 │ 4 │ 6 ║ 8 │ 2 │ 7 ║ 5 │ 9 │ 1 ║
╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝                          ╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝

      Input Sudoku Pair Grid                                          Output Sudoku Pair Grid

Time taken - 0.14565899999999998 secs
```
