import numpy as np
from classes import Vector, Matrix

def scalar_product_method(V1n: list, Vn1: Vector) -> float:
    if len(V1n) != Vn1.get_size():
        raise ValueError("Tamanhos incompatíveis entre o vetor V1n e o objeto Vector")

    result = 0
    for i in range(len(V1n)):
        result += V1n[i] * Vn1.get_item(i)
    
    return result

def gaus_method(coeff, stakes):
    # CAMPOS, Frederico Ferreira. Algoritmos Numericos. Editora LTC, 2001.

    '''
    EX.:
        ax = b

        [4;-6;5][x1]   [29]
        [-2;8;1][x2] = [-15]
        [1;-3;2][x3]   [11]

        L   multi_factor               a              b    operation
        1   m11 = -(4)/1 = -4           4;-6; 5      29   
        2   m21 = -(-2)/1 = 2          -2; 8;-1     -15
        3                               1;-3; 2      11
        4   m12 = -(6)/2 = -3           0; 6;-3     -15    m11*L3 + L1
        5                               0; 2; 3       7    m31*L3 + L2
        6                               0; 0;-12    -36    m12*L5 + L4

        a = [ 0; 0;-12]
            [ 0; 2; 3 ]
            [ 1;-3; 2 ]

        b = [ 11 ]
            [  7 ]
            [-36 ]

        x3 = -36/-12 = 3
        x2 = (7 - 3*3)/2 = -1
        x1 = (11 - (-3)*(-1) - (2)*(3))/1 = 2
    '''

    a = Matrix(coeff.items)  # Copy the matrix instead of inserting rows one by one
    b = Vector(stakes.items)  # Copy the vector instead of inserting items one by one

    row_already_used_as_pivot = []
    multipliers = []
    c = 0
    while c < a.get_size_columns():
        # Find a pivot for column c
        pivot_line_index = 0
        while pivot_line_index >= 0:
            pivot = a.get_item(pivot_line_index, c)
            if pivot != 0 and pivot_line_index not in row_already_used_as_pivot:
                row_already_used_as_pivot.append(pivot_line_index)
                break
            else:
                pivot_line_index += 1

        # Find multipliers for other lines
        multipliers.append([])
        for i in range(a.get_size_rows()):
            if i != pivot_line_index:
                multipliers[c].append(-a.get_item(i, c) / pivot)
            else:
                multipliers[c].append(0)
        
        # Update rows and subtract mci*pivot_row from other rows
        pivot_L = a.get_row(pivot_line_index)
        for i in range(a.get_size_rows()):
            if i not in row_already_used_as_pivot:
                L = a.get_row(i)
                L = np.add(np.multiply(multipliers[c][i], pivot_L), L)
                a.set_row(i, L)

                item = b.get_item(i)
                b.set_item(i, multipliers[c][i] * b.get_item(pivot_line_index) + item)

        c += 1

    # Solve for variables
    X = [0 for _ in range(a.get_size_columns())]
    i = a.get_size_rows() - 1
    while i >= 0:
        sum = 0
        for j in range(a.get_size_columns()):
            sum += a.get_item(i, j) * X[j]
        sum = b.get_item(i) - sum
        X[i] = sum / a.get_item(i, i)
        i -= 1

    return X