import time
import traffic as tr
import math
import random
import copy

def get_random_neighbor(old_solution):
    solution = copy.deepcopy(old_solution)
    change_amount = random.randint(1, len(solution)//3 )
    for _ in range(change_amount):
        iidx = random.randint(0,len(solution)-1) # intersection index
        if len(solution[iidx]) > 1:
            sidx = random.randint(0,len(solution[iidx]) -1)
            street = solution[iidx][sidx]
            if random.random() > 0.5:
                random.shuffle(solution[iidx])
            elif random.random() > 0.3:
                solution[iidx][sidx] = (street[0], street[1] + random.randint(1, 3) )
            else:
                solution[iidx][sidx] = (street[0], max(1, street[1] - 1) )
            
    return solution

MAX_TIME = 60 * 5 - 5
start_time = time.time()

tf = tr.initialize()

uniform_solution = tf.generate_uniform_solution()
score = tf.evaluate(uniform_solution)
best_solution = tuple([uniform_solution, score])
current_solution = copy.deepcopy(best_solution)

count = 0
T = 10000
elapsed_time = time.time() - start_time
while (elapsed_time < MAX_TIME):
    T = max(T * 0.99, 10)
    random_neighbor = get_random_neighbor(current_solution[0])
    e1 = current_solution[1]
    e2 = tf.evaluate(random_neighbor)
    if e2>e1 : 
        current_solution = (random_neighbor,e2)
        e1=e2
    else:
        p = math.exp(-(e1-e2)/T)
        if  p >= random.random():
            current_solution = (random_neighbor, e2)
            e1 = e2
    if e1 > best_solution[1]:
        best_solution = current_solution
        count = 0
    if count > 5:
        current_solution = best_solution
        count = 0
    count += 1

    elapsed_time = time.time() - start_time


solution = best_solution[0]
tf.solution_print(solution)