from sudoku_table import SudokuTable
from time import time
from copy import deepcopy

def backtrack(table,SUV,ODV):
    sudoku=SudokuTable(table)
    result=recursive_backtrack({},sudoku,SUV,ODV)
    print(sudoku)


def recursive_backtrack(assignment,sudoku,SUV,ODV):
    if len(assignment)==sudoku.count_empty_variables:
        return assignment
    i,j=sudoku.select_unassigned_variable(choice=SUV)
    print('i',i,'j',j)
    print(sudoku)
    last_domain = deepcopy(sudoku.domain)
    for value in sudoku.order_domain_values(choice=ODV,i=i,j=j):
        print(value)
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






# table=[0, 3, 4, 0,
#        4, 0, 0, 2,
#        1, 0, 0, 3,
#        0, 2, 1, 0]

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
# # t=time()
# # backtrack(table,1,0)
# # t1=time()-t
# # print(t1)
t=time()
backtrack(table,1,0)
t1=time()-t
print(t1)

