from basic_functions import *
import itertools
# checks all possible sequences of tasks for each drone, returns the maximum time of the sequences with minimum time
def scheduling_TSP(tasks, n_drones, drone_speed = 10.2):
    total_time = []
    best_sequences = []
    for drone in range(n_drones):
        tasks_d = [ task for task in tasks if task["drone"] == drone]
        min_time = 10000000
        best_sequence = ()
        for sequence in itertools.permutations(tasks_d):
            time = get_total_time(sequence,drone_speed)
            if time < min_time:
                min_time = time
                best_sequence = sequence
        total_time += [min_time]
        best_sequences += [best_sequence]
    return [best_sequences, max(total_time)]