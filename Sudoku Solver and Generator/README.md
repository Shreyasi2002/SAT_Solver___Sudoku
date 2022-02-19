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
* Each entry has at least one value:<br/>
            <img src="https://latex.codecogs.com/svg.image?C_1&space;=&space;\wedge_{1\leq&space;r\leq&space;2n,&space;1\leq&space;c\leq&space;n}(x_{r,c,1}\vee&space;x_{r,c,2}&space;...&space;\vee&space;x_{r,c,n})\texttt{}" title="C_1 = \wedge_{1\leq r\leq 2n, 1\leq c\leq n}(x_{r,c,1}\vee x_{r,c,2} ... \vee x_{r,c,n})\texttt{}" />
* Each entry has at most one value:<br/>
            <img src="https://latex.codecogs.com/svg.image?C_2&space;=&space;\wedge_{1\leq&space;r\leq&space;2n,&space;1\leq&space;c\leq&space;n,&space;1\leq&space;v<&space;v'\leq&space;n}(\sim&space;x_{r,c,v}\vee&space;\sim&space;x_{r,c,v'})&space;" title="C_2 = \wedge_{1\leq r\leq 2n, 1\leq c\leq n, 1\leq v< v'\leq n}(\sim x_{r,c,v}\vee \sim x_{r,c,v'}) " />
* Each row has all the numbers:<br/>
            <img src="https://latex.codecogs.com/svg.image?C_3&space;=&space;\wedge_{1\leq&space;r\leq&space;2n,&space;1\leq&space;v\leq&space;n}(x_{r,1,v}\vee&space;x_{r,2,v}&space;...&space;\vee&space;x_{r,n,v})" title="C_3 = \wedge_{1\leq r\leq 2n, 1\leq v\leq n}(x_{r,1,v}\vee x_{r,2,v} ... \vee x_{r,n,v})" />
* Each column has all the numbers:<br/>
            <img src="https://latex.codecogs.com/svg.image?C_4&space;=&space;\wedge_{1\leq&space;c\leq&space;n,&space;1\leq&space;v\leq&space;n}(x_{1,c,v}\vee&space;x_{2,c,v}&space;...&space;\vee&space;x_{n,c,v})&space;" title="C_4 = \wedge_{1\leq c\leq n, 1\leq v\leq n}(x_{1,c,v}\vee x_{2,c,v} ... \vee x_{n,c,v}) " /><br/>
            and<br/>
            <img src="https://latex.codecogs.com/svg.image?\wedge_{1\leq&space;c\leq&space;n,&space;1\leq&space;v\leq&space;n}(x_{n&plus;1,c,v}\vee&space;x_{n&plus;2,c,v}&space;...&space;\vee&space;x_{2n,c,v})&space;(for\:second\:sudoku)" title="\wedge_{1\leq c\leq n, 1\leq v\leq n}(x_{n+1,c,v}\vee x_{n+2,c,v} ... \vee x_{2n,c,v}) (for\:second\:sudoku)" />
* Each block has all the numbers:<br/>
            <img src="https://latex.codecogs.com/svg.image?C_5&space;=&space;\wedge_{1\leq&space;r'\leq&space;2k,&space;1\leq&space;c'\leq&space;k,&space;1\leq&space;v\leq&space;n}(\vee&space;_{(r,c)\epsilon&space;B_n(r',c')}x_{r,c,v})&space;" title="C_5 = \wedge_{1\leq r'\leq 2k, 1\leq c'\leq k, 1\leq v\leq n}(\vee _{(r,c)\epsilon B_n(r',c')}x_{r,c,v}) " /><br/>
            where,<br/>
            <img src="https://latex.codecogs.com/svg.image?B_n&space;(r',&space;c')&space;=&space;\left\{&space;{(r'\sqrt{n}&space;&plus;&space;i,&space;c'\sqrt{n}&plus;j)\;&space;|\;&space;0\leq&space;i,j\leq&space;\sqrt{n}}\right\}" title="B_n (r', c') = \left\{ {(r'\sqrt{n} + i, c'\sqrt{n}+j)\; |\; 0\leq i,j\leq \sqrt{n}}\right\}" />
