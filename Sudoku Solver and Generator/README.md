# Sudoku Pair – Solving and Generation

A k-sudoku puzzle pair solver and generator implemented by encoding the problem to propositional logic and solving it via SAT solver (PySAT).

Given a sudoku puzzle pair S1, S2 (both of dimension k) as input, the sudoku pair solver should fill the empty cells of both sudokus such that it satisfies the following constraints –

- Individual sudoku properties should hold.
- For each empty cell 𝑺𝟏[𝒊, 𝒋] ≠ 𝑺𝟐[𝒊, 𝒋], where i is row and j is column.

The k-sudoku puzzle pair generator must return a sudoku pair which is maximal (have the largest number of holes possible) and has a unique solution.


## Implementation

We can reduce the problem of solving Sudokus to the propositional satisfiability problem and the workflow looks like this –

