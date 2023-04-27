'''
    f=-x1+x2
    x1+x2<=6
    x1-x2<=4
    -x1+x2<=4
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

    def insert_row(self, row) -> None:
        self.items.append([])
        self.columns = 0
        for item in row:
            self.items[self.rows].append(item)
            self.columns += 1
        self.rows += 1
    
    def get_item(self, r, c) -> float:
        return self.items[r][c]
    
    def get_size_rows(self) -> int:
        return self.rows

    def get_size_columns(self) -> int:
        return self.columns
    
    def get_row(self, r) -> list:
        row = []
        for c in range(self.columns):
            row.append(self.items[r][c])
        return row

    def set_row(self, r, L) -> None:
        for c in range(self.columns):
            self.items[r][c] = L[c]

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

    def insert_item(self, item):
        self.items.append(item)
        self.rows += 1
    
    def get_item(self, r) -> float:
        return self.items[r]

    def set_item(self, r, item) -> None:
        self.items[r] = item        

def read_from_json():
    file = open(FILE_NAME, "r", encoding="utf-8")
    model = json.load(file)
    file.close()
    return model

def gaus_jordan_method(coeff, stakes) -> Vector:
    '''Gaus Jordan'''
    '''ax = b'''
    a = coeff
    b = stakes

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
        sum = b.get_item(i) - sum
        X[i] = sum/a.get_item(i, i)
        i -= 1
    # print(X)

    '''as you can see I'm a dumb and I found X vector reversed'''
    X = X[::-1]
    # print(X)

    return X

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
    for name,coeff in C:
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
    lamb = gaus_jordan_method(BT, CB)

    # Let us calculate Xb
    Xb = gaus_jordan_method(B, b)

    # Let us find non basic costs
    # while():
        # Cx[c] = CN[c] - lambT*a.get_column(c)
    
    # if there is a Cx[c] < 0:
        # find y related to the candidate Cx[c]

        # find epsolon

        # find new base and non base
        
        # show function current value

        # keep loop
    # else:
        # already solution

        # break

    # show function final value

if __name__ == "__main__":
    main()