* For each empty cell in the sudoku pair S1, S2, 𝑆1[𝑖, 𝑗] ≠ 𝑆2[𝑖, 𝑗]:<br/>
            <img src="https://latex.codecogs.com/svg.image?C_6&space;=&space;\wedge_{1\leq&space;r\leq&space;n,&space;1\leq&space;c\leq&space;n,&space;1\leq&space;v\leq&space;n}(\sim&space;x_{r,c,v}\vee&space;\sim&space;x_{r&plus;n,c,v})&space;" title="C_2 = \wedge_{1\leq r\leq n, 1\leq c\leq n, 1\leq v\leq n}(\sim x_{r,c,v}\vee \sim x_{r+n,c,v}) " />
* The solution respects the given clues H:<br/>
            <img src="https://latex.codecogs.com/svg.image?C_7&space;=&space;\wedge_{(r,c,v)\epsilon&space;H}(x_{r,c,v})&space;" title="C_7 = \wedge_{(r,c,v)\epsilon H}(x_{r,c,v}) " />

To get the Dimacs CNF variable number for the variable x<sub>r,c,v</sub> (encoding the fact that the cell at (r, c) has the value v, the following formula is used
–
```
(r - 1) * n * n + (c - 1) * n + (v - 1) + 1
```

The above clauses are passed to the **PySAT - Glucose 4.1 SAT solver** which generates a model if the formula is satisfiable, else returns None.

The generated model is then passed to a decoder to get the output in the form of a sudoku grid.

**Input Format :**

In the .csv file containing the sudoku pair - The first k<sup>2</sup> rows are for the first sudoku and the rest are for the second sudoku. Each row has k<sup>2</sup> cells. Each cell contains a number from 1 to k<sup>2</sup>. Cell with 0 specifies an empty cell.

**Usage :**
```
python3 sudoku_solver.py k input_sudoku_file.csv
```

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


## Sudoku Pair Generator – Implementation

The following steps were followed for sudoku generation –

1. Generating a random sudoku pair solution board where all the numbers are filled in. This will ensure that the puzzle always has a solution.<br/>

Let’s take an example for k = 3,<br/>
Shuffling rows is broken down in groups of 3 rows. It is ok to swap groups, but we cannot swap rows or columns across groups without breaking the integrity of the blocks. (the same reasoning applies to columns)<br/><br/>
For example,
```
0 [6, 2, 5,  8, 4, 3,  7, 9, 1] \                 -|
1 [7, 9, 1,  2, 6, 5,  4, 8, 3] |  group 0 -|     -| r in shuffle(rBase) 
2 [4, 8, 3,  9, 7, 1,  6, 2, 5] /           |     -|
                                            |
3 [8, 1, 4,  5, 9, 7,  2, 3, 6] \           |     -|
4 [2, 3, 6,  1, 8, 4,  9, 5, 7] |  group 1 -| *   -| r in shuffle(rBase)
5 [9, 5, 7,  3, 2, 6,  8, 1, 4] /           |     -|
                                            |
6 [5, 6, 9,  4, 3, 2,  1, 7, 8] \           |     -|
7 [3, 4, 2,  7, 1, 8,  5, 6, 9] |  group 2 -|     -| r in shuffle(rBase)
8 [1, 7, 8,  6, 5, 9,  3, 4, 2] /                 -|

                                * for g in shuffle(rBase)
```
We can swap groups 0,1,2 by moving all 3 of their rows at the same time:
```
3 [8, 1, 4,  5, 9, 7,  2, 3, 6] \           |     -|
4 [2, 3, 6,  1, 8, 4,  9, 5, 7] |  group 1 -|     -| r in shuffle(rBase)
5 [9, 5, 7,  3, 2, 6,  8, 1, 4] /           |     -|
                                            |
6 [5, 6, 9,  4, 3, 2,  1, 7, 8] \           |     -|
7 [3, 4, 2,  7, 1, 8,  5, 6, 9] |  group 2 -| *   -| r in shuffle(rBase)
8 [1, 7, 8,  6, 5, 9,  3, 4, 2] /                 -|
                                            |
0 [6, 2, 5,  8, 4, 3,  7, 9, 1] \           |     -|
1 [7, 9, 1,  2, 6, 5,  4, 8, 3] |  group 0 -|     -| r in shuffle(rBase) 
2 [4, 8, 3,  9, 7, 1,  6, 2, 5] /           |     -|

                                * for g in shuffle(rBase)
```
And we can swap between the 3 rows of a group (e.g. 3,4,5) ...
```
0 [6, 2, 5,  8, 4, 3,  7, 9, 1] \                 -|
1 [7, 9, 1,  2, 6, 5,  4, 8, 3] |  group 0 -|     -| r in shuffle(rBase) 
2 [4, 8, 3,  9, 7, 1,  6, 2, 5] /           |     -|
                                            |
5 [9, 5, 7,  3, 2, 6,  8, 1, 4] \           |     -|
4 [2, 3, 6,  1, 8, 4,  9, 5, 7] |  group 1 -| *   -| r in shuffle(rBase)
3 [8, 1, 4,  5, 9, 7,  2, 3, 6] /           |     -|
                                            |
6 [5, 6, 9,  4, 3, 2,  1, 7, 8] \           |     -|
7 [3, 4, 2,  7, 1, 8,  5, 6, 9] |  group 2 -|     -| r in shuffle(rBase)
8 [1, 7, 8,  6, 5, 9,  3, 4, 2] /                 -|

                                * for g in shuffle(rBase)
```
We CANNOT swap rows across groups (e.g. 1 <--> 3):
```
0 [6, 2, 5,  8, 4, 3,  7, 9, 1] \                 -|
3 [8, 1, 4,  5, 9, 7,  2, 3, 6] |  group 0 -|     -| r in shuffle(rBase) 
2 [4, 8, 3,  9, 7, 1,  6, 2, 5] /           |     -|
                                            |
1 [7, 9, 1,  2, 6, 5,  4, 8, 3] \           |     -|
4 [2, 3, 6,  1, 8, 4,  9, 5, 7] |  group 1 -| *   -| r in shuffle(rBase)
5 [9, 5, 7,  3, 2, 6,  8, 1, 4] /           |     -|
                                            |
6 [5, 6, 9,  4, 3, 2,  1, 7, 8] \           |     -|
7 [3, 4, 2,  7, 1, 8,  5, 6, 9] |  group 2 -|     -| r in shuffle(rBase)
8 [1, 7, 8,  6, 5, 9,  3, 4, 2] /                 -|

                                * for g in shuffle(rBase)
```
*See the duplicate 8 in the top left block, duplicate 7 below that, etc.*

2. Remove 70% of the numbers from the sudoku pair
3. Check if there is only one solution<br/>
   - Use the constraints discussed above (for sudoku solver) and pass them to the PySAT solver.<br/>
   - Add a clause to forbid the solution just found by inverting it (negation).<br/>
   - Use the PySAT solver to find a new solution and so forth...<br/>
   - Continue the above till the formula is unsatisfiable.
4. If there is more than one solution, add numbers back to the board from the sudoku till there is only one way to solve it.
Select a position where the two solutions (given by SAT solver) differ (this will converge faster to a single solution puzzle).

**Usage :**
```
python3 sudoku_generator.py
```
A prompt asking the user for input (k) will appear.


## Limitations

1. The Sudoku Solver takes about 120-130 secs to solve a sudoku pair when k = 4
2. Since the Sudoku Generator is based on randomness, it may take as low as 2 secs to as high as 1200 secs to generate a sudoku pair when k = 3
3. The Sudoku Solver and Generator is not tested for k > 4 since it may exhaust available resources.
