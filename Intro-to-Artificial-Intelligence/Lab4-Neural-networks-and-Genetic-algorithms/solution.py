import numpy as np
import sys

# Sources used:
# https://www.w3schools.com/python/numpy/numpy_random_normal.asp
# https://www.geeksforgeeks.org/numpy-random-choice-in-python/

#################################### LOADING ####################################


arguments = sys.argv
training_path, testing_path, nn_architecture = "", "", ""
popsize, elitism, probability, std_gauss, iterations = 0, 0, 0, 0, 0

for i in range(0, len(arguments)-1):
    if arguments[i] == "--train":
        training_path = arguments[i+1]
    if arguments[i] == "--test":
        testing_path = arguments[i+1]
    if arguments[i] == "--nn":
        nn_architecture = arguments[i+1]
    if arguments[i] == "--popsize":
        popsize = int(arguments[i+1])
    if arguments[i] == "--elitism":
        elitism = int(arguments[i+1])
    if arguments[i] == "--p":
        probability = float(arguments[i+1])
    if arguments[i] == "--K":
        std_gauss = float(arguments[i+1])
    if arguments[i] == "--iter":
        iterations = int(arguments[i+1])

# TRAIN SET
lines = []
with open(training_path, "r") as file:
    for line in file:
        line = line.rstrip("\n")
        l = line.split(",")
        lines.append(l)

header = lines[0]
attributes = header[:-1]
class_label = header[-1]

arr_attrs, arr_output = [], []
train_set_attributes, train_set_output = [], []

for line in lines[1:]:
    l1, l2 = [], []
    for i in range(0, len(header)):
        if header[i] != class_label:
            l1.append(float(line[i]))
        else:
            l2.append(float(line[i]))
    arr_attrs.append(l1)
    arr_output.append(l2)

train_set_attributes = np.array(arr_attrs)
train_set_output = np.array(arr_output)

# TEST SET
lines = []
with open(testing_path, "r") as file:
    for line in file:
        line = line.rstrip("\n")
        l = line.split(",")
        lines.append(l)

arr_attrs, arr_output = [], []
test_set_attributes, test_set_output = [], []
for line in lines[1:]:
    l1, l2 = [], []
    for i in range(0, len(header)):
        if header[i] != class_label:
            l1.append(float(line[i]))
        else:
            l2.append(float(line[i]))
    arr_attrs.append(l1)
    arr_output.append(l2)

test_set_attributes = np.array(arr_attrs)
test_set_output = np.array(arr_output)

layers = [str(1)]
for i in nn_architecture.split("s")[:-1]:
    layers.append(i)
layers.append(str(1))

#################################### NEURAL NETWORK ####################################


class NN:
    def __init__(self, dataset):
        self.dataset = dataset
        self.hidden_size = [int(l) for l in layers]
        self.input_size = [len(attributes)] + [l for l in self.hidden_size[1:-1]]
        self.weights = None
        self.bias = None
        self.error = None
        self.fitness = None

    def __lt__(self, other):
        return self.fitness < other.fitness

    def generate_weights(self):
        self.weights = [np.random.normal(loc=0, scale=0.01, size=(self.hidden_size[i], self.input_size[i - 1]))
                        for i in range(1, len(self.hidden_size))]

    def generate_bias(self):
        self.bias = [np.random.normal(loc=0, scale=0.01, size=(1, self.hidden_size[i])) for i in
                     range(1, len(self.hidden_size))]

    def set_weights(self, weights):
        self.weights = weights

    def set_bias(self, bias):
        self.bias = bias

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    def predict(self, output_set):
        results = []
        for instance in self.dataset:
            input_vector = instance
            for layer in range(0, len(layers)-1):
                res = np.dot(self.weights[layer], input_vector.T) + self.bias[layer]
                res = res[0]
                if layer != len(layers)-2:
                    res = NN.sigmoid(res)
                input_vector = res
            results.append(res)

        # ERROR
        sum = 0
        for i in range(0, len(results)):
            sum += (output_set[i] - results[i])**2
        err = (1 / len(results)) * sum
        self.error = err
        self.fitness = 1 / err

    def pair(self, other):
        child = NN(self.dataset)
        child_weights = []
        for w1, w2 in zip(self.weights, other.weights):
            child_weights.append((w1 + w2) / 2)
        child_bias = []
        for w1, w2 in zip(self.bias, other.bias):
            child_bias.append((w1 + w2) / 2)
        child.set_weights(child_weights)
        child.set_bias(child_bias)
        return child

    def mutate(self):
        for layer in self.weights:
            for weights in layer:
                for i in range(0, len(weights)):
                    if np.random.rand() < probability:
                        weights[i] += np.random.normal(loc=0, scale=std_gauss)

        for layer in self.bias:
            for bias in layer:
                for i in range(0, len(bias)):
                    if np.random.rand() < probability:
                        bias[i] += np.random.normal(loc=0, scale=std_gauss)

#################################### GENETIC ALGORITHM ####################################


class Generation:
    def __init__(self, individuals):
        self.individuals = np.sort(individuals)[::-1]
        self.individual_fitness = [ind.fitness for ind in self.individuals]
        p = []
        for i in range(len(self.individuals)):
            p.append((self.individuals[i].fitness / np.sum(self.individual_fitness))[0])
        self.probabilities = p

    def selection(self):
        return np.random.choice(a=self.individuals, size=2, replace=False, p=self.probabilities)

    def populate(self):
        new_generation = []
        for i in range(elitism):
            new_generation.append(self.individuals[i])
        while len(new_generation)-1 < popsize - elitism:
            parents = self.selection()
            child = parents[0].pair(parents[1])
            child.mutate()
            child.predict(train_set_output)
            new_generation.append(child)
        return Generation(new_generation)

#################################### MAIN ####################################


gen = []
for i in range(popsize):
    nn = NN(train_set_attributes)
    nn.generate_weights()
    nn.generate_bias()
    nn.predict(train_set_output)
    gen.append(nn)



first_generation = Generation(gen)
generation = first_generation.populate()
for i in range(1, iterations+1):
    new_gen = generation.populate()
    if i % 2000 == 0:
        print(f"[Train error @{i}]:", end=" ")
        print(new_gen.individuals[np.argmax(new_gen.individuals)].error[0])
    generation = new_gen

test_nn = generation.individuals[0]
test_nn.dataset = test_set_attributes
test_nn.predict(test_set_output)
print(f"[Test error]: {test_nn.error[0]}")

