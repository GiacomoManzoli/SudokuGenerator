#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv



def build_sudoku_from_string(sudoku_str):
    result = {}
    for i in range(9):
        for j in range(9):
            char = sudoku_str[i*9+j]
            #print char
            if char != '-':
                result[(i,j)] = int(sudoku_str[i*9+j])
    assert len(result.keys()) == 25
    return result

def to_string(sudoku):
    start = '┌'
    end = '└'
    for i in range(9):
        start += "─"
        end += "─"
        if (i == 2 or i == 5):
            start += "┬"
            end += "┴"
    start += "┐\n"
    end += "┘\n"
    for i in range(9):
        row = '│'
        for j in range(9):
            row += str(sudoku[(i,j)]) if (i,j) in sudoku.keys() else ' '
            if (j == 2 or j == 5):
                row += "│"
        row+="│\n"
        if (i == 2 or i == 5):
            row+="├───┼───┼───┤\n"
        start+=row
    return start + end


sudokus = []

with open('./Archivio/sudokus_ok.csv', 'rb') as f:
    reader = csv.reader(f, delimiter=';')

    for row in reader:
        if row[0] == 'method':
            continue # salta la prima riga
        method = row[0] 
        sudoku_str = row[1]
        if sudoku_str == 'TIMEOUT':
            continue
        sudoku = build_sudoku_from_string(sudoku_str)
        sudokus.append((method,sudoku))
        print to_string(sudoku)

results = {}

for (method,sudoku) in sudokus:

    if not method in results:
        results[method] = {}

    for k in sudoku.keys():
        if k in results[method].keys():
            results[method][k] += 1
        else:
            results[method][k] = 1


rgba = {}

for method in results:
    print '--------- ', method, '----------'
    print results[method]
    print '--------------------------------'

    rgba[method] = {}
    sudoku = results[method]
    # find max
    max_val = 0
    for k in sudoku.keys():
        if sudoku[k] > max_val:
            max_val = sudoku[k]
    for i in range(9):
        for j in range(9):
            rgba[method][(i,j)] = 0
    for k in sudoku.keys():
        rgba[method][k] = int(100*sudoku[k]/max_val)

    print rgba[method]

    #33CCFF

#CSS
css = '.cell { width: 30px; height:30px}'
for i in range(101):
    css += '.bg-'+str(i)+' { background-color: rgba(0, 205, 255, '+str(i/float(100))+'); background: rgba(0, 205, 255, '+str(i/float(100))+'); } \n'

# Page start
start = '<html><head><style>\n'+css+'\n</style></head><body>'
end = '</body></html>'

page = ''
for method in rgba:
    sudoku = rgba[method]
    table = '<h1>'+method+'</h1>\n<table>'
    for i in range(9):
        table += '<tr>'
        for j in range(9):
            table+= '<td class="cell bg-'+str(sudoku[(i,j)])+'">&nbsp</td>'
        table += '</tr>'
    table += '</table>'
    page += table

print start + page + end

