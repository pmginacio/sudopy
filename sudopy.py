#!/usr/bin/env python
# -*- coding: utf-8; -*-
"""Solve a sudoky puzzle

Given a string which represent a sudoku puzzle, sudopy will output the solved 
puzzle.
"""

__author__ = "Pedro Inácio"
__copyright__ = "Copyright 2015"
__version__ = "1.0"
__maintainer__ = "Pedro Inácio"
__email__ = "pedro@inacio.space"
__status__ = "Development"

# Load modules
import re
import argparse
import itertools
from os import path

class Sudoku(object):
	"""A class that handles a single sudoku puzzle"""

	Board = None
	Squares = None
	Groups = None

	NSET = set([str(x) for x in range(1,10)])

	def __init__(self, sud):
		"""Constructor, recieves a string with a sudoku puzzle and builds the
		corresponding sudoku board.
		"""
		super(Sudoku, self).__init__()

		# build the board
		self.Board = [[self.NSET.copy() for col in range(9)] for row in range(9)]

		# gather the squares 
		self.Squares = [ list() for sq in range(9) ]
		for row in range(9):
			sq = row/3*3
			self.Squares[sq].extend(self.Board[row][0:3])
			self.Squares[sq+1].extend(self.Board[row][3:6])
			self.Squares[sq+2].extend(self.Board[row][6:9])

		# Gather all meaningful groups of cells
		self.Groups = self.Squares
		for i in range(9):
			# append rows
			self.Groups.append(self.Board[i])
			# append columns
			self.Groups.append([row[i] for row in self.Board])

		# now fill the board, all non-numbers are discarded except spaces which 
		# are zeros. Zeros mean no-value
		sud = sud.replace(' ','0')
		sud = re.sub('\n','',sud)
		sud = re.sub('[^0-9]','',sud)

		# fill the board, stop at 81
		item = 0
		for c in sud:
			row, col = divmod(item,9)
			
			if c != '0':
				self.set(row,col,c)

			item += 1
			if item == 81:
				break

	def __str__(self):
		""" 
		Print the board. The unique elements in the cell are the numbers in 
		the board
		"""
		out=''
		item = 0

		out += '-'*23+'\n'
		for row in range(9):
			out += '|'
			for col in range(9):

				cell = self.Board[row][col]
				if len(cell) == 1:
					for n in cell:
						out += '|'+n
				else:
					out += '| '

				if col == 8:
					out += '||\n'

				if col == 2 or col == 5:
				 	out += '|'

			if (row+1)%3 == 0:
				out += '-'*23+'\n'

		return out

	def set(self,row,col,c):
		"""Set a value in a cell, exclude row, line and square possibilities"""

		if c not in self.Board[row][col]:
			raise Exception('Value '+c+' is not possible in cell ('+
				str(row)+','+str(col)+')')

		# exclude possiblity from line and row and square
		sq = row/3*3 + col/3
		for x in range(9):
			self.Board[x][col] -= set(c)
			self.Board[row][x] -= set(c)
			self.Squares[sq][x] -= set(c)

		# restore as possibility
		self.Board[row][col].clear()
		self.Board[row][col].add(c)

	def solve(self,tmp=None):
		"""Loop all the groups of sets and exclude possibilities"""

		# Loop all groups of cells. i.e., squares, rows and columns
		change_flag = False

		# temporary
		if tmp is None:
			tmp = self.Groups

		for g in tmp:

			# Loop numbers from 8 to 1
			for n in range(1,10):

				# find all cells in this group with at least n possibilities
				idxs = list()
				[idxs.append(x) for x in range(9) if len(g[x]) >= n]

				# if found less that n cells, then continue to next group
				if len(idxs) < n:
					continue

				# for each combination of n cells
				for c in itertools.combinations(idxs,n):

					# get the corresponding sets
					A = list()
					[A.append(g[x]) for x in c]
					notA = list()
					[notA.append(g[x]) for x in range(9) if x not in c]

					# find the intersection and 
					itsc = self.NSET.copy()
					[itsc.intersection_update(x) for x in A]

					# check that there are at least n numbers in the intersection
					if len(itsc) < n:
						continue

					# now loop all n-element combinations of the intersection
					for aux in itertools.combinations(itsc,n):
						subset = set(aux)
					
						# check that each n-element subset of the intersection 
						# does not exist in any of the the other cells
						present_in_other_cells=False
						for x in subset:
							for cell in notA:
								if x in cell:
									present_in_other_cells=True

						# check if subset is the only possibility of the group
						only_poss = True
						for cell in A:
							if len(cell.difference(subset)) > 0:
								only_poss = False
								break

						# if not present in any other cells, then discard other 
						# possibilities. Only flag changes if there are other poss
						if not present_in_other_cells:
							for cell in A:
								if len(cell.difference(subset)) > 0:
									cell.intersection_update(subset)
									change_flag = True

						# if only possible in the group of cells, then discard 
						# possibilities from the other cells
						if only_poss and present_in_other_cells:
							for cell in notA:
								cell.difference_update(subset)
								change_flag = True

		return change_flag

	def _print_poss(self):
		"""Print the board with all the possibilities"""
		out=''
		item = 0
		out += '-'*37+'\n'
		for row in range(9):
			for sset in [ list('123'), list('456'), list('789') ]:
				out += '|'
				for col in range(9):
					cell = self.Board[row][col]
					if len(cell) == 1:
						if '5' in sset:
							for n in self.Board[row][col]:
								out += ' '+n+' '
						else:
							out += '   '
					else:
						for n in sset:
							if n in cell:
								out += n
							else:
								out += ' '
					out += '|'
				out += '\n'
			out += '-'*37+'\n'

		return out

def parse_args():
	"""Return a parser to take care of the input arguments"""

	# Define the input parser
	desc = "Solve a sudoku puzzle"
	epilog = """The single input argument specifies either a filename or a 
	string representation of a sudoku board. If a filename is given, the a string
	representation of the sudoku board is read from the contents of the file.

	A string representation is any collection of digits, where digits 1 to 9 
	represent the values of the respective cells. The board is read row by row,
	such that the 10-th digit in the string corresponds to the first element of
	the second row of the board.
	Zeros or spaces represent cells which have no value atributed.
	Other characters including newlines are discarded.
	"""

	parser = argparse.ArgumentParser(description=desc, epilog=epilog)
	parser.add_argument("sud",help="filename or string representing sudoku puzzle")

	return parser.parse_args()


def main():
	"""Parse input arguments, build the sudoku board, solve it and print it"""

	# build parser and parse the input arguments
	args = parse_args()

	# check if it is a file
	if path.isfile(args.sud):
		# load file as a string
		with open(args.sud,'r') as f:
			sudstr = f.read()
	# otherwise us the input string as the board
	else:
		sudstr = args.sud

	# build the sudoku puzzle data structure
	sud = Sudoku(sudstr)

	# loop until solved or until no changes have been made
	while sud.solve():
		pass

	# print the board
	print sud

# This idiom means the below code only runs when executed from command line
if __name__ == '__main__':
	main()
