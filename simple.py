import time
import sys
import traffic as tr

MAX_TIME = 5 * 60 - 5
start_time = time.time()

tf = tr.initialize()

uniform_solution = tf.generate_random_solution()
score = tf.evaluate(uniform_solution)
best_solution = tuple([uniform_solution, score])

elapsed_time = time.time() - start_time
while (elapsed_time < MAX_TIME):

    new_solution = tf.generate_random_solution()
    score = tf.evaluate(new_solution)
    if best_solution[1] < score:
        best_solution = tuple([new_solution, score])

    elapsed_time = time.time() - start_time

solution = best_solution[0]
tf.solution_print(solution)
