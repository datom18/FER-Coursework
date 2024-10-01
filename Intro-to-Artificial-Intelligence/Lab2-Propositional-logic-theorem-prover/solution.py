import sys

# Sources used:
# https://www.pythontutorial.net/python-oop/python-__hash__/
# https://eng.lyft.com/hashing-and-equality-in-python-2ea8c738fb9d

#################################### CLASSES ####################################

class Literal:

    def __init__(self, name, negated=False):
        self.name = name
        self.negated = negated
    
    def __str__(self):
        res = ""
        if self.negated:
            res += "~"
        res += self.name
        return res
    
    def __eq__(self, other):
        return isinstance(other, Literal) and self.name == other.name and self.negated == other.negated
    
    def __hash__(self):
        return hash((self.name, self.negated))

class Clause:

    def __init__(self, literals, parents=(None, None)):
        self.literals = set(literals)
        self.parents = parents
    
    def __str__(self):
        l = 1
        res = ""
        for literal in self.literals:
            if l != len(self.literals):
                res += str(literal) + " v "
            else:
                res += str(literal)
            l += 1

        return res

    def __eq__(self, other):
        return isinstance(other, Clause) and self.literals == other.literals
    
    def __hash__(self):
        return hash(frozenset(self.literals))

    def checkComplementary(self, other):
        for literal in self.literals:
            complement = Literal(literal.name, not literal.negated)
            if complement in other.literals:
                return True
        return False
    
    def resolve(self, other):
        resolvents = []
        for literal in self.literals:
            complement = Literal(literal.name, not literal.negated)
            if complement in other.literals:
                resolvent = self.literals.union(other.literals) - {literal, complement}
                if len(resolvent) == 0:
                    resolvents.append(Clause({Literal("NIL", False)}, (self, other)))
                else:
                    resolvents.append(Clause(resolvent, (self, other)))
        return resolvents
    
    def isRedundant(self):
        for literal in self.literals:
            complement = Literal(literal.name, not literal.negated)
            if complement in self.literals:
                return True
        return False
    
#################################### LOADING ####################################

filepath = ""
cooking_filepath = ""
cooking_filepath_input = ""
wanted_function = ""
arguments = sys.argv


if "resolution" in arguments:
    wanted_function = "resolution"
    filepath = arguments[2]

if "cooking" in arguments:
    wanted_function = "cooking"
    cooking_filepath = arguments[2]
    cooking_filepath_input = arguments[3]


def loadResolutionData(filepath):
    
    clauses = []
    with open(filepath, "r", encoding="utf-8") as file:
        lines = []
        for line in file:
            if not line.startswith("#"):
                lines.append(line.rstrip("\n").lower())

    idx = 0
    for line in lines:
        idx += 1
        literals = set() 
        goal_literals = set()
        var = line.split(" v ")
        if idx != len(lines):
            for l in var:
                if l.startswith("~"):
                    literals.add(Literal(l[1:], True))
                else:
                    literals.add(Literal(l, False))
        else:
            for l in var:
                if l.startswith("~"):
                    literals.add(Literal(l[1:], False))
                    goal_literals.add(Literal(l[1:], True))
                else:
                    literals.add(Literal(l, True))
                    goal_literals.add(Literal(l, False))
        
        clauses.append(Clause(literals))
        goal = Clause(goal_literals)

    return clauses, goal

def loadCookingData(filepath):

    clauses = []
    with open(filepath, "r", encoding="utf-8") as file:
        lines = []
        for line in file:
            if not line.startswith("#"):
                lines.append(line.rstrip("\n").lower())

    idx = 0
    for line in lines:
        idx += 1
        literals = set() 
        var = line.split(" v ")
        for l in var:
            if l.startswith("~"):
                literals.add(Literal(l[1:], True))
            else:
                literals.add(Literal(l, False))
 
        clauses.append(Clause(literals))
        
    return clauses
    
def loadCookingInputData(filepath):
    tasks = []
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            tasks.append(line.rstrip("\n"))
    return tasks


#################################### ACCESSORY FUNCTIONS ####################################

def printElements(l):
    for i in l:
        print(i)

def sublist(smaller, larger):
    for clause in smaller:
        if clause not in larger:
            return False
    return True

def addToList(original, addition):
    for el in addition:
        original.append(el)
    return original


def cleanClauses(clauses):
    result = set()
    for clause in clauses:
        if not clause.isRedundant():
            result.add(clause)
    remove_clauses = set()
    for c1 in result:
        for c2 in result:
            if c1 != c2:
                if c1.literals.issubset(c2.literals):
                    remove_clauses.add(c2)
    result = result - remove_clauses
    return result


