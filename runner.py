#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sudoku import RandomSudokuGenerator, AStarSudokuGenerator, SudokuSolver, Sudoku, ReverseSudokuGenerator

import csv
csv.register_dialect('lol', delimiter=';')

solver = SudokuSolver()
generator_a = AStarSudokuGenerator(kind='linear', solver = solver)
generator_rand = RandomSudokuGenerator(solver = solver)
generator_rev = ReverseSudokuGenerator(solver = solver)

times = 100
generators = [
    ('astar',generator_a), 
    ('random',generator_rand), 
    ('random_rev',generator_rev)
]

results = []

for name,g in generators:
    print 'Utilizzo il generatore: ', name
    for i in range(times):
        print 'Iterazione:', i
        # Azzera i valori, è una soluzione brutta, però non
        # è necessaria una bella soluzione
        solver.solve_calls = 0
        solver.feasible_values_calls = 0
        solver.infeasible_count = 0
        
        (s, c, n, t) = g.generate_sudoku(target = 25)
        
        results.append({
            'method':name,
            'sudoku':s.to_linear(),
            'visited':n,
            'time':t,
            'solve_calls': solver.solve_calls,
            'infeasible_count': solver.infeasible_count,
            'feasible_values_calls': solver.feasible_values_calls
            })

with open('sudokus.csv', 'w') as csvfile:
    fieldnames = ['method', 'sudoku', 'visited', 'time', 'solve_calls', 'infeasible_count', 'feasible_values_calls']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='lol')
    writer.writeheader()
    writer.writerows(results)


print 'USO A*REV'
g = AStarSudokuGenerator(solver = solver, kind = 'reverse')
for i in range(5):
    # Azzera i valori, è una soluzione brutta, però non
    # è necessaria una bella soluzione
    solver.solve_calls = 0
    solver.feasible_values_calls = 0
    solver.infeasible_count = 0
    
    (s, c, n, t) = g.generate_sudoku(target = 25)
    
    results.append({
        'method':name,
        'sudoku':s.to_linear(),
        'visited':n,
        'time':t,
        'solve_calls': solver.solve_calls,
        'infeasible_count': solver.infeasible_count,
        'feasible_values_calls': solver.feasible_values_calls
        })

with open('sudokus_astar_rev.csv', 'w') as csvfile:
    fieldnames = ['method', 'sudoku', 'visited', 'time', 'solve_calls', 'infeasible_count', 'feasible_values_calls']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='lol')
    writer.writeheader()
    writer.writerows(results)
