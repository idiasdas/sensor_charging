from basic_functions import *
import time
import threading

def scheduling_inorder(tasks,n_drones,drone_speed = 10.2):
    """Given a list of tasks in a given order, it schedules them respecting this order. This allows us to verify all possible schedulings.

    Args:
        tasks (list): The tasks to be scheduled
        n_drones (int): Amount of drones available
        drone_speed (float, optional): The drones' speed. Defaults to 10.2 meters per second.

    Returns:
        [list,float]: A list with the tasks scheduled and the total time to charge the sensors in this schedule.
    """
    current_time = 0
    n_tasks = len(tasks)
    base_station = (0,0,0)
    current_tasks = []
    last_position = []
    status_free = []
    for drone in range(n_drones):
        last_position += [base_station]
        status_free += [True]
    done = []
    
    while n_tasks > 0:
        go = True
        while(go):
            # order tasks by wait time
            for task in tasks:
                task["ToF"] = dist(last_position[task["drone"]],task["position"])/drone_speed
                if(get_wait_time(task, current_tasks,current_time) > task["ToF"]):
                    task["total_wait"] = max(get_wait_time(task, current_tasks,current_time),task["ToF"])
                else:
                    task["total_wait"] = task["ToF"]
            task_added = False
            for task in list(tasks):
                if(status_free[task["drone"]]):
                    task["start"] = current_time + task["total_wait"]
                    task["end"] = task["start"] + task["time"]
                    last_position[task["drone"]] = task["position"]
                    current_tasks += [task]
                    tasks.remove(task)
                    task_added = True
                    status_free[task["drone"]] = False
                    break
                else:
                    go = False
                    break
                
            if(not task_added):
                go = False
        
        # Forward in time
        time = min([x["end"] for x in current_tasks])
        #Finish tasks
        for task in list(current_tasks):
            if(time >= task["end"]):
                done += [task]
                status_free[task["drone"]] = True
                current_tasks.remove(task)
                n_tasks = n_tasks - 1
    return [done,time]

# -------------------------------------------------------------------------------------------------------------------------------------------------
def optimal(tasks,n_drones,drone_speed = 10.2, timeout = 0):
    """Verifies all possible schedulings by scheduling in order all permutations of a list of tasks. And returns the best scheduling.

    Args:
        tasks (list): List of tasks
        n_drones (int): Number of drones available
        drone_speed (float, optional): Drones' speed. Defaults to 10.2 meters per second.
        timeout (float, optional): Limit in seconds before the code stops. When timeout = 0 the code runs until the end. Defaults to 0.

    Returns:
        [list, float]: The scheduling and the total time required to charge the sensors with the smallest time among all schedulings.
    """
    start_time = time.process_time()
    best_done = []
    best_time = 100000
    best_sequence = []
    for order in itertools.permutations(range(len(tasks))):
        if(timeout > 0 and time.process_time() - start_time > timeout):
            # print("Timeout")
            return [[],0]
        sequence = []
        for i in range(len(tasks)):
            sequence += [tasks[order[i]]]
        done,charging_time = scheduling_inorder(list(sequence),n_drones,drone_speed)
        if(charging_time < best_time):
            best_done = list(done)
            best_time = charging_time
            best_sequence = list(sequence)
    done,charging_time = scheduling_inorder(list(best_sequence),n_drones,drone_speed)
    return [best_done,best_time]


# -------------------------------------------------------------------------------------------------------------------------------------------------
def run_optimal_thread(d,s,i,tasks, drone_speed,my_lock,file_name,timeout = 0):
    """Runs the optimal scheduling for a set of parameters and saves the resulsts into a shared file.

    Args:
        d (int): Number of drones
        s (int): Number of sensors
        i (int): Instance number
        tasks (list): List of tasks to be scheduled
        drone_speed (float): Drone's speed
        my_lock (threading.Lock): Lock shared among the threads to access the shared file
        file_name (string): Shared file where the resulsts will be written.
        timeout (int, optional): Amount of seconds this thread will run before timing out. Defaults to 0. If 0, then there is no limit.
    """
    start_time = time.process_time()
    done,recharge_time = optimal(tasks,d,drone_speed,timeout)
    exec_time = time.process_time() - start_time

    my_lock.acquire()
    output_file = open(file_name,"a")
    output_file.write( str(i) + "\t" + str(recharge_time) + "\t" + str(exec_time) + "\n")
    # output_file.write(str(p) + "\t" + str(d) + "\t" + str(s) + "\t" + str(i) + "\t" + str(recharge_time) + "\t" + str(exec_time) + "\n")
    # print(str(p) + "\t" + str(d) + "\t" + str(s) + "\t" + str(i) + "\t" + str(recharge_time) + "\t" + str(exec_time) + "\n")
    output_file.close()
    my_lock.release()

