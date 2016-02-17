#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sudoku import Sudoku, SudokuSolver

import random

class SudokuGenerator(object):
    '''
    Classe base per il generatore di Sudoku
    '''
    def generate_full_sudoku(self):
        ''' Crea un sudoku completo '''
        box_list = [b for box in Sudoku.BOXES for b in box]
        solver = SudokuSolver()
        while True:
            # Popola alcune celle del sudoku casualmente
            # il while true serve perché il random può generare dei sudoku infeasible
            seed = {}
            for i in range(9):
                b = random.choice(box_list)
                seed[b] = random.randint(1,9)
                
            (sols, b, t) = solver.solve(Sudoku(seed), max_sol = 10)
            if len(sols) > 0:
                return random.choice(sols)

    def generate_sudoku(self, target):
        abstract
