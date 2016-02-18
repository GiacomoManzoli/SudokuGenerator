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
   
    def __init__(self, kind='linear'):
        self.__kind = kind


    def generate_sudoku(self, target = 25):
        search = AStarSearch()

        base_sudoku = self.generate_full_sudoku()
        timer = Timer()
        
        if self.__kind == 'reverse':
            problem = ReverseSudokuGenerationProblem(Sudoku(), target)
        else:
            problem = SudokuGenerationProblem(base_sudoku, target)

        timer.start()
        node, cnt_explored = search.search(problem, h = lambda n: problem.value(n.state))
        time = timer.stop()
        return node.state, len(node.state), cnt_explored, time


class SudokuGenerationProblem(Problem):
    
    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal.  Your subclass's constructor can add
        other arguments."""
        self.initial = initial;
        self.goal = goal
        self.__sudoku_solver = SudokuSolver()
        

    def actions(self, state):
        # state : Sudoku
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        # Le azioni possibili in un determinato stato
        # sono la rimozione di un elemento nella cella (i,j)
        # state.filled_cell() ritorna la lista di chiavi degli elementi del sudoku
        # l'ordinamento della lista è dato dal valore hash delle chiavi
        actions = state.filled_cell()
        #actions.sort() # Richiede un tempo bliblico
        random.shuffle(actions) # Richiede un tempo altrettanto bibblico
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
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        new_state = state.copy()
        new_state.clear_cell(action) 
        return new_state

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough."""
        (sols, b, t) = self.__sudoku_solver.solve(state, max_sol = 2)
        print 'Diff: %s (Target: %s)' % (len(state), self.goal)
        print 'Sols: ', len(sols)
        return len(state) == self.goal and len(sols) == 1

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        #return c + 1
        return 0

    def value(self, state):
        """For optimization problems, each state has a value.  Hill-climbing
        and related algorithms try to minimize this value."""
        
        # Minimo numero di celle da pulire per raggiungere la difficoltà desiderata
        assert state != None
        min_cell = len(state) - self.goal
        # min_cell deve essere una sotto stima del numero di mosse necessarie, non può
        # essere una valore negativo
        min_cell = 0 if min_cell < 0 else min_cell
        (sols, b, t) = self.__sudoku_solver.solve(state, max_sol = 2)

        if len(sols) == 1:
            return min_cell
        else:
            # Valore alto, in modo che l'algoritmo A* metta il nodo in fondo alla coda
            return 10000

class ReverseSudokuGenerationProblem(Problem):
    
    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal.  Your subclass's constructor can add
        other arguments."""
        self.initial = initial;
        self.goal = goal
        self.__sudoku_solver = SudokuSolver()
        

    def actions(self, state):
        # state : Sudoku
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        # Le azioni possibili in un determinato stato
        # sono la rimozione di un elemento nella cella (i,j)
        # state.filled_cell() ritorna la lista di chiavi degli elementi del sudoku
        # l'ordinamento della lista è dato dal valore hash delle chiavi
        actions = state.empty_cells()
        actions = [(a,v) for a in actions for v in range(1,10)]
        #actions.sort() # Richiede un tempo bliblico
        random.shuffle(actions) # Richiede un tempo altrettanto bibblico
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
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        new_state = state.copy()
        new_state.set_cell(action[0], action[1]) 
        return new_state

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough."""
        
        print 'Diff: %s (Target: %s)' % (len(state), self.goal)
        if len(state) != self.goal:
            return False
        (sols, b, t) = self.__sudoku_solver.solve(state, max_sol = 2)
        
        print 'Sols: ', len(sols)
        return len(state) == self.goal and len(sols) == 1

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        #return c + 1
        return 0

    def value(self, state):
        """For optimization problems, each state has a value.  Hill-climbing
        and related algorithms try to minimize this value."""
        
        # Minimo numero di celle da settare per raggiungere la difficoltà desiderata
        assert state != None
        min_cell = self.goal - len(state)
        # min_cell deve essere una sotto stima del numero di mosse necessarie, non può
        # essere un valore negativo
        min_cell = 0 if min_cell < 0 else min_cell
        
        #(sols, b, t) = self.__sudoku_solver.solve(state, max_sol = 2)

        return min_cell
        #if len(sols) == 1 or min_cell != 0:
        #    return min_cell
        #else:
        #    # Valore alto, in modo che l'algoritmo A* metta il nodo in fondo alla coda
        #    return 10000