# -------------------------------------------------------------------------------------------------------------------------------------------------
def optimal_experiment(p = 5, drones  = range(3,11), sensors = [5,10,15,20,30,40,50], instances = range(0,50), drone_speed = 0.5, output_path = "optimal_output/", timeout = 300):
    """ Runs the optimal scheduling for a set of parameters and saves the resulsts into a shared file with all the instances.

    Args:
        p (int, optional): Squared number of positions. Defaults to 5.
        drones (list, optional): List with all the numbers of available drones to be considered. Defaults to range(3,11).
        sensors (list, optional): List with all the numbers of sensors to be considered. Defaults to [5,10,15,20,30,40,50].
        instances (list, optional): Numbers of the instances to be considered. Defaults to range(0,50).
        drone_speed (float, optional): Drones speed. Defaults to 0.5.
        output_path (string, optional): Path where the output files will be saved. Defaults to "optimal_output/".
        timeout (int, optional): Amount of seconds this thread will run before timing out. Defaults to 300. If 0, then there is no limit.
    """    
    inputs_path = "/Users/idiasdas/dev/sensor_charging/inputs/"
    my_lock = threading.Lock()
    
    for d in drones:
        for s in sensors:
            threads = []
            file_name = output_dir + "optimal_output_p" + str(p) +"_d"+ str(d) + "_s" + str(s) + ".txt"
            output_file = open(file_name,"a")
            output_file.write("i\trecharge_time\texec_time\n")
            output_file.close()
            for i in instances:
                file = inputs_path + "d"+str(d)+"_s"+str(s)+"_p"+str(p)+"/" + str(i) + ".txt"
                tasks = get_tasks(file)
                
                t = threading.Thread(target = run_optimal_thread, args = [d,s,i,tasks, drone_speed,my_lock,file_name,timeout])
                threads.append(t)
                t.start()

            for t in threads:
                t.join()
# -------------------------------------------------------------------------------------------------------------------------------------------------
def read_optimal_results(drones = range(3,11), sensors = [5,10,15,20,30,40,50] ,files_path = "/Users/idiasdas/dev/sensor_charging/optimal_output/2_hour/"):
    """Reads the files at files_path and returns a list of dictionaries with all the results

    Returns:
        list: A list with the optimal results for each parameter described as python dictionaries.
    """
    p = 5
    i_max = 50
    drone_speed = 0.5
    optimal_results = []    
    for d in drones:
        for s in sensors:
            file_name = files_path + "optimal_output_p" + str(p) +"_d"+ str(d) + "_s" + str(s) + ".txt"
            file = open(file_name, 'r')
            data = file.readlines()
            for line in data[1:]: # jumps the first line
                results = line.split()
                dict_results = {}
                dict_results["drones"] = d
                dict_results["sensors"] = s
                dict_results["i"] = int(results[0])
                dict_results["recharge_time"] = float(results[1])
                dict_results["exec_time"] = float(results[2])
                if(dict_results["recharge_time"]>0):
                    optimal_results += [dict_results]
            file.close()
    return optimal_results
# -------------------------------------------------------------------------------------------------------------------------------------------------
def read_old_optimal_results(file_name = "/Users/idiasdas/dev/sensor_charging/optimal_output/backup_optimal_results_GLOBECOM.txt"):
    """Reads the file with the optimal results used for GLOBECOM 2022

    Returns:
        list: A list with the optimal results for each parameter described as python dictionaries.
    """
    optimal_results = []
    file = open(file_name, 'r')
    for line in file.readlines(): # jumps the first line
        results = line.split()
        dict_results = {}
        dict_results["drones"] = int(results[0])
        dict_results["sensors"] = int(results[1])
        dict_results["i"] =  int(results[2])
        dict_results["recharge_time"] =  float(results[3])
        optimal_results += [dict_results]
    file.close()
    return optimal_results