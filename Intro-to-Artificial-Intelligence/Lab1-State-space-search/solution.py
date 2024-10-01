from collections import deque
from heapq import *
import sys

# Sources used:
# https://www.geeksforgeeks.org/deque-in-python/
# https://www.geeksforgeeks.org/unpacking-a-tuple-in-python/
# https://realpython.com/sort-python-dictionary/
# https://builtin.com/data-science/priority-queues-in-python

#################################### LOADING ####################################

arguments = sys.argv

algorithm = ""
wantOptimistic = False
wantConsistent = False

for i in range(0, len(arguments)):
    if arguments[i] == "--alg":
        algorithm = arguments[i+1]
    if arguments[i] == "--ss":
        filepath = arguments[i+1]
    if arguments[i] == "--h":
        heuristic_filepath = arguments[i+1]
    if arguments[i] == "--check-optimistic":
        wantOptimistic = True
    if arguments[i] == "--check-consistent":
        wantConsistent = True

states = {}
heuristic = {}

with open(filepath, "r", encoding="utf-8") as file:
    initial_state = file.readline().rstrip("\n")
    if initial_state.startswith("#"):
        initial_state = file.readline().rstrip("\n")
    goal_state = file.readline().rstrip("\n").split(" ")
    list = []
    for line in file:
        list.append(line.rstrip("\n"))


for el in list:
    var = el.split(":")
    var = [el.strip() for el in var]
    node = var[0]
    next_states_list = var[1].split(" ")
    next_states = {}
    for state in next_states_list:
        state = state.split(",")
        if len(state) == 2:
            next_states.update({state[0] : state[1]})
    states.update({node : next_states})


if algorithm == "astar" or wantOptimistic or wantConsistent:
    with open(heuristic_filepath, "r", encoding="utf-8") as file:
        list = []
        for line in file:
            list.append(line.rstrip("\n"))

        
    for el in list:
        var = el.split(":")
        var = [el.strip() for el in var]
        heuristic.update({var[0] : float(var[1])})


#################################### BFS ####################################

def breadthFirstSearch(initial_state, states, goal_state):

    open = deque()  # deque containing tuples with 3 elements: (state, cost, parent)
    open.append((initial_state, 0, None))
    visited = set()

    while len(open) != 0:
        n = open.popleft()
        visited.add(n[0])
        if n[0] in goal_state:
            return n, len(visited)
    
        next_states = states.get(n[0])
        next_states = dict(sorted(next_states.items()))     
        for state, cost in next_states.items():
            if state not in visited:
                open.append((state, float(cost), n))

    return False, len(visited)

def pathBFS(n):
    path = []
    total_cost = 0.0
    while n != None:
        state, cost, n = n     
        path.append(state)
        total_cost += cost
    return path[::-1], total_cost


def printPath(path):
    res = ""
    for p in range(0, len(path)):
        if p != len(path)-1:
            res += path[p] + " => "
        else:
            res += path[p]
    return res 

def printBFS(solutionFound, visited, path, total_cost):
    print("# BFS")
    print("[FOUND_SOLUTION]: " + solutionFound)
    print("[STATES_VISITED]: " + str(visited))
    print("[PATH_LENGTH]: " + str(len(path)))
    print("[TOTAL_COST]: " + str(float(total_cost))) 
    print("[PATH]: " + printPath(path))


#################################### UCS ####################################

def uniformCostSearch(initial_state, states, goal_state):
    open = []   # priority queue containing tuples with 3 elements: (total_path_cost, state, parent) 
    heappush(open, (0, initial_state, None))
    visited = set()

    while len(open) != 0:
        n = heappop(open)
        visited.add(n[1])
        if n[1] in goal_state:
            total_cost = n[0]
            return n, len(visited), total_cost
        
        next_states = states.get(n[1])
        for state, cost in next_states.items():
            if state not in visited:
                heappush(open, (float(cost) + n[0], state, n))
    
    return False, len(visited), None 

def pathUCS(n):
    path = []
    while n != None:
        cost, state, n = n     
        path.append(state)
    return path[::-1]


def printUCS(solutionFound, visited, path, total_cost):
    print("# UCS")
    print("[FOUND_SOLUTION]: " + solutionFound)
    print("[STATES_VISITED]: " + str(visited))
    print("[PATH_LENGTH]: " + str(len(path)))
    print("[TOTAL_COST]: " + str(float(total_cost))) 
    print("[PATH]: " + printPath(path))

#################################### ASTAR ####################################

