from sudoku_table import SudokuTable
from time import time
from copy import deepcopy
from math import sqrt

def backtrack(table,SUV,ODV):
    sudoku=SudokuTable(table)
    result=recursive_backtrack({},sudoku,SUV,ODV)
    print(sudoku)


def recursive_backtrack(assignment,sudoku,SUV,ODV):
    if len(assignment)==sudoku.count_empty_variables:
        return assignment
    i,j=select_unassigned_variable(sudoku,choice=SUV)
    #print('i',i,'j',j)
    #print(sudoku)
    last_domain = deepcopy(sudoku.domain)
    for value in sudoku.order_domain_values(choice=ODV,i=i,j=j):
        #print(value)
        if sudoku.is_consistent(i,j,value):
            assignment[(i,j)]=value
            sudoku.set_variable(i,j,value)
            sudoku.domain=deepcopy(last_domain)
            sudoku.update_domain(i,j,value)
            result=recursive_backtrack(assignment,sudoku,SUV,ODV)
            if result:
                return result
            assignment.pop((i,j))
            sudoku.domain=deepcopy(last_domain)

            sudoku.remove_variable(i,j)
    return False


def select_unassigned_variable(sudoku, choice):
    if choice is 0:  # first cell that is empty
        pos = table.index(0)
        return int(pos / sudoku.table_len), int(pos % sudoku.table_len)

    if choice is 1:  # minimum remaining value
        pos=minimum_remaining_value(sudoku)
        return pos[0]

    if choice is 2: # MRV+ degree heuristic
        pos=minimum_remaining_value(sudoku)
        return degree_heuristic(sudoku,pos)

def order_domain_values(self, choice, i, j):
    if choice is 0:  # in order
        return sorted(self.domain[(i, j)])
    if choice is 1:
        pass


def minimum_remaining_value(sudoku):
    min_length = sudoku.table_len
    for i in range(0, sudoku.table_len):
        for j in range(0, sudoku.table_len):
            if sudoku.table[i * sudoku.table_len + j] is 0:
                if len(sudoku.domain[(i, j)]) < min_length:
                    min_length = len(sudoku.domain[(i, j)])
                    pos = [(i, j)]
                elif len(sudoku.domain[(i, j)]) == min_length:
                    pos.append((i, j))
    return pos


def degree_heuristic(sudoku,pos):
    max_degree = -1
    for i, j in pos:
        if not sudoku.table[i * sudoku.table_len + j]:
            count = sudoku.table[i * sudoku.table_len:(i + 1) * sudoku.table_len].count(0)
            for a in range(0, sudoku.table_len):
                if not sudoku.table[a * sudoku.table_len + j]:
                    count += 1
            a = int(sqrt(sudoku.table_len))
            m = int(i / a)
            n = int(j / a)
            for k in range(m * a, (m + 1) * a):
                for l in range(n * a, (n + 1) * a):
                    if not sudoku.table[k * sudoku.table_len + l]:
                        if k != i or l != j:
                            count += 1
                        if k == i and l == j:
                            count += 1
            count -= 3
            if count > max_degree:
                max_degree = count
                x, y = i, j
    return x, y

# table=[0, 4, 0, 1,
#        0, 0, 0, 0,
#        2, 0, 0, 0,
#        0, 1, 0, 0]

# backtrack(table,0,0)

table=[5,3,0,0,7,0,0,0,0,
       6,0,0,1,9,5,0,0,0,
       0,9,8,0,0,0,0,6,0,
       8,0,0,0,6,0,0,0,3,
       4,0,0,8,0,3,0,0,1,
       7,0,0,0,2,0,0,0,6,
       0,6,0,0,0,0,2,8,0,
       0,0,0,4,1,9,0,0,5,
       0,0,0,0,8,0,0,7,9]
t=time()
backtrack(table,1,0)
t1=time()-t
print(t1)
t=time()
backtrack(table,2,0)
t1=time()-t
print(t1)

