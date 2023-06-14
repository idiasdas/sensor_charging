from basic_functions import *
from scheduling_optimal import *
from plot_schedule import *


def check_new_optimal(p = 5, drones = [3,4], sensors=[5,10],input_path = "inputs/",files_path = "tests_outputs/optimal/"):
    """Reads the resulsts form the new optimal sheduling algorithm and compares them with the old optimal results.
        If any differences are found it prints the tasks, and plots the schedule for the new optimal and the old optimal.

    Args:
        p (int, optional): Number of positions. Defaults to 5.
        drones (list, optional): List with all the amounts of drones to be considered. Defaults to [3,4].
        sensors (list, optional): List with all the amounts of sensors to be considered. Defaults to [5,10].
        input_path (str, optional): Path to tasks. Defaults to "inputs/".
        files_path (str, optional): Path to save output files. Defaults to "tests_outputs/optimal/".

    Returns:
        bool: Return True if no differences are found, False otherwise.
    """    
    amount_of_errors = 0
    results = read_optimal_results(drones, sensors, files_path )
    old_results = read_old_optimal_results()
    for result in results:
        for old_result in old_results:
            if result["drones"] == old_result["drones"] and result["sensors"] == old_result["sensors"] and result["i"] == old_result["i"] and result["recharge_time"] != old_result["recharge_time"]:
                amount_of_errors += 1
                print("mistake found:" + str(amount_of_errors))
                print(result["drones"])
                print(result["sensors"])
                print(result["i"])
                print("---------------------------------------------------------------------------------")
                file = input_path + "d"+str(result["drones"])+"_s"+str(result["sensors"])+"_p"+str(p)+"/" + str(result["i"]) + ".txt"
                tasks = get_tasks(file)
                for task in tasks:
                    print(task)
                print("---------------------------------------------------------------------------------")
                done,c_time = optimal(tasks, result["drones"], drone_speed=0.5)
                for task in done:
                    print(task)
                print("---------------------------------------------------------------------------------")
                print("New optimal:" + str(result["recharge_time"]))
                print("Old optimal:" + str(old_result["recharge_time"]))
                print("Check new:" + str(c_time))
                print("---------------------------------------------------------------------------------")
                plot_schedule(done,result["drones"],old_result["recharge_time"],file_name="tests_outputs/optimal_mistake_"+ str(amount_of_errors) + ".eps",save=True)
                if(not verify_schedule(done)):
                    print("ERROR IN SCHEDULE")
                    return False
                print("---------------------------------------------------------------------------------")

    if amount_of_errors == 0:
        print("(SUCCESS)")
        return True
    else:
        print("Error found: " + str(amount_of_errors) + " out of " + str(len(results)) + " tests")
        print("(FAIL)")
        return False

def visualize_instance(d = 3,s = 5,i = 1, input_path = "inputs/"):
    """Runs the new optimal algorithm for a given instance and plots the schedule.

    Args:
        d (int, optional): Number os drones. Defaults to 3.
        s (int, optional): Number os sensors. Defaults to 5.
        i (int, optional): Iteration number. Defaults to 1.
        input_path (str, optional): Path to tasks. Defaults to "inputs/".
    """    
    
    file = input_path + "d"+str(d)+"_s"+str(s)+"_p"+str(5)+"/" + str(i) + ".txt"               
    tasks = get_tasks(file)

    done,c_time = optimal(tasks, d, drone_speed=0.5)

    print("New optimal:" + str(c_time))
    for task in done:
        print(task)

    plot_schedule(done,d,1000,file_name="tests_outputs/look_at_this_shit_optimal.eps",save=True)
    

# visualize_instance()
# Create files
# optimal_experiment(drones = range(3,11), sensors=[5,10,15,20,30,40,50], output_path="optimal_output/new_optimal/task_limit_15/", tasks_limit=15, timeout=3600)
optimal_experiment(drones = [3,4], sensors=[5,10], output_path="tests_outputs/optimal/", tasks_limit=15, timeout=100)
# Check them against old results
check_new_optimal(drones = [3,4], sensors=[5,10])

