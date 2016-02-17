#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum

class SudokuDifficulty(Enum):
    Easy = 1
    Medium = 2
    Hard = 3
    Evil = 4

    @classmethod
    def range(diff):
        if diff == SudokuDifficulty.Easy:
            return range(36,82)
        elif diff == SudokuDifficulty.Medium:
            return range(31,36)
        elif diff == SudokuDifficulty.Hard:
            return range(26,31)
        else:
            return range(0,26)

class Sudoku(object):
    '''
    Classe che rappresenta un sudoku
    '''
    __dict = {}

    def __init__(self, dict={}):
        self.__dict = dict.copy()

    def to_string(self):
        s = ''
        for i in range(9):
            s += ' '.join('%d' % self.__dict[(i,j)] if (i,j) in self.__dict.keys() else '_' for j in range(9))
            s += '\n'
        return s

    def filled_cell(self):
        return self.__dict.keys()

    def clear_cell(self, key):
        self.__dict.pop(key, None)

    def set_cell(self, key, val):
        self.__dict[key] = val

    def cell(self, key):
        return self.__dict[key]

    def difficulty(self):
        cnt_cells = len(self)
        if cnt_cells in SudokuDifficulty.range(SudokuDifficulty.Easy):
            return SudokuDifficulty.Easy
        elif cnt_cells in SudokuDifficulty.range(SudokuDifficulty.Medium):
            return SudokuDifficulty.Medium
        elif cnt_cells in SudokuDifficulty.range(SudokuDifficulty.Hard):
            return SudokuDifficulty.Hard
        else:
            return SudokuDifficulty.Evil

    def copy(self):
        return Sudoku(self.__dict)

    def get_dict(self):
        '''
        Ritorna un dizionario del tipo {(i,j): v}
        '''
        return self.__dict.copy()

    def __str__(self):
        return self.to_string()

    def __len__(self):
        return len(self.filled_cell()) 

    BOXES = [
        [(0,0), (0,1), (0,2),
         (1,0), (1,1), (1,2),
         (2,0), (2,1), (2,2)],
        [(0,3), (0,4), (0,5),
         (1,3), (1,4), (1,5),
         (2,3), (2,4), (2,5)],
        [(0,6), (0,7), (0,8),
         (1,6), (1,7), (1,8),
         (2,6), (2,7), (2,8)],

        [(3,0), (3,1), (3,2),
         (4,0), (4,1), (4,2),
         (5,0), (5,1), (5,2)],
        [(3,3), (3,4), (3,5),
         (4,3), (4,4), (4,5),
         (5,3), (5,4), (5,5)],
        [(3,6), (3,7), (3,8),
         (4,6), (4,7), (4,8),
         (5,6), (5,7), (5,8)],

        [(6,0), (6,1), (6,2),
         (7,0), (7,1), (7,2),
         (8,0), (8,1), (8,2)],
        [(6,3), (6,4), (6,5),
         (7,3), (7,4), (7,5),
         (8,3), (8,4), (8,5)],
        [(6,6), (6,7), (6,8),
         (7,6), (7,7), (7,8),
         (8,6), (8,7), (8,8)]
    ]
