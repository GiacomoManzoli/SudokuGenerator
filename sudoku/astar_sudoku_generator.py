#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sudoku import Sudoku, SudokuSolver, SudokuDifficulty, SudokuGenerator
from search import Problem, AStarSearch
from util import PriorityQueue, Timer

import random

class AStarSudokuGenerator(SudokuGenerator):
    '''
    Classe per la generazione di Sudoku utilizzando l'algoritmo A*
    '''
   
    def __init__(self, solver = SudokuSolver(), kind='linear'):
        SudokuGenerator.__init__(self, solver)  
        self.__kind = kind


    def generate_sudoku(self, target = 25):
        search = AStarSearch()

        base_sudoku = self.generate_full_sudoku()
        timer = Timer()
        
        if self.__kind == 'reverse':
            problem = ReverseSudokuGenerationProblem(Sudoku(), target, self.solver)
        else:
            problem = SudokuGenerationProblem(base_sudoku, target, self.solver)

        timer.start()
        node, cnt_explored = search.search(problem, h = lambda n: problem.value(n.state))
        time = timer.stop()
        return node.state, len(node.state), cnt_explored, time


class SudokuGenerationProblem(Problem):
    
    def __init__(self, initial, goal=None, solver = SudokuSolver()):
        self.initial = initial;
        self.goal = goal
        self.__sudoku_solver = solver
        

    def actions(self, state):
        # state : Sudoku
        # Se lo stato corrente ha un numero sufficiente di elementi, non
        # è necessario creare nuove azioni, vengono così generati meno nodi
        # In ogni caso l'influenza sulle prestazioni è minima
        if len(state) == self.goal:
            return []
        # Le azioni possibili in un determinato stato
        # sono la rimozione di un elemento nella cella (i,j)
        # state.filled_cell() ritorna la lista di chiavi degli elementi del sudoku
        # l'ordinamento della lista è dato dal valore hash delle chiavi
        actions = state.filled_cell()
        random.shuffle(actions)
        return actions
        #good_actions = []
        #for action in actions:
        #    s = self.result(state, action)
        #    (sols, b, t) = self.__sudoku_solver.solve(s, max_sol =2)
        #    if len(sols) == 1:
        #        good_actions.append(action)
        #return good_actions

    def result(self, state, action):
        # state : Sudoku
        # action : (i,j)
        new_state = state.copy()
        new_state.clear_cell(action) 
        return new_state

    def goal_test(self, state):
        if len(state) != self.goal:
            return False
        (sols, b, t) = self.__sudoku_solver.solve(state, max_sol = 2)
        #print 'Diff: %s (Target: %s)' % (len(state), self.goal)
        #print 'Sols: ', len(sols)
        return len(sols) == 1

    def path_cost(self, c, state1, action, state2):
        return 0

    def value(self, state):
        # Minimo numero di celle da pulire per raggiungere la difficoltà desiderata
        min_cell = len(state) - self.goal
        # min_cell deve essere una sotto stima del numero di mosse necessarie, non può
        # essere una valore negativo
        min_cell = 0 if min_cell < 0 else min_cell
        
        # Conviene filtratre maggiormente
        #if min_cell != 0:
        #    return min_cell
        #return min_cell
        (sols, b, t) = self.__sudoku_solver.solve(state, max_sol = 2)

        if len(sols) == 1:
            return min_cell
        else:
            # Valore alto, in modo che l'algoritmo A* metta il nodo in fondo alla coda
            return 10000

class ReverseSudokuGenerationProblem(Problem):
    
    def __init__(self, initial, goal=None, solver = SudokuSolver()):
        self.initial = initial;
        self.goal = goal
        self.__sudoku_solver = solver
        

    def actions(self, state):
        # state : Sudoku
        if len(state) == self.goal:
            return []
        # Le azioni possibili in un determinato stato
        # sono la rimozione di un elemento nella cella (i,j)
        # state.filled_cell() ritorna la lista di chiavi degli elementi del sudoku
        # l'ordinamento della lista è dato dal valore hash delle chiavi
        actions = state.empty_cells()
        #actions = [(a,v) for a in actions for v in range(1,10)]
        print 'looking for actions'
        actions = [(a,v) for a in actions for v in self.__sudoku_solver.feasible_values(state,a)]
        random.shuffle(actions)
        return actions
        #good_actions = []
        #for action in actions:
        #    s = self.result(state, action)
        #    (sols, b, t) = self.__sudoku_solver.solve(s, max_sol =2)
        #    if len(sols) == 1:
        #        good_actions.append(action)
        #return good_actions

    def result(self, state, action):
        # state : Sudoku
        # action : ((i,j),v)
        new_state = state.copy()
        new_state.set_cell(action[0], action[1]) 
        return new_state

    def goal_test(self, state):
        
        #print 'Diff: %s (Target: %s)' % (len(state), self.goal)
        if len(state) != self.goal:
            return False
        (sols, b, t) = self.__sudoku_solver.solve(state, max_sol = 2)
        
        #print 'Sols: ', len(sols)
        return len(state) == self.goal and len(sols) == 1

    def path_cost(self, c, state1, action, state2):
        return 0

    def value(self, state):
        # Minimo numero di celle da settare per raggiungere la difficoltà desiderata
        assert state != None
        min_cell = self.goal - len(state)
        # min_cell deve essere una sotto stima del numero di mosse necessarie, non può
        # essere un valore negativo
        min_cell = 0 if min_cell < 0 else min_cell

        print 'valueate\n', state
        (sols, b, t) = self.__sudoku_solver.solve(state, max_sol = 2)
        print 'done', len(sols)
        #return min_cell
        if len(sols) == 1 or min_cell != 0:
            return min_cell
        else:
            # Valore alto, in modo che l'algoritmo A* metta il nodo in fondo alla coda
            return 10000
