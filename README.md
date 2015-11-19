# sudopy
A python implementation of a sudoku puzzle solver.

## Description
A sudoku puzzle is a 9x9 matrix of cells with a few of them already assigned a value from 1 to 9.
The objective of the puzzle is very simple: assign values to all the remaining cells in the board, such that each line, column and 3x3 square contains all the number from 1 to 9.
What makes sudoku an interesting puzzle is, besides its simplicity, the fact that every puzzle can always be completely solved using only the existing information on the board.
In other words, no guessing is necessary!

In this app I implemented a simple and powerful algorithm which is capable of solve any sudoku puzzle.
In my opinion, alternative brute-force algorithms are (probably) less efficient and certainly not elegant.

## The algorithm
Solving a sudoku puzzle is done by keeping track of the list of possible values for each cell.
A group of cells can be either a line, a column or a 3x3 square.
Then by inspecting groups of cells, it becomes possible to systematically eliminate possibilities until all the cells have only one possible value.
At this point the board is solved.

A general description of the algorithm follows.
We are going to loop all possible groups (lines, columns and squares) of cells until the board is solved.
We will try to sets of n-numbers which are exclusive to sets of n-cells.
So, let n be a number from 1 to 8.
For a given group of cells G, find the sub-group H with all cells that have at least n elements.
If there are less than n cells with n elements, continue to the next group of cells.
Otherwise, we are interested in finding all the n-cell combinations of H.
Let S be a n-cell combination of H and !S be the remaining cells in G which are not in S.
Now, compute the intersection I of all the possibilities in S.
If the size of I is less than n, continue to the next combination of cells S.
Now, we will search all possible n-element combination of the intersection we found.
So, let LP be the list of all n-element permutations of I.
For each P in LP, if no element of P is present in !S, then the list of possibilities of all cells in S is P.
If all cells in S only have P as possibility, then discard all the elements of P from !S.

After a few iterations of this algorithm the board will be solved.

## An example
Let's look at a hypothetical group of cells, name A to I, and their possible values:
| Cell | Possibilities |
| ---- | ------------- |
| A    | 14569 		   |
| B    | 1459		   |
| C    | 9			   |
| D    | 8		       |	
| E    | 167		   |	
| F    | 67			   |
| G    | 236		   |	
| H    | 2374		   |	
| I    | 67		       |

Let's start with the obvious cases. 
Cells CD only have one possible value, i.e., they are solved.
Therefore, values (8,9) must be discarded from the list of possibilities in the remaining cells.
Looking back at the algorithm, CD are cases of 1-cell group S with 1-possiblity P which are the only possibility of S, therefore all !S must be discarded of their P possibilities.
| Cell | Possibilities | Discarded |
| ---- | ------------- | --------- |
| A    | 1456          | 9         |
| B    | 145       	   | 9         |
| C    | 9             |           |
| D    | 8             |           |
| E    | 167           |           |      	
| F    | 67            |           |     	
| G    | 236           |           |      	
| H    | 2374          |           |       	
| I    | 67            |           |

Next, we can see that cells GH have two values in common: (2,3).
In fact, these are the only two cells with 2 or 3.
Therefore, 2 and 3 must be place in GH, and other possible values for cells GH can be discarded.
Referring to the algorithm, GH is a 2-cell group S with a 2-element intersection P which are only found in S.
Therefore, P must be the list of possibilities for all cells in S.
| Cell | Possibilities | Discarded |
| ---- | ------------- | --------- |
| A    | 1456          |           |
| B    | 145           |           |			
| C    | 9             |           |
| D    | 8             |           |
| E    | 167           |           |
| F    | 67            |           |
| G    | 23            | 6         |
| H    | 23            | 74        |
| I    | 67            |           |

With this example we have shown how to systematically discard possibilities from an arbitrary group of cells using the outlined algorithm.
By looping through all groups of cells in a sudoku puzzle, the solution is achieved, typically after 3 or 4 iterations.