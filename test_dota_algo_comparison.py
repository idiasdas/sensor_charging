from basic_functions import *
from plot_schedule import *
from plot_total_recharge_time import *
from scheduling_wait_time import *
from scheduling_longest_tasks_first import *
from scheduling_ToF import *

def dota_algo_set_comparison(algo1, algo2, input_path = "/Users/idiasdas/dev/sensor_charging/inputs/"):
    """Compare two algorithms for scheduling tasks given a set of inputs. Considers inputs from old MILP with drones already assigned to tasks.

    Returns:
        boolean: True if the two algorithms give the same results, False otherwise.
    """

    p = 5
    i_max = 50
    drone_speed = 0.5    
    sensors = [5,10,15,20,30,40,50]

    for s in range(len(sensors)):
        for d in range(3,11):
            for i in range(0,i_max):
                file = input_path + "d"+str(d)+"_s"+str(sensors[s])+"_p"+str(p)+"/" + str(i) + ".txt"
                
                tasks = get_tasks(file)
                scheduling1,time1 = algo1(tasks, d, drone_speed)

                tasks = get_tasks(file)
                scheduling2,time2 = algo2(tasks, d, drone_speed)

                if time1 != time2:
                    print("\t- Different time for d = " + str(d) + ", s = " + str(sensors[s]) + ", i = " + str(i))
                    plot_schedule(scheduling1, d, time1, file_name = "tests_outputs/test_equivalence_" + algo1.__name__ +".eps",save=True)
                    plot_schedule(scheduling2, d, time2, file_name = "tests_outputs/test_equivalence_" + algo2.__name__ +".eps",save=True)

                    print(" Saved different example as tests_outputs/test_equivalence_" + algo1.__name__ +".eps and tests_outputs/test_equivalence_" + algo2.__name__ +".eps")
                    print("Stopped equivalence test.")
                    return False


    return True 

def test_equivalence(algos, file_name):
    """Tests equivalence between two algorithms. If they are not equivalent, plots the difference between them and gives two examples of different solutions.

    Args:
        algos (list): List with two algorithms to be compared. They must be described as dictionaries such as {"algo":scheduling_algo_wait_time, "label":"scheduling_wait_time","line":"b-"}.
        file_name (string): Name of plot file to be saved in case of not equivalent algorithms.
    """    
    print("Testing scheduling_wait_time and scheduling_wait_time_optimized")
    if dota_algo_set_comparison(algos[0]["algo"], algos[1]["algo"]):
        print("(SUCCESS)")
    else:
        print("Plotting difference between algorithms over all inputs")
        plot_total_recharge_time(algos, file_name="tests_outputs/"+file_name+".eps")
        print("(FAIL)")
    print("---------------------------------------------------------------")


# algo1 = {"algo":scheduling_algo_wait_time, "label":"scheduling_wait_time","line":"b-"}
# algo2 = {"algo":scheduling_algo_wait_time_optimized, "label":"scheduling_wait_time_optimized","line":"r-"}
# test_equivalence([algo1, algo2], "test_equivalence_wait_time")

# algo1 = {"algo":scheduling_algo_longest_tasks_first, "label":"scheduling_longest_tasks_first","line":"b-"}
# algo2 = {"algo":scheduling_algo_longest_tasks_first_optimized,"label":"scheduling_longest_tasks_first_optimized","line":"r-"}
# test_equivalence([algo1, algo2], "test_equivalence_longest_tasks_first")

# algo1 = {"algo":scheduling_algo_tof, "label":"scheduling_ToF","line":"b-"}
# algo2 = {"algo":scheduling_algo_tof_optimized, "label":"scheduling_ToF_optimized","line":"r-"}
# test_equivalence([algo1, algo2], "test_equivalence_ToF")
