from basic_functions import *
def scheduling_DB_TOF(tasks,n_drones, drone_speed = 10.2):
    """Drone-based scheduling Time of Flight.
        The tasks must have drones already assigned to them. 

    Args:
        tasks (list): list of tasks to be scheduled
        n_drones (int): number of drones available
        drone_speed (float, optional): Drone's speed. Defaults to 10.2.

    Returns:
        list: List of schediled tasks, with start and finish times
    """
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
        
        # Try to assign all tasks without conflicts
        for task in list(tasks):
            if(not check_conflicts(task, current_tasks)):
                task["ToF"] = dist(task["position"],last_position[task["drone"]])/drone_speed
                task["start"] = time + task["ToF"]
                task["end"] = task["start"] + task["time"]
                last_position[task["drone"]] = task["position"]
                current_tasks += [task]
                status_free[task["drone"]] = False
                tasks.remove(task)

        # Assign tasks with conflicts
        for task in list(tasks):
            if(status_free[task["drone"]] and len( [x for x in current_tasks if x["drone"] == task["drone"]]) == 0):
                if(get_longest_conflict_time(task, current_tasks,time) > task["ToF"]):
                    task["total_wait"] = max(get_longest_conflict_time(task, current_tasks,time),task["ToF"])
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


def scheduling_DB_TOF_optimized(tasks,n_drones, drone_speed = 10.2):
    """Drone-based scheduling Time of Flight. Optimized version.
        The tasks must have drones already assigned to them.

    Args:
        tasks (list): list of tasks to be scheduled
        n_drones (int): number of drones available
        drone_speed (float, optional): Drone's speed. Defaults to 10.2.
        skip_conflicts (bool, optional): If False, the algorithm will try to schedule tasks despite conflicts using the wait time to avoid them. If True the algorithm will only assign conflict free tasks. Defaults to True which showed better results in our tests.

    Returns:
        list: List of schediled tasks, with start and finish times
    """
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
            if(not status_free[task["drone"]]): # Wait time correction for tasks whose drone is busy
                    task["ToF"] += [(x["end"] - time) for x in current_tasks if x["drone"] == task["drone"]][0]
            task["total_wait"] = max(get_longest_conflict_time(task, current_tasks,time),task["ToF"])
            
        tasks.sort(key=lambda x: x["ToF"])
                
        for task in list(tasks):
            if(status_free[task["drone"]] and not check_conflicts(task, current_tasks)):
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