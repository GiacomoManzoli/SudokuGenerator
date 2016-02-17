#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sudoku import RandomSudokuGenerator, AStarSudokuGenerator


generator = AStarSudokuGenerator()
#generator = RandomSudokuGenerator()

s, l, x, y = generator.generate_sudoku()

print 'Generato sudoku con %d numeri' % l

print s


