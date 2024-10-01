import sys, math

# Sources used:
# https://www.geeksforgeeks.org/python-sort-dictionary-by-values-and-keys/

#################################### LOADING ####################################

training_filepath = ""
testing_filepath = ""
arguments = sys.argv

training_filepath = arguments[1]
testing_filepath = arguments[2]
depth_value = -1
if len(arguments) > 3:
    depth_value = int(arguments[3])

lines = []
with open(training_filepath, "r", encoding="utf-8") as file:
    for line in file:
        line = line.rstrip("\n")
        l = line.split(",")
        lines.append(l)

header = lines[0]
attributes = header[:-1]
class_label = header[-1]

dataset = []

for line in lines[1:]:
    d = {}
    for i in range(0, len(header)):
        d.update({header[i]: line[i]})
    dataset.append(d)

# TEST DATA LOADING
lines = []
with open(testing_filepath, "r", encoding="utf-8") as file:
    for line in file:
        line = line.rstrip("\n")
        l = line.split(",")
        lines.append(l)

test_data = []

for line in lines[1:]:
    d = {}
    for i in range(0, len(header)):
        d.update({header[i]: line[i]})
    test_data.append(d)


#################################### HELP CLASSES ####################################

class Leaf:
    def __init__(self, value):
        self.value = value
    
class Node:
    def __init__(self, attr, subtrees):
        self.attr = attr
        self.subtrees = subtrees


#################################### FUNCTIONS/ALGORITHM ####################################

def count_values(D, x=class_label):
    count = {}
    for el in D:
        v = el.get(x)
        if v in count:
            count[v] += 1
        else:
            count[v] = 1
    return count


def filter_dataset(D, x, v):
    new_D = []
    for el in D:
        if el.get(x) == v:
            new_D.append(el)
    return new_D


def mostCommonValue(D):
    d = count_values(D)
    res = {el[0] : el[1] for el in sorted(d.items(), key = lambda x: (-x[1], x[0]))}
    return max(res, key=res.get)


def entropy(D):
    count = count_values(D) 
    total = sum(count.values())
    res = 0
    for i in count.values():
        p = i / total
        res -= p * math.log2(p) 

    return res


def IG(D, x):
    entropy_D = entropy(D)
    total = sum(count_values(D).values())
    s = 0
    for val in count_values(D,x):
        new_D = filter_dataset(D, x, val)
        total_i = sum(count_values(new_D).values())
        s += (total_i / total) * entropy(new_D)

    return entropy_D - s    


def maxIG(D, X):
    ig_values = {}
    for i in X:
        ig_values.update({i: IG(D,i)}) 
    res = {el[0] : el[1] for el in sorted(ig_values.items(), key = lambda x: (-x[1], x[0]))}
    """ for k,v in res.items():
        print(f"IG({k})={v:.4f}", end=" ")
    print() """
    return max(res, key=ig_values.get)
    

def id3(D, D_parent, X, depth=-1):
    if not D:
        v = mostCommonValue(D_parent)
        return Leaf(v)
    v = mostCommonValue(D)
    if not X or entropy(D)==0 or depth == 0:
        return Leaf(v)
    x = maxIG(D, X)
    subtrees = []
    x_values = list(count_values(D, x).keys())
    x_values.sort()
    X.remove(x)
    for val in x_values:
        t = id3(filter_dataset(D, x, val), D, X, depth-1)  
        subtrees.append((val, t))
    X.append(x)
    return Node(x, subtrees)


def printTree(root, path=[]):
    if isinstance(root, Leaf):
        for i in range(0, len(path)):
            print(f"{i+1}:{path[i][0]}={path[i][1]}", end=" ")
        print(root.value)
    elif isinstance(root, Node):
        for value, subtree in root.subtrees:
            printTree(subtree, path + [(root.attr, value)])


def predict(tree, l):
    if isinstance(tree, Leaf):
        return tree.value
    elif isinstance(tree, Node):
        attr_value = l.get(tree.attr)
        for val, subtree in tree.subtrees:
            if attr_value == val:
                return predict(subtree, l)
    return mostCommonValue(test_data)


def evaluate(test_data):
    ans = []
    correct = 0
    total = len(test_data)
    for d in test_data:
        p = predict(tree, d)
        ans.append(p)
        if d.get(class_label) == p:
            correct += 1
    return ans, correct / total


def findElements(val1, val2, ans):
    count = 0
    for i in range(0, len(test_data)):
        if test_data[i].get(class_label) == val1 and ans[i] == val2:
            count += 1
    return count


def confusion_matrix(ans):
    val = count_values(test_data)
    val = list(val.keys())
    val.sort()
    y = len(val)
    for i in range(y):
        for j in range(y):
            count = findElements(val[i], val[j], ans)
            print(count, end= " ")
        print()


#################################### CLASS ####################################

class ID3:

    def __init__(self):
        pass

    def fit(self, dataset):
        tree = id3(dataset, dataset, attributes, depth_value)
        return tree
    
    def predict(self, test_dataset):
        answers, accuracy = evaluate(test_dataset)
        return answers, accuracy


#################################### MAIN ####################################

model = ID3()

tree = model.fit(dataset)
print("[BRANCHES]:")
printTree(tree)

answers, accuracy = model.predict(test_data)

print("[PREDICTIONS]:", end=" ")
for i in answers:
    print(i, end=" ")
print()

print("[ACCURACY]:", end=" ")
print(f"{accuracy:.5f}")

print("[CONFUSION_MATRIX]:")
confusion_matrix(answers)
