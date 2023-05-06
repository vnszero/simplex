'''
    f = - x1 - 2x2
    x1+x2<=6
    x1-x2<=4
    -x1+x2<=4

    x3 + x2 = 6 => x3 = 2
    x4 - x2 = 4 => x4 = 8
    x2 = 4      => x2 = 4
'''

FILE_NAME = res = "model.json"

import json
import numpy

class Matrix:
    def __init__(self, data=0) -> None:
        self.rows = 0
        self.columns = 0
        self.items = []
        if not data == 0:
            for row in data:
                self.columns = 0
                self.items.append([])
                for item in row:
                    self.items[self.rows].append(item)
                    self.columns += 1
                self.rows += 1
    
    def __str__(self) -> str:
        # output = str(self.rows)+' x '+str(self.columns)+'\n'
        output = ''
        for i in range(self.rows):
            output += '[\t'
            for j in range(self.columns):
                output += str(self.items[i][j])+'\t'
            output += ']\n'
        return output

    def insert_row(self, row:list) -> None:
        self.items.append([])
        self.columns = 0
        for item in row:
            self.items[self.rows].append(item)
            self.columns += 1
        self.rows += 1
    
    def get_item(self, r:int, c:int) -> float:
        return self.items[r][c]
    
    def get_size_rows(self) -> int:
        return self.rows

    def get_size_columns(self) -> int:
        return self.columns
    
    def get_row(self, r:int) -> list:
        row = []
        for c in range(self.columns):
            row.append(self.items[r][c])
        return row

    def set_row(self, r:int, L:list) -> None:
        for c in range(self.columns):
            self.items[r][c] = L[c]
    
    def get_column(self, c:int) -> list:
        column = []
        for r in range(self.rows):
            column.append(self.items[r][c])
        return column

    def set_column(self, c:int, K:list) -> None:
        for r in range(self.rows):
            self.items[r][c] = K[r]

class Vector:
    def __init__(self, data=0) -> None:
        self.rows = 0
        self.items = []
        if not data == 0:
            for item in data:
                self.items.append(item)
                self.rows += 1
        
    def __str__(self) -> str:
        # output = str(self.rows)+'\n'
        output = ''
        for i in self.items:
            output += '[ '+str(i)+' ]\n'
        return output

    def insert_item(self, item:float):
        self.items.append(item)
        self.rows += 1
    
    def get_item(self, r:int) -> float:
        return self.items[r]

    def set_item(self, r:int, item:float) -> None:
        self.items[r] = item

    def get_size(self) -> int:
        return self.rows      

def read_from_json():
    file = open(FILE_NAME, "r", encoding="utf-8")
    model = json.load(file)
    file.close()
    return model

def gaus_jordan_method(coeff:Matrix, stakes:Vector) -> Vector:
    '''Gaus Jordan'''
    '''ax = b'''
    # to avoid memory sharing of variables from main
    # must create then again to keep their values
    a = Matrix()
    b = Vector()
    for r in range(coeff.get_size_rows()):
        a.insert_row(coeff.get_row(r))
    # print(a)

    for r in range(stakes.get_size()):
        b.insert_item(stakes.get_item(r))
    # print(b)

    '''
    EX.:
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

    x1 = -36/-12 = 3
    x2 = (7 - 3*3)/2 = -1
    x3 = (11 - (-3)*(-1) - (2)*(3))/1 = 2
    '''

    row_already_used_as_pivot = []
    m = [] #matrix m is a transposed matrix
    c = 0
    while c < a.get_size_columns():
        # print(c)
        '''Lets find a pivot for column c'''
        pivot_line_index = 0
        while(pivot_line_index >= 0):
            pivot = a.get_item(pivot_line_index, c)
            if pivot != 0 and not (pivot_line_index in row_already_used_as_pivot):
                row_already_used_as_pivot.append(pivot_line_index)
                break
            else:
                # find another pivot
                # assuming that there is always a valid pivot in column
                pivot_line_index += 1
        # print(pivot)

        '''with the pivot, lets find multiplayers for other lines'''
        m.append([])
        for i in range(a.get_size_rows()):
            if i != pivot_line_index:
                # saving multiplier for that line
                m[c].append(-a.get_item(i,c)/pivot)
            else:
                # pivot's line will not change
                m[c].append(0)
        # print(m)
        
        '''recover rows and sub mci*pivot_row from other rows'''
        pivot_L = a.get_row(pivot_line_index)
        for i in range(a.get_size_rows()):
            if not i in row_already_used_as_pivot:
                
                # coeff
                L = a.get_row(i)
                # print('----------------')
                # print('{}*{}'.format(m[c][i], pivot_L))
                # print('{} + {}'.format(numpy.multiply(m[c][i],pivot_L), L))
                L = numpy.add(numpy.multiply(m[c][i],pivot_L), L)
                # print(L)
                # print('----------------')
                a.set_row(i, L)

                # stakes
                item = b.get_item(i)
                
                # print('{}*{}+{}'.format(m[c][i],b.get_item(pivot_line_index),item))
                b.set_item(i, m[c][i]*b.get_item(pivot_line_index) + item)

        '''to the next column'''
        c += 1
    # print(a)
    # print(b)

    '''finally find values for variables'''
    X = [0 for x in range(a.get_size_columns())]
    i = a.get_size_rows() - 1
    while(i >= 0):
        sum = 0
        for j in range(a.get_size_columns()):
            sum += a.get_item(i,j)*X[j]
            # print("s = {}*{}".format(a.get_item(i,j),X[j]))
        # print("{} - {}".format(b.get_item(a.get_size_rows() - 1 - i), sum))
        sum = b.get_item(i) - sum
        X[i] = sum/a.get_item(i, i)
        i -= 1
    # print(X)

    return X