#################################### ALGORITHM ####################################

def selectClauses(clauses, support, visited):
    result = []
    for c_i in clauses:
        for c_j in support:
            if c_i not in visited or c_j not in visited:
                if c_i.checkComplementary(c_j) and c_i != c_j:               
                    result.append((c_i, c_j))    
    return result

def plResolution(clauses):
    start_clauses = clauses[0:len(clauses)-1] 
    goal_clause = clauses[-1]
    support = set()
    if len(goal_clause.literals) == 1:    
        support = {clauses[-1]}
        start_clauses.append(clauses[-1])
    else:
        for literal in goal_clause.literals:
            support.add(Clause({literal}))
            goal_clause = Clause({literal})
            start_clauses.append(goal_clause)
    visited = set()

    temp = clauses
    clauses = set() # turning clauses to set() after loading for better performance
    clauses.update(temp)
    clauses = cleanClauses(clauses)

    while True:
        resolvents = []
        new = []
        nil = Clause({Literal("NIL")})

        for clausePair in selectClauses(clauses, support, visited):
            
            resolvents = clausePair[0].resolve(clausePair[1])
            visited.update([clausePair[0], clausePair[1]])
            
            if nil in resolvents:
                last_clause = resolvents[-1]
                used_clauses = []
                usedClauses(last_clause, used_clauses)
                printSolution(used_clauses, start_clauses)
                return True
            new = addToList(new, resolvents)
        if sublist(new, clauses):
            return False    
        clauses.update(new) 
        clauses = cleanClauses(clauses)
        support.update(new)
        support = cleanClauses(support)


#################################### ALG. STEPS ####################################

def usedClauses(clause, used_clauses):
    if clause.parents != (None, None):
        for parent in clause.parents:
            usedClauses(parent, used_clauses)
    if (clause, clause.parents) not in used_clauses:
        used_clauses.append((clause, clause.parents))
        

def printSolution(used_clauses, start_clauses):
    temp = []
    for clause in start_clauses:
        temp.append((clause, clause.parents))
    start_clauses = temp

    numerics = {}
    i = 1            
    for clause in start_clauses:
        if clause in used_clauses:
            cl, parents = clause
            if parents == (None, None):
                numerics.update({cl : i})
                print(str(i) + ". " + str(cl))            
                i+= 1
    print("===============")
    for clause in used_clauses:
        cl, parents = clause
        if parents != (None, None):
            numerics.update({cl : i})
            print(str(i) + ". " + str(cl) + " (" + str(numerics.get(parents[0])) + ", " + str(numerics.get(parents[1])) + ")")  
            i += 1  
    print("===============")

#################################### MAIN ####################################

if wanted_function == "resolution":
    clauses, goal = loadResolutionData(filepath)
    solved = plResolution(clauses)
    if solved:
        print("[CONCLUSION]: " + str(goal) + " is true")
    else:
        print("[CONCLUSION]: " + str(goal) + " is unknown")

if wanted_function == "cooking":
    clauses = loadCookingData(cooking_filepath)
    tasks = loadCookingInputData(cooking_filepath_input)
    
    for task in tasks:
        command = task[len(task)-1]
        clause = task[:-1].lower().rstrip(" ")

        if command == "?":

            print("User’s command: " + str(clause) + " ?")

            literals = set()
            goal_literals = set()
            if clause.startswith("~"):
                literals.add(Literal(clause[1:], False))
                goal_literals.add(Literal(clause[1:], True))
            else:
                literals.add(Literal(clause, True))
                goal_literals.add(Literal(clause, False))
            
            clauses.append(Clause(literals))
            goal = Clause(goal_literals)

            solved = plResolution(clauses)
            if solved:
                print("[CONCLUSION]: " + str(goal) + " is true")
            else:
                print("[CONCLUSION]: " + str(goal) + " is unknown")  

            clauses.remove(clauses[-1])
            print()
        

        if command == "+":
            
            print("User’s command: " + str(clause) + " +")
            print("Added " + str(clause))

            literals = set() 
            var = clause.split(" v ")
            for l in var:
                if l.startswith("~"):
                    literals.add(Literal(l[1:], True))
                else:
                    literals.add(Literal(l, False))
    
            clauses.append(Clause(literals))  
            print()
            

        if command == "-":

            print("User’s command: " + str(clause) + " -")
            print("Removed " + str(clause))

            literals = set() 
            var = clause.split(" v ")
            for l in var:
                if l.startswith("~"):
                    literals.add(Literal(l[1:], True))
                else:
                    literals.add(Literal(l, False))
        
            clause = Clause(literals)
            clauses.remove(clause)
            print()
        
