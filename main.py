#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sudoku import RandomSudokuGenerator, AStarSudokuGenerator, SudokuSolver, Sudoku, ReverseSudokuGenerator

solver = SudokuSolver()

test_solver = SudokuSolver()

generator_a = AStarSudokuGenerator(kind='linear')
generator_a_rev = AStarSudokuGenerator(kind='reverse', solver = test_solver)
generator_rand = RandomSudokuGenerator()
generator_rev = ReverseSudokuGenerator()

#s1, l1, x1, y1 = generator_a.generate_sudoku(target = 25)
#s2, l2, x2, y2 = generator_a_rev.generate_sudoku(target = 25)
s3, l3, x3, y3 = generator_rand.generate_sudoku(target = 24)
#s4, l4, x4, y4 = generator_rev.generate_sudoku(target = 25)


#(ss1, _, _) = solver.solve(s1, max_sol = 2)
#(ss2, _, _) = solver.solve(s2, max_sol = 2)
(ss3, _, _) = solver.solve(s3, max_sol = 2)
#(ss4, _, _) = solver.solve(s4, max_sol = 2)

#assert len(ss1) == 1, 'A* genera un sudoku con più di una soluzione'
#assert len(ss2) == 1, 'A*Rev genera un sudoku con più di una soluzione'
assert len(ss3) == 1, 'Rand genera un sudoku con più di una soluzione'
#assert len(ss4) == 1, 'Rev genera un sudoku con più di una soluzione'

print '########################################'
#print 'A* - Generato sudoku con %d numeri' % l1
#print x1, y1
#print s1
#print 'A*Reverse - Generato sudoku con %d numeri' % l2
#print x2, y2
#print s2
print 'Random - Generato sudoku con %d numeri' % l3
print x3, y3
print s3
#print 'ReverseRandom - Generato sudoku con %d numeri' % l4
#print x4, y4
#print s4
#print test_solver.feasible_values_calls, test_solver.infeasible_count, test_solver.solve_calls




