from math import sqrt


class SudokuTable:
    def __init__(self, table):
        self.table = table.copy()
        self.table_len = int(sqrt(len(table)))
        initial_domain = list(range(1, self.table_len + 1))
        self.domain = {}
        for i in range(0, self.table_len):
            for j in range(0, self.table_len):
                if not self.table[i * self.table_len + j]:  # is empty
                    self.domain[(i, j)] = list(filter(lambda x: x not in self.get_constrains(i, j), initial_domain))

        self.count_empty_variables = table.count(0)

    def __str__(self):
        s = ''
        for i in range(0, self.table_len):
            s=s+str(self.table[i*self.table_len:(i+1)*self.table_len])+'\n'
        return s

    def get_constrains(self, i, j):
        # row constrains
        constrains = self.table[i * self.table_len:(i + 1) * self.table_len]

        # column constrains
        for a in range(0, self.table_len):
            constrains.append(self.table[a * self.table_len + j])

        # inner table constrains
        a = int(sqrt(self.table_len))
        x = int(i / a)
        y = int(j / a)
        for i in range(x * a, (x + 1) * a):
            for j in range(y * a, (y + 1) * a):
                constrains.append(self.table[i * self.table_len + j])

        constrains = list(set(constrains))
        constrains.remove(0)
        return constrains

    def set_domain_values(self):
        initial_domain = list(range(1, self.table_len + 1))
        self.domain = {}
        for i in range(0, self.table_len):
            for j in range(0, self.table_len):
                if not self.table[i * self.table_len + j]:  # is empty
                    self.domain[(i, j)] = list(filter(lambda x: x not in self.get_constrains(i, j), initial_domain))

    def update_domain(self,i,j,value):
        domain=self.domain
        for x in range(0,self.table_len):
            if x!=j and domain.get((i,x)) and (value in domain.get((i,x))):
                domain[(i,x)].remove(value)
            if x!=i and domain.get((x,j)) and (value in domain.get((x,j))):
                domain[(x,j)].remove(value)

        a = int(sqrt(self.table_len))
        x = int(i / a)
        y = int(j / a)
        for m in range(x * a, (x + 1) * a):
            for n in range(y * a, (y + 1) * a):
                if (m != i or n!=j) and domain.get((m,n)) and (value in domain.get((m,n))):
                    domain[(m,n)].remove(value)



    def set_variable(self, i, j, value):
        self.table[i * self.table_len + j] = value

    def remove_variable(self, i, j):
        self.table[i * self.table_len + j] = 0



    def select_unassigned_variable(self, choice):
        if choice is 0:  # first cell that is empty
            pos = self.table.index(0)
            return int(pos / self.table_len), int(pos % self.table_len)


        if choice is 1:  # minimum remaining value
            min_length=self.table_len
            for i in range(0,self.table_len):
                for j in range(0, self.table_len):
                    if self.table[i*self.table_len+j] is 0:
                        if len(self.domain[(i,j)])<min_length:
                            min_length=len(self.domain[(i,j)])
                            x,y=i,j
            return x,y


        if choice is 2: #degree heuristic
            max_degree=-1
            for i in range(0,self.table_len):
                for j in range(0, self.table_len):
                    if not self.table[i * self.table_len + j]:
                        count=self.table[i*self.table_len:(i+1)*self.table_len].count(0)
                        for a in range(0, self.table_len):
                            if not self.table[a*self.table_len+j]:
                                count += 1
                        a = int(sqrt(self.table_len))
                        m = int(i / a)
                        n = int(j / a)
                        for k in range(m * a, (m+ 1) * a):
                            for l in range(n * a, (n + 1) * a):
                                if not self.table[k * self.table_len + l]:
                                    count += 1
                        count -= 3
                        if count>max_degree:
                            max_degree=count
                            x,y=i,j
            #print('xy=',x,y)
            return x,y



    def order_domain_values(self, choice, i, j):
        #self.set_domain_values()
        if choice is 0:  # in order
            return sorted(self.domain[(i, j)])

    def is_consistent(self,i,j,value):
        constrains=self.get_constrains(i,j)
        if value not in constrains:
            return True
        return False
