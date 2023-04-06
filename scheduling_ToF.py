from basic_functions import *
def scheduling_algo_tof(tasks,n_drones, drone_speed = 10.2):
    time = 0
    n_tasks = len(tasks)
    base_station = (0,0,0)
    current_tasks = []
    last_position = []
    status_free  = []
    for drone in range(n_drones):
        last_position += [base_station]
        status_free += [True]
    done = []
    
    while n_tasks > 0:
        # order tasks by ToF
        for task in tasks:
            task["ToF"] = dist(task["position"],last_position[task["drone"]])/drone_speed
        tasks.sort(key=lambda x: x["ToF"])
        
        #Try to assign all tasks
        for task in list(tasks):
            if(not check_conflicts(task, current_tasks)):
                task["ToF"] = dist(task["position"],last_position[task["drone"]])/drone_speed
                task["start"] = time + task["ToF"]
                task["end"] = task["start"] + task["time"]
                last_position[task["drone"]] = task["position"]
                current_tasks += [task]
                status_free[task["drone"]] = False
                tasks.remove(task)
                
        for task in list(tasks):
            if(status_free[task["drone"]] and len( [x for x in current_tasks if x["drone"] == task["drone"]]) == 0):
                if(get_wait_time(task, current_tasks,time) > task["ToF"]):
                    task["total_wait"] = max(get_wait_time(task, current_tasks,time),task["ToF"])
                else:
                    task["total_wait"] = task["ToF"]
                task["start"] = time + task["total_wait"]
                task["end"] = task["start"] + task["time"]
                last_position[task["drone"]] = task["position"]
                current_tasks += [task]
                tasks.remove(task)
                status_free[task["drone"]] = False
        # Forward in time          
        shortest_time = min([x["end"] for x in current_tasks])
        time = shortest_time
        
        # Finish tasks
        for task in list(current_tasks):
            if(time >= task["end"]):
                done += [task]
                current_tasks.remove(task)
                status_free[task["drone"]] = True
                n_tasks = n_tasks - 1

    
    return [done,time]