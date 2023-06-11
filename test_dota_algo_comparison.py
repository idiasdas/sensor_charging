from basic_functions import *
from scheduling_wait_time import *
from plot_schedule import *

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
                    plot_schedule(scheduling1, d, time1, file_name = "tests_outputs/scheduling1.eps",save=True)
                    plot_schedule(scheduling2, d, time2, file_name = "tests_outputs/scheduling2.eps",save=True)
                    return False


    return True 


print("Testing scheduling_wait_time and scheduling_wait_time_optimized")
if dota_algo_set_comparison(scheduling_algo_wait_time, scheduling_algo_wait_time_optimized):
    print("SUCCESS")
else:
    print("FAIL")
