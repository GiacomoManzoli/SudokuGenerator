#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sudoku import Sudoku, SudokuSolver, SudokuDifficulty, SudokuGenerator
from util import Timer

import random

class ReverseSudokuGenerator(SudokuGenerator):
    '''
    Classe per la generazione di Sudoku partendo da un sudoku vuoto
    '''
   
    def generate_sudoku(self, target = 25):
        solver = SudokuSolver()
        sudoku = Sudoku()
        timer = Timer()
        step = 0
        timer.start()
        while True:
            solutions, _, _ = solver.solve(sudoku, max_sol = 2)
            if len(sudoku) == target and len(solutions) == 1:
                return sudoku, len(sudoku), step, timer.stop()
            step += 1
            # 2 casi possibili:
            # - non abbastanza numeri --> aggiungo un nuovo numero
            # - abbastanza numeri ma più di una soluzione o nessuna
            #       --> tolgo un numero a caso e ne aggiungo uno nuovo

            if len(sudoku) < target:
                cell_to_fill = random.choice(sudoku.empty_cells())
                # uso un valore che probabilmente porterà ad un sudoku feasible
                values = solver.feasible_values(sudoku, cell_to_fill)
                assert len(values) > 0, 'Non ci sono valori'
                value = random.choice(values)
                sudoku.set_cell(cell_to_fill, value)
                print sudoku
            else:
                cell_to_clear = random.choice(sudoku.filled_cell())
                sudoku.clear_cell(cell_to_clear)

        