def scalar_product(V1n, Vn1) -> float:
    sum = 0
    for i in range(len(V1n)):
        sum += V1n[i]*Vn1[i]
    return sum

def main():
    
    '''Recover info from json file'''
    model = read_from_json()
    for key in model:
        value = model[key]
        # print("{}: {}".format(key, value))
        if key == 'goal':
            goal = value
        elif key == 'C':
            # The order matters, so C cant be a dict
            C = value
        elif key == 'A':
            A = Matrix(value)
        elif key == 'B':
            B = Matrix(value)
        elif key == 'N':
            N = Matrix(value)
        elif key == 'b':
            b = Vector(value)
    # print(C)
    # print(A)
    # print(B)
    # print(N)
    # print(b)

    '''make a first interaction'''
    '''Find BT'''
    BT = Matrix()
    for j in range(B.get_size_columns()):
        row = []
        for i in range(B.get_size_columns()):
            row.append(B.get_item(i,j))
        BT.insert_row(row)
    # print(BT)

    '''set base coefficients'''
    index = 0
    CB = Vector()   # base coefficients vector
    CN = Vector()   # non base coefficients vector
    for coeff in C:
        if index < B.get_size_columns():
            CB.insert_item(coeff)
        else:
            CN.insert_item(coeff)
        index += 1
    # print(CB)
    # print(CN)
    
    '''Find Lambda'''
    # at first lambda vector will be declared as [1 1 1]
    # Let us use Gauss Jordan Method to solve equations
    lambT = gaus_jordan_method(BT, CB)
    lamb = Vector(lambT)
    # print(lamb)

    # Let us calculate Xb
    Xb = Vector(gaus_jordan_method(B, b))
    # print(Xb)

    # Let us find non basic costs
    Cxn = []
    lower = 10 # any number greater then zero must work
    lower_key = 0
    for i in range(CN.rows):
        Cxn.append(CN.get_item(i) - scalar_product(lambT,A.get_column(i)))
        if lower > Cxn[i]:
            lower = Cxn[i]
            lower_key = i
    # print(lower)
    # print(lower_key)

    # if there is a Cx[c] < 0:
    if lower < 0:
        # find y related to the candidate Cxn[i]
        y = Vector(gaus_jordan_method(B, Vector(A.get_column(lower_key))))
        # print(y)

        # find epsolon
        epsolon = 10000
        epsolon_key = 0
        for i in range(y.get_size()):
            if y.get_item(i) > 0:
                holder = Xb.get_item(i)/y.get_item(i)
                if epsolon > holder:
                    epsolon = holder
                    epsolon_key = i
        # print(epsolon)
        # print(epsolon_key)

        # show new base and non base
        # print(C)
        # print(B)
        # print(CB)
        # print(N)
        # print(CN)
        # print('========')

        # recover info from base and non base matrices
        base_column_epsolon = B.get_column(epsolon_key)
        non_base_column_lower = N.get_column(lower_key)
        func_coeff_epsolon = C[epsolon_key]
        func_coeff_lower = C[lower_key + 3]
        base_coeff_epsolon = CB.get_item(epsolon_key)
        non_base_coeff_lower = CN.get_item(lower_key)
        
        # column swap
        B.set_column(epsolon_key, non_base_column_lower)
        N.set_column(lower_key, base_column_epsolon)
        C[epsolon_key] = func_coeff_lower
        C[lower_key + 3] = func_coeff_epsolon
        CB.set_item(epsolon_key, non_base_coeff_lower)
        CN.set_item(lower_key, base_coeff_epsolon)

        # show new base and non base
        # print(C)
        # print(B)
        # print(CB)
        # print(N)
        # print(CN)
        # print('========')

        # find the values to Xs
        Xs = gaus_jordan_method(B,b) 
        # print(B)
        # print(Xs)
        # print(b)

        # show the current value for the f(x)
        print(C[:3])
        print(scalar_product(Xs,C[:3]))

        # keep loop
    # else:
        # already solution

        # break

    # show function final value

if __name__ == "__main__":
    main()