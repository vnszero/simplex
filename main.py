'''
    f=-x1+x2
    x1+x2<=6
    x1-x2<=4
    -x1+x2<=4
'''
import json

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
    
    def get_item(self, r, c) -> int:
        return self.items[r][c]
    
    def get_size_rows(self) -> int:
        return self.rows

    def get_size_columns(self) -> int:
        return self.columns

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

def read_from_json():
    file = open("model.json", "r", encoding="utf-8")
    model = json.load(file)
    file.close()
    return model

def gaus_jordan_method(coeff, lamb, stakes) -> Vector:
    '''Gaus Jordan'''
    '''ax = b'''
    a = coeff
    x = lamb
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

    '''Use decomposition to find triangular matrix'''

    return 0

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
    one_data = [1 for x in range(B.get_size_columns())]
    lamb = Vector(one_data)
    # print(lamb)

    # Let us use Gauss Jordan Method to solve equations
    lamb = gaus_jordan_method(BT, lamb, CB)


if __name__ == "__main__":
    main()