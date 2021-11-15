import numpy as np

class bubble:
    def __init__(self, left_bubble, right_bubble, operation : str):
        self.left_bubble = left_bubble
        self.right_bubble = right_bubble
        self.operation = operation
        self.is_core = False
        
    
    def print_bubble(self) -> str:
        return "("+self.left_bubble.print_bubble() + self.operation + self.right_bubble.print_bubble()+")"

    def calculate_bubble(self, var_dict) -> float:
        l, r =  self.left_bubble.calculate_bubble(var_dict), self.right_bubble.calculate_bubble(var_dict)
        if self.operation == "+":
            return l+r
        elif self.operation == "-":
            return l-r
        elif self.operation == "*":
            return l * r
        elif self.operation == "/":
            return l/r
        else:
            raise Exception("Invalid operation provided:", self.operation)
        

    def get_children(self):
        return self.left_bubble, self.right_bubble

    def get_cores(self, var_only=False):

        l, r = self.get_children()
        
        cores = l.get_cores(var_only=var_only).flatten(), r.get_cores(var_only=var_only).flatten()

        cores=np.unique(np.concatenate( cores, axis=0 ))
        return cores

    
        

class core_bubble(bubble):
    def __init__(self, core, is_numeric = False):
        self.core = core
        self.is_core = True
        self.is_numeric = is_numeric
    
    def get_cores(self, var_only = False):
        if var_only and self.is_numeric:
            return np.array([])
        
        return np.array([self.core])
        
    def calculate_bubble(self, var_dict) -> float:
        if self.is_numeric:
            return float(self.core)
        
        return var_dict[self.core]

    def print_bubble(self) -> str:
        return self.core

# Testing:

X = core_bubble("X")
Y = core_bubble("Y")

basic_bub1 = bubble(X, Y, "+")
basic_bub2 = bubble(X, Y, "/")

bub_3 = bubble(basic_bub1, basic_bub2, "+")
basic_bub3 = bubble(
    bubble(core_bubble("Z"), bub_3, "-"),
    core_bubble("2", is_numeric=True),
    "+"
    )

print(basic_bub3.print_bubble())

print(basic_bub3.get_cores())
print(basic_bub3.get_cores(var_only=True))

print(bubble(core_bubble("2", is_numeric=True), core_bubble("3", is_numeric=True), "+").calculate_bubble({}))
result = basic_bub3.calculate_bubble(var_dict = {'X' : 1, 'Y' : 1, 'Z':2})

print(result)