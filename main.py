'''
    problem:
    min(f(x)) = -x1 - 2*x2
    
    I)      x1 + x2 <= 6
    II)     x1 - x2 <= 4
    III)    -x1 + x2 <= 4
    IV)     xn >= 0

    standard shape:
    min(f(x)) = -x1 - 2*x2

    I)      x1 + x2 + x3 = 6
    II)     x1 - x2 + x4 = 4
    III)    -x1 + x2 + x5 = 4
    IV)     xn >= 0
    
'''

'''assuming that model is already in standard shape'''

from classes import Vector, Matrix
from file_handler import read_from_json
from numerical_methods import gaus_method, scalar_product_method

FILE_NAME = "model_salesman.json"

def find_optimal_solution(CB, CN, B, N, A, b):
    while True:
        BT = Matrix()
        for j in range(B.get_size_columns()):
            row = B.get_column(j)
            BT.insert_row(row)

        lambT = gaus_method(BT, CB)
        Xb = Vector(gaus_method(B, b))

        Cxn = []
        for i in range(CN.get_size()):
            column = Vector(A.get_column(i))
            Cxn.append(CN.get_item(i) - scalar_product_method(lambT, column))

        print('Values of Cxn')
        print(Cxn)
        print('==============')

        there_is_zero = False
        if 0 in Cxn:
            there_is_zero = True
        lower = min(Cxn)
        lower_key = Cxn.index(lower)
        keyboard = int(input('0 to exit or other to continue: '))
        if lower < 0 and not there_is_zero and keyboard:
            y = Vector(gaus_method(B, Vector(A.get_column(lower_key))))

            epsolon = 10000
            epsolon_key = 0
            for i in range(y.get_size()):
                if y.get_item(i) > 0:
                    holder = Xb.get_item(i) / y.get_item(i)
                    if epsolon > holder:
                        epsolon = holder
                        epsolon_key = i

            base_column_epsolon = B.get_column(epsolon_key)
            non_base_column_lower = N.get_column(lower_key)
            base_coeff_epsolon = CB.get_item(epsolon_key)
            non_base_coeff_lower = CN.get_item(lower_key)

            B.set_column(epsolon_key, non_base_column_lower)
            N.set_column(lower_key, base_column_epsolon)
            CB.set_item(epsolon_key, non_base_coeff_lower)
            CN.set_item(lower_key, base_coeff_epsolon)

            XsT = gaus_method(B, b)
            print('values of Xs:')
            print('{}\n'.format(XsT))

            print('base:')
            print(CB)
            print('non-base:')
            print(CN)

            print('f(x) = {}\n'.format(scalar_product_method(XsT, CB)))

        else:
            XsT = gaus_method(B, b)
            print('values of Xs:')
            print('{}\n'.format(XsT))

            print('base:')
            print(CB)
            print('non-base:')
            print(CN)

            print('f(x) = {}\n'.format(scalar_product_method(XsT, CB)))
            break

def main():

    model = read_from_json(FILE_NAME)

    variable_mapping = {
        'C': 'C',
        'A': 'A',
        'B': 'B',
        'N': 'N',
        'b': 'b'
    }

    variables = {}
    for key in model:
        value = model[key]
        if key in variable_mapping:
            variable_name = variable_mapping[key]
            variables[variable_name] = value

    CB = Vector()
    CN = Vector()
    for i, coeff in enumerate(variables['C']):
        if i < len(variables['B']):
            CB.insert_item(coeff)
        else:
            CN.insert_item(coeff)
    
    B = Matrix(variables['B'])
    b = Vector(variables['b'])
    XsT = gaus_method(B, b)
    print('values of Xs:')
    print('{}\n'.format(XsT))

    print('base:')
    print(CB)
    print('non-base:')
    print(CN)

    print('f(x) = {}\n'.format(scalar_product_method(XsT, CB)))

    B = Matrix(variables['B'])
    N = Matrix(variables['N'])
    A = Matrix(variables['A'])
    b = Vector(variables['b'])
    find_optimal_solution(CB, CN, B, N, A, b)


if __name__ == "__main__":
    main()