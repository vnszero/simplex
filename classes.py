class Matrix:
    def __init__(self, data=None):
        self.rows = 0
        self.columns = 0
        self.items = []
        if data is not None:
            for row in data:
                self.items.append(list(row))
                self.columns = max(self.columns, len(row))
                self.rows += 1
    
    def __str__(self):
        output = ''
        for i in range(self.rows):
            output += '[    '
            for j in range(self.columns):
                if j < len(self.items[i]):
                    output += str(self.items[i][j])+'   '
                else:
                    output += '0    '  # Fill missing values with 0
            output += ']\n'
        return output

    def insert_row(self, row):
        self.items.append(list(row))
        self.columns = max(self.columns, len(row))
        self.rows += 1
    
    def get_item(self, r, c):
        if r < self.rows and c < self.columns:
            return self.items[r][c]
        else:
            raise IndexError("Index out of range")

    def get_size_rows(self):
        return self.rows

    def get_size_columns(self):
        return self.columns
    
    def get_row(self, r):
        if r < self.rows:
            return self.items[r]
        else:
            raise IndexError("Index out of range")

    def set_row(self, r, L):
        if r < self.rows:
            self.items[r] = list(L)
        else:
            raise IndexError("Index out of range")
    
    def get_column(self, c):
        if c < self.columns:
            return [self.items[r][c] if c < len(self.items[r]) else 0 for r in range(self.rows)]
        else:
            raise IndexError("Index out of range")

    def set_column(self, c, K):
        if c < self.columns:
            for r in range(self.rows):
                if r < len(self.items[r]):
                    self.items[r][c] = K[r]
                else:
                    self.items[r].append(K[r])
        else:
            raise IndexError("Index out of range")

class Vector:
    def __init__(self, data=None):
        self.rows = 0
        self.items = []
        if data is not None:
            self.items = list(data)
            self.rows = len(data)
        
    def __str__(self):
        output = ''
        for i in self.items:
            output += '[    '+str(i)+'  ]\n'
        return output

    def insert_item(self, item):
        self.items.append(item)
        self.rows += 1
    
    def get_item(self, r):
        if r < self.rows:
            return self.items[r]
        else:
            raise IndexError("Index out of range")

    def set_item(self, r, item):
        if r < self.rows:
            self.items[r] = item
        else:
            raise IndexError("Index out of range")

    def get_size(self):
        return self.rows