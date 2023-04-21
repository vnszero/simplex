'''
    f=-x1+x2
    x1+x2<=6
    x1-x2<=4
    -x1+x2<=4
'''
import json

class Matrix:
    def __init__(self, data) -> None:
        self.rows = 0
        self.columns = 0
        self.items = []
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

class Vector:
    def __init__(self, data) -> None:
        self.rows = 0
        self.items = []
        for item in data:
            self.items.append(item)
            self.rows += 1
        
    def __str__(self) -> str:
        # output = str(self.rows)+'\n'
        output = ''
        for i in self.items:
            output += '[ '+str(i)+' ]\n'
        return output

def read_from_json():
    file = open("model.json", "r", encoding="utf-8")
    model = json.load(file)
    file.close()
    return model

def main():
    
    '''Recover info from json file'''
    model = read_from_json()
    for key in model:
        value = model[key]
        # print("{}: {}".format(key, value))
        if key == 'goal':
            goal = value
        elif key == 'C':
            C = Vector(value)
        elif key == 'A':
            A = Matrix(value)
        elif key == 'PX':
            PX = Vector(value)
        elif key == 'B':
            B = Matrix(value)
        elif key == 'N':
            N = Matrix(value)
        elif key == 'b':
            b = Vector(value)
    # print(A)
    # print(PX)
    # print(B)
    # print(N)
    # print(b)

if __name__ == "__main__":
    main()