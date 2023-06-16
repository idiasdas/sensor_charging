from basic_functions import *


def scheduling_algo_nodrone_wt_revised(tasks,n_drones,drone_speed = 10.2):
    base_station = (0,0,0)
    current_tasks = []

    drone_position = []
    drone_time = []
    for drone in range(n_drones):
        drone_position += [base_station]
        drone_time += [0]
    done = []

    while len(tasks) > 0:
        for task in tasks:
            task["ToF"] = 10000000
            task["wait_time"] = 10000000
            wait_time = 10000000
            for drone in range(n_drones):
                tof = dist(drone_position[drone],task["position"])/drone_speed
                wait_time = max(get_longest_conflict_time(task, current_tasks,0, drone = drone),tof + drone_time[drone])
                if(wait_time < task["wait_time"]):
                    task["ToF"] = tof
                    task["wait_time"] = wait_time
                    task["drone"] = drone
        
        tasks.sort(key = lambda x: x["wait_time"],reverse=False)
        task = tasks[0]

        task["start"] = task["wait_time"]
        task["end"] = task["start"] + task["time"]
        drone_position[task["drone"]] = task["position"]
        drone_time[task["drone"]] = task["end"]

        for old_task in list(current_tasks):
            if(old_task["drone"] == task["drone"]):
                current_tasks.remove(old_task)
                done += [old_task]

        tasks.remove(task)
        current_tasks += [task]
    
    for task in list(current_tasks):
        current_tasks.remove(task)
        done += [task]

    finish_time = max([x["end"] for x in done])
    return [done,finish_time]   

def scheduling_algo_nodrone_wait_time_optimized(tasks,n_drones,drone_speed = 10.2):
    """Scheduling Algorithm Drone olbivious task assignment (DOTA-WT)

    Args:
        tasks (list): List of tasks to be scheduled.
        n_drones (int): Number of drones available.
        drone_speed (float, optional): Drone's speed. Defaults to 10.2 metets per second.

    Returns:
        list: List of tasks scheduled.
    """
    n_tasks = len(tasks)
    current_time = 0
    base_station = (0,0,0)
    current_tasks = []
    last_position = []
    status_free = []
    for drone in range(n_drones):
        last_position += [base_station]
        status_free += [True]
    done = []

    while n_tasks > 0:
        assign_tasks = len(tasks) > 0
        while(assign_tasks):
            # Ordering the tasks by the wait_time
            for task in tasks:
                task["ToF"] = 10000000
                task["wait_time"] = 10000000
                wait_time = 10000000
                for drone in range(n_drones):
                    tof = dist(last_position[drone],task["position"])/drone_speed
                    if(not status_free[drone]): # Time of flight correction for tasks whose drone is busy
                        tof += [(x["end"] - current_time) for x in current_tasks if x["drone"] == drone][0]
                    wait_time = max(get_longest_conflict_time(task, current_tasks,current_time, drone = drone),tof)
                    if(wait_time < task["wait_time"]):
                        task["ToF"] = tof
                        task["wait_time"] = wait_time
                        task["drone"] = drone
            
            tasks.sort(key = lambda x: x["wait_time"],reverse=False)
            task = tasks[0]
            
            assign_tasks = False
            if(status_free[task["drone"]]):
                status_free[task["drone"]] = False
                task["start"] = current_time + task["wait_time"]
                task["end"] = task["start"] + task["time"]
                last_position[task["drone"]] = task["position"]
                current_tasks += [task]
                tasks.remove(task)
                assign_tasks = len(tasks) > 0

        # Forward time
        current_time = min([x["end"] for x in current_tasks])
        #Finish tasks
        for task in list(current_tasks):
            if(current_time >= task["end"]):
                done += [task]
                status_free[task["drone"]] = True
                current_tasks.remove(task)
                n_tasks = n_tasks - 1
    return [done,current_time]      

