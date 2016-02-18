#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sudoku import Sudoku, SudokuGenerator, SudokuSolver, SudokuDifficulty

from util import Timer
import random


class RandomSudokuGenerator(SudokuGenerator):

    def generate_sudoku(self, target = 25):
        '''
        Genera un sudoku rimuovendo casualemente dei valori fino a che non si ottiene un livello di difficoltà pari a quello specificato dal parametro target
        Ogni 1000 Backtrack ripristina metà valori scelti casualemente tra quelli rimossi

        returns (current_sudoku, len(current_sudoku), cnt_backtrack, time)
        '''
        base_sudoku = self.generate_full_sudoku()
        current_sudoku = Sudoku(base_sudoku.get_dict())

        solver = SudokuSolver()
        
        box_list = [b for box in Sudoku.BOXES for b in box]
        cache = [] # Cache dei valori per il backtrack
        cnt_backtrack = 0
        single_solution = False;
        timer = Timer()
        
        timer.start()
        while True:
            print '----------------------------'
            print 'Cache size', len(cache)
            # Test di uscita
            if len(current_sudoku) == target and single_solution:
                break;
            print 'Current values count: ', len(current_sudoku)
            print 'Single solution: ', single_solution
            print 'Backtrack', cnt_backtrack
            
            # Quanti valori togliere
            n = len(current_sudoku) / 20
            
            print 'Prova a rimuovere %d valori' %n
            assert n != 0
            # Togli i numeri
            for i in range(n):
                key = random.choice(current_sudoku.filled_cell())
                cache.append(key)
                current_sudoku.clear_cell(key)
            
            print 'Cache size', len(cache)

            # Verifica l'unicità della soluzione
            (sols, b, t) = solver.solve(current_sudoku, max_sol = 2)
            # Se unica, continua
            if len(sols) == 1:
                single_solution = True
                print "Rimossi con successo %d elementi" % n
                continue
            # Se più di una, torna indietro
            else:
                print "Backtrack, sols: %d" % len(sols)
                single_solution = False
                cnt_backtrack += 1

                # Ripristina gli ultimi n valori tolti
                print 'Restored cache size', len(cache)
                for i in range(n):
                    # Ripristina gli utlimi elementi tolti
                    k = cache[-1]
                    current_sudoku.set_cell(k, base_sudoku.cell(k))
                    cache.pop(-1)

                if cnt_backtrack % 1000 == 0:
                    print 'Riprista casualmente metà cache'
                    for i in range(len(cache)/2):
                        # Ripristina gli utlimi elementi tolti
                        idx = random.randint(0, len(cache)-1)
                        k = cache[idx]
                        current_sudoku.set_cell(k, base_sudoku.cell(k))
                        cache.pop(idx)

        print '----------------------------'
        print 'Backtrack necessari: ', cnt_backtrack
        time = timer.stop()
        return current_sudoku, len(current_sudoku), cnt_backtrack, time