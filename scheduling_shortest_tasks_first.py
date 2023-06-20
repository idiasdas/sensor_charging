from basic_functions import *
def scheduling_DB_STF(tasks,n_drones,drone_speed = 10.2):
    """Drone-based Shortest Tasks First.
    Schedule tasks in a greedy way, shortest tasks first

    Args:
        tasks (list): List of tasks to be scheduled
        n_drones (int): Number of drones available
        drone_speed (float, optional): Drone's speed. Defaults to 10.2.

    Returns:
        list: List of scheduled tasks, with start and finish times.
    """
    time = 0
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
            # order tasks by duration
            for task in tasks:
                task["ToF"] = dist(last_position[task["drone"]],task["position"])/drone_speed
                if(get_longest_conflict_time(task, current_tasks,time) > task["ToF"]):
                    task["total_wait"] = max(get_longest_conflict_time(task, current_tasks,time),task["ToF"])
                else:
                    task["total_wait"] = task["ToF"]
            tasks.sort(key = lambda x: x["time"])
            task_added = False
            for task in list(tasks):
                if(not check_conflicts(task, current_tasks) and status_free[task["drone"]]):
                    task["start"] = time + task["ToF"]
                    task["end"] = task["start"] + task["time"]
                    last_position[task["drone"]] = task["position"]
                    current_tasks += [task]
                    tasks.remove(task)
                    task_added = True
                    status_free[task["drone"]] = False
                    break
                else:
                    if(status_free[task["drone"]] and len( [x for x in current_tasks if x["drone"] == task["drone"]]) == 0):
                        task["start"] = time + task["total_wait"]
                        task["end"] = task["start"] + task["time"]
                        last_position[task["drone"]] = task["position"]
                        current_tasks += [task]
                        tasks.remove(task)
                        task_added = True
                        status_free[task["drone"]] = False
                        break
                    status_free[task["drone"]] = False
                    
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

def scheduling_DB_STF_optimized(tasks, n_drones, drone_speed = 10.2):
    """Drone-based Shortest Tasks First. Optimimzed version.

    Args:
        tasks (list): List of tasks to be scheduled
        n_drones (int): Number of drones available
        drone_speed (float, optional): Drone's speed. Defaults to 10.2.
        skip_conflicts (bool, optional): If True, tasks that have conflicts are skipped during assignment until they are conflicy free. Defaults to False.

    Returns:
        list: List of scheduled tasks, with start and finish times.
    """
    time = 0
    n_tasks = len(tasks)
    base_station = (0,0,0)
    current_tasks = []
    last_position = []
    status_free = []
    for drone in range(n_drones):
        last_position += [base_station]
        status_free += [True]
    done = []
    tasks.sort(key = lambda x: x["time"],reverse=False)
    
    while n_tasks > 0:
        assign_tasks = len(tasks) > 0
        while(assign_tasks):
            # order tasks by duration from shortest to longest
            for task in tasks:
                task["ToF"] = dist(last_position[task["drone"]],task["position"])/drone_speed
                if(not status_free[task["drone"]]): # Wait time correction for tasks whose drone is busy
                    task["ToF"] += [(x["end"] - time) for x in current_tasks if x["drone"] == task["drone"]][0]
                task["total_wait"] = max(get_longest_conflict_time(task, current_tasks,time),task["ToF"])
                
            # assign tasks
            assign_tasks = False
            for task in list(tasks):
                if(status_free[task["drone"]]):
                    task["start"] = time + task["total_wait"]
                    task["end"] = task["start"] + task["time"]
                    last_position[task["drone"]] = task["position"]
                    current_tasks += [task]
                    tasks.remove(task)
                    status_free[task["drone"]] = False
                    assign_tasks = len(tasks) > 0 # Stop if there are no more tasks to assign
                    break # Stop after assigning one task to recompute wait_time
        
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