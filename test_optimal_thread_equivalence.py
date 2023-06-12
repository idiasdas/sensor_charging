from basic_functions import *
from scheduling_optimal import *
from plot_schedule import *


def chekc_new_optimal(drones = [3,4], sensors=[5,10],input_path = "/Users/idiasdas/dev/sensor_charging/inputs/",files_path = "/Users/idiasdas/dev/sensor_charging/tests_outputs/optimal/"):

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
                file = input_path + "d"+str(result["drones"])+"_s"+str(result["sensors"])+"_p"+str(5)+"/" + str(result["i"]) + ".txt"
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

def visualize_instace(d = 3,s = 5,i = 1, input_path = "/Users/idiasdas/dev/sensor_charging/inputs/"):
    
    file = input_path + "d"+str(d)+"_s"+str(s)+"_p"+str(5)+"/" + str(i) + ".txt"
                        
    tasks = get_tasks(file)
    done,c_time = optimal(tasks, d, drone_speed=0.5)

    print("New optimal:" + str(c_time))
    for task in done:
        print(task)

    plot_schedule(done,d,1000,file_name="tests_outputs/look_at_this_shit_optimal.eps",save=True)
    

# visualize_instace()
# Create files
optimal_experiment(drones = range(3,11), sensors=[5,10,15,20,30,40,50], output_path="optimal_output/new_optimal/", tasks_limit=15)
# Check them against old results
# chekc_new_optimal(drones = [3,4], sensors=[5,10])
