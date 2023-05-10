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

FILE_NAME = "model4.json"

from classes import Vector, Matrix
from file_handler import read_from_json
from numerical_methods import gaus_method, scalar_product_method

def main(): 
    '''Recover info from json file'''
    model = read_from_json(FILE_NAME)
    for key in model:
        value = model[key]
        if key == 'C':
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

    '''set base coefficients for first interaction'''
    index = 0
    CB = Vector()   # base coefficients vector
    CN = Vector()   # non base coefficients vector
    for coeff in C:
        if index < B.get_size_columns():
            CB.insert_item(coeff)
        else:
            CN.insert_item(coeff)
        index += 1

    '''Find Transposed Xs' values'''
    XsT = gaus_method(B,b)
    print('values of Xs:')
    print('{}\n'.format(XsT)) 

    '''History of changes'''
    print('base:')
    print(CB)
    print('non-base:')
    print(CN)

    '''Show current value for the f(x)'''
    print('f(x) = {}\n'.format(scalar_product_method(XsT,CB)))

    while 1:
        '''Find BT'''
        BT = Matrix()
        for j in range(B.get_size_columns()):
            row = []
            for i in range(B.get_size_columns()):
                row.append(B.get_item(i,j))
            BT.insert_row(row)

        '''Find transposed lambda vector'''
        # Let's use Gauss Method to solve equations
        lambT = gaus_method(BT, CB)

        '''Calculate Xb'''
        Xb = Vector(gaus_method(B, b))

        '''Find non-basic costs'''
        Cxn = []
        for i in range(CN.rows):
            Cxn.append(CN.get_item(i) - scalar_product_method(lambT,Vector(A.get_column(i))))
        
        '''Show relatives'''
        print('Values of Cxn')
        print(Cxn)
        print('==============')

        '''Get the lower one and make a decision'''
        lower = min(Cxn)
        lower_key = Cxn.index(lower)
        keyboard = int(input('0 to exit or other to continue: '))
        if lower < 0 and keyboard:
            # there's an x that can minimize f(x)

            '''Find y related to candidate Cxn[i]'''
            y = Vector(gaus_method(B, Vector(A.get_column(lower_key))))

            '''Find epsolon'''
            epsolon = 10000
            epsolon_key = 0
            for i in range(y.get_size()):
                if y.get_item(i) > 0:
                    holder = Xb.get_item(i)/y.get_item(i)
                    if epsolon > holder:
                        epsolon = holder
                        epsolon_key = i

            '''Recover info from base and non-base matrices'''
            base_column_epsolon = B.get_column(epsolon_key)
            non_base_column_lower = N.get_column(lower_key)
            base_coeff_epsolon = CB.get_item(epsolon_key)
            non_base_coeff_lower = CN.get_item(lower_key)
            
            '''Column swap'''
            B.set_column(epsolon_key, non_base_column_lower)
            N.set_column(lower_key, base_column_epsolon)
            CB.set_item(epsolon_key, non_base_coeff_lower)
            CN.set_item(lower_key, base_coeff_epsolon)

            '''Find Transposed Xs' values'''
            XsT = gaus_method(B,b)
            print('values of Xs:')
            print('{}\n'.format(XsT)) 

            '''History of changes'''
            print('base:')
            print(CB)
            print('non-base:')
            print(CN)

            '''Show current value for the f(x)'''
            print('f(x) = {}\n'.format(scalar_product_method(XsT,CB)))

            '''keep loop'''

        else:
            # already solution

            '''Find Transposed Xs' values'''
            XsT = gaus_method(B,b)
            print('values of Xs:')
            print('{}\n'.format(XsT)) 

            '''History of changes'''
            print('base:')
            print(CB)
            print('non-base:')
            print(CN)

            '''Show current value for the f(x)'''
            print('f(x) = {}\n'.format(scalar_product_method(XsT,CB)))

            '''stop loop'''
            break

if __name__ == "__main__":
    main()