from basic_functions import *
from scheduling_optimal import *
from plot_schedule import *


def chekc_new_optimal():
    input_path = "/Users/idiasdas/dev/sensor_charging/inputs/"
    results = read_optimal_results(drones = [3,4], sensors=[5,10],files_path = "/Users/idiasdas/dev/sensor_charging/optimal_output/")
    old_results = read_old_optimal_results()
    for result in results:
        for old_result in old_results:
            if result["drones"] == old_result["drones"] and result["sensors"] == old_result["sensors"] and result["i"] == old_result["i"] and result["recharge_time"] != old_result["recharge_time"]:
                print("mistake found")
                print(result["drones"])
                print(result["sensors"])
                print(result["i"])
                print("-------------")
                file = input_path + "d"+str(result["drones"])+"_s"+str(result["sensors"])+"_p"+str(5)+"/" + str(result["i"]) + ".txt"
                    
                tasks = get_tasks(file)
                done,c_time = optimal(tasks, result["drones"], drone_speed=0.5)
                for task in done:
                    print(task)
                print("New optimal:" + str(result["recharge_time"]))
                print("Old optimal:" + str(old_result["recharge_time"]))
                print("Check new:" + str(c_time))
                plot_schedule(done,result["drones"],old_result["recharge_time"],file_name="tests_outputs/shiiiit_optimal.eps",save=True)
                
                exit(1)

# Create files
optimal_experiment(drones = [3], sensors=[5], output_path="tests_outputs/optimal/")
# Check them against old results
# chekc_new_optimal()