def aStarSearch(initial_state, states, goal_state, heuristic):
    open = []   # priority queue containing tuples with 4 elements: (total_path_cost + heuristic(state), state, total_path_cost, parent) 
    heappush(open, (heuristic.get(initial_state), initial_state, 0, None)) 
    visited = set()
    visited_count = 0

    while len(open) != 0:
        n = heappop(open)
        visited.add(n)
        visited_count += 1
        if n[1] in goal_state:
            total_cost = n[2]
            return n, visited_count, total_cost
        
        next_states = states.get(n[1])
        for state, cost in next_states.items():
            found = ""
            temp = 0
            allowPush = True
            for s in visited:
                if s[1] == state:
                    temp = s[0]
                    found = "visited"
                    break
            if found == "":
                for s in open:
                    if s[1] == state:
                        temp = s[2]
                        found = "open"
                        break
            if found != "":
                if temp < float(cost) + n[2] + heuristic.get(state):
                    allowPush = False
                else:
                    if found == "visited":
                        for s in visited:
                            if s[1] == state:
                                visited.remove(s)
                                found = ""
                                break
                    if found == "open":
                        for s in open:
                            if s[1] == state:
                                open.remove(s)    
                                heapify(open)
                                break
                    allowPush = True
            if allowPush:
                heappush(open, (float(cost) + n[2] + heuristic.get(state), state, float(cost) + n[2], n))
        
    return False, visited_count, total_cost

def pathAStar(n):
    path = []
    while n != None:
        total_cost, state, cost, n = n     
        path.append(state)
    return path[::-1]  

def printAStar(filepath, solutionFound, visited, path, total_cost):
    file = filepath.split("\\")[-1]
    print("# A-STAR " + file)
    print("[FOUND_SOLUTION]: " + solutionFound)
    print("[STATES_VISITED]: " + str(visited))
    print("[PATH_LENGTH]: " + str(len(path)))
    print("[TOTAL_COST]: " + str(float(total_cost))) 
    print("[PATH]: " + printPath(path))

#################################### CHECK OPTIMISTIC ####################################

def checkOptimistic(goal_state, states, heuristic):
    heurSorted = dict(sorted(heuristic.items()))
    result = {}
    for state, heur in heurSorted.items():
        if state in goal_state:
            result.update({state : 0.0})
        else:
            solution, visited, total_cost = uniformCostSearch(state, states, goal_state) 
            result.update({state : total_cost})
    return result

def printCheckOptimistic(filepath, result, heuristic):
    
    file = filepath.split("\\")[-1]
    print("# HEURISTIC-OPTIMISTIC " + file)   
    
    errCount = 0
    for state, cost in result.items():
        if heuristic.get(state) <= cost:
            print("[CONDITION]: [OK] h(" + state + ") <= h*: " + str(heuristic.get(state)) + " <= " + str(cost))
        else:
            print("[CONDITION]: [ERR] h(" + state + ") <= h*: " + str(heuristic.get(state)) + " <= " + str(cost))
            errCount += 1
    if errCount == 0:
        print("[CONCLUSION]: Heuristic is optimistic.")
    else:
        print("[CONCLUSION]: Heuristic is not optimistic.")


#################################### CHECK CONSISTENCY ####################################

def checkConsistent(states, heuristic):
    
    heurSorted = dict(sorted(heuristic.items()))
    errCount = 0
    for state, heur in heurSorted.items():
        next_states = states.get(state)
        sortedStates = dict(sorted(next_states.items()))
        for nextState, cost in sortedStates.items():
            if heuristic.get(state) <= heuristic.get(nextState) + float(cost):
                print("[CONDITION]: [OK] h(" + state + ") <= h(" + nextState + ") + c: " + str(heuristic.get(state)) + " <= " + str(heuristic.get(nextState)) + " + " + str(float(cost)))
            else:
                print("[CONDITION]: [ERR] h(" + state + ") <= h(" + nextState + ") + c: " + str(heuristic.get(state)) + " <= " + str(heuristic.get(nextState)) + " + " + str(float(cost)))
                errCount += 1

    if errCount == 0:
        print("[CONCLUSION]: Heuristic is consistent.")
    else:
        print("[CONCLUSION]: Heuristic is not consistent.")


#################################### MAIN ####################################

def main():
    
    if algorithm == "bfs":

        solution, visited = breadthFirstSearch(initial_state, states, goal_state)
        if solution != False:
            path, total_cost = pathBFS(solution)
            printBFS("yes", visited, path, total_cost)
    
    if algorithm == "ucs":
        
        solution, visited, total_cost = uniformCostSearch(initial_state, states, goal_state) 
        if solution != False:
            path = pathUCS(solution)
            printUCS("yes", visited, path, total_cost)
    
    if algorithm == "astar":
        
        solution, visited, total_cost = aStarSearch(initial_state, states, goal_state, heuristic)

        if solution != False:
            path = pathAStar(solution)
            printAStar(heuristic_filepath, "yes", visited, path, total_cost) 


    if wantOptimistic:
        result = checkOptimistic(goal_state, states, heuristic)
        printCheckOptimistic(heuristic_filepath, result, heuristic)

    if wantConsistent:
        file = heuristic_filepath.split("\\")[-1]
        print("# HEURISTIC-CONSISTENT " + file)
        checkConsistent(states, heuristic)

    return 0


main()