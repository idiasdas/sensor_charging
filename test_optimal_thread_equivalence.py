from basic_functions import *
from scheduling_optimal import *


# def test_optimal_thread_equivalence(input_path = "/Users/idiasdas/dev/sensor_charging/inputs/"):
#     p = 5
#     results_optimal = read_old_optimal_results()

#     for result in results_optimal:
#         file = input_path+"d"+str(result["n_drones"])+"_s"+str(result["sensors"])+"_p"+str(p)+"/" + str(result["i"]) + ".txt"
#         tasks = get_tasks(file)

#         my_lock = threading.Lock()
#         run_optimal_thread(result["drones"],result["sensors"],result["i"],tasks, result["drone_speed"],my_lock,"",3600)