def scheduling_algo_nodrone_wait_time(tasks,n_drones,drone_speed = 10.2):
    """Scheduling Algorithm Drone olbivious task assignment (DOTA-WT)

    Args:
        tasks (list): List of tasks to be scheduled.
        n_drones (int): Number of drones available.
        drone_speed (float, optional): Drone's speed. Defaults to 10.2 metets per second.

    Returns:
        list: List of tasks scheduled.
    """
    n_tasks = len(tasks)
    time = 0
    base_station = (0,0,0)
    current_tasks = []
    last_position = []
    status_free = []
    for drone in range(n_drones):
        last_position += [base_station]
        status_free += [True]
    done = []

    while n_tasks > 0:
        while(True in status_free and len(tasks) > 0):
            # Ordering the tasks by the wait_time
            for task in tasks:
                task["ToF"] = 10000000
                task["wait_time"] = 10000000
                wait_time = 10000000
                for drone in range(n_drones):
                    if(status_free[drone]):
                        tof = dist(last_position[drone],task["position"])/drone_speed
                        wait_time = max(get_wait_time_nodrone(task,drone, current_tasks,time),tof)
                        if(wait_time < task["wait_time"]):
                            task["ToF"] = tof
                            task["wait_time"] = wait_time
                            task["drone"] = drone
            tasks.sort(key = lambda x: x["wait_time"],reverse=False)
            task = tasks[0]
            status_free[task["drone"]] = False
            task["start"] = time + task["wait_time"]
            task["end"] = task["start"] + task["time"]
            last_position[task["drone"]] = task["position"]
            current_tasks += [task]
            tasks.remove(task)
        # Forward time
        time = min([x["end"] for x in current_tasks])
        #Finish tasks
        for task in list(current_tasks):
            if(time >= task["end"]):
                done += [task]
                status_free[task["drone"]] = True
                current_tasks.remove(task)
                n_tasks = n_tasks - 1
    return [done,time]            


def scheduling_algo_nodrone_wait_time_all(tasks,n_drones,drone_speed = 10.2):
    """Scheduling Algorithm Drone olbivious task assignment (DOTA-WT-ALL) Considers all drones for the wait time, including the ones that are busy with tasks.
        In this, if a drone is busy but wilds the best wait time, we foward in time before assigning the task to it.

    Args:
        tasks (list): List of tasks to be scheduled.
        n_drones (int): Number of drones available.
        drone_speed (float, optional): Drone's speed. Defaults to 10.2 metets per second.

    Returns:
        list: List of tasks scheduled.
    """
    n_tasks = len(tasks)
    time = 0
    base_station = (0,0,0)
    current_tasks = []
    last_position = []
    status_free = []
    for drone in range(n_drones):
        last_position += [base_station]
        status_free += [True]
    done = []
    while n_tasks > 0:
        while(True in status_free and len(tasks) > 0):
            # Ordering the tasks by the wait_time
            for task in tasks:
                task["ToF"] = 10000000
                task["wait_time"] = 10000000
                wait_time = 10000000
                for drone in range(n_drones):                    
                    tof = dist(last_position[drone],task["position"])/drone_speed
                    if(status_free[drone]):
                        wait_time = max(get_wait_time_nodrone(task,drone, current_tasks,time),tof)
                    else:
                        wait_time = max(get_end_time_drone(drone, current_tasks),get_wait_time_nodrone(task,drone, current_tasks,time)) + tof
                    if(wait_time < task["wait_time"]):
                        task["ToF"] = tof
                        task["wait_time"] = wait_time
                        task["drone"] = drone
            tasks.sort(key = lambda x: x["wait_time"],reverse=False)
            task = tasks[0]
            if(status_free[task["drone"]] == False):
                break
            else:
                status_free[task["drone"]] = False
                task["start"] = time + task["wait_time"]
                task["end"] = task["start"] + task["time"]
                last_position[task["drone"]] = task["position"]
                current_tasks += [task]
                tasks.remove(task)
        # Forward time
        time = min([x["end"] for x in current_tasks])
        #Finish tasks
        for task in list(current_tasks):
            if(time >= task["end"]):
                done += [task]
                status_free[task["drone"]] = True
                current_tasks.remove(task)
                n_tasks = n_tasks - 1
    return [done,time]            


