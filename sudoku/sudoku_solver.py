#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ortools.constraint_solver import pywrapcp

from sudoku import Sudoku


class SudokuSolver(object):

    def solve(self, sudoku, max_sol = 1):
        ''' Risolve un sudoku.
        - max_sol (int) specifica quante soluzioni devono essere cercate
        - sudoku (Sudoku) è l'oggetto che rappresenta il sudoku da risolvere
            se il sudoku non contiene alcun numero (è vuoto) viene utilizzata
            un'euristica di scelta delle variabili casualemente

        returns (solutions, branches, time)
        - solutions ([Sudoku]) lista di soluzioni
        - branches (int)
        - time (int)
        '''        
        sudoku_vals = sudoku.get_dict()
        
        slv = pywrapcp.Solver('sudoku_gen')

        # Variabili
        x = { (i,j) : slv.IntVar(1,9,'Cella %d,%d' %(i,j)) for i in range(9) for j in range(9)}

        # Vincoli
        for k in range(0,9):
            # Alldifferent sulle righe
            slv.Add(slv.AllDifferent([x[(k,j)] for j in range(9)],True)) 
            # Alldifferent sulle colonne
            slv.Add(slv.AllDifferent([x[(i,k)] for i in range(9)],True))
      
        # Vincolo tutti gli elementi di un quadrato diversi
        for box in Sudoku.BOXES:
            slv.Add(slv.AllDifferent([x[t] for t in box]))

        # Vincolo sui valori fissati
        for k in sudoku_vals:
            slv.Add( x[k] == sudoku_vals[k])

        all_vars = x.values()

        # Euristiche per il DecisionBuilder
        var_selection_strategy = slv.CHOOSE_MIN_SIZE_LOWEST_MIN # Più efficace per trovare una singola soluzione
        if sudoku_vals == {}:
            print 'RANDOM'
            var_selection_strategy = slv.CHOOSE_RANDOM # Utile per generare sudoku diversi se non ci sono valori fissati

        value_selection_strategy = slv.ASSIGN_RANDOM_VALUE # Maggiore casualità nella generazione, non influise nella risoluzione
        
        decision_builder = slv.Phase(all_vars, var_selection_strategy, value_selection_strategy)
        time_limit = 20000
        search_monitors = [slv.TimeLimit(time_limit)]
        #search_monitors.append(slv.SearchLog(500000))
        slv.NewSearch(decision_builder, search_monitors)

        solutions = []
        while slv.NextSolution():
            solutions.append(Sudoku({(i,j):x[(i,j)].Value() for i in range(9) for j in range(9)}))
            if len(solutions) == max_sol:
                break
            
        slv.EndSearch()

        # obtain stats
        branches, time = slv.Branches(), slv.WallTime()
        return solutions, branches, time
