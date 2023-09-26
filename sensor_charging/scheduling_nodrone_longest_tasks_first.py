from basic_functions import *

def scheduling_SB_LTF_revised(tasks,n_drones,drone_speed = 10.2):
    """Sensor-based Longest Tasks First(SB-LTF). Revised version.

    Args:
        tasks (list): List of tasks to be scheduled. Any preassigned drones are ignored.
        n_drones (int): Number of available drones.
        drone_speed (float, optional): Drone's flight speed. Defaults to 10.2.

    Returns:
        [list,float]: [List of tasks assigned, finish time]
    """
    base_station = (0,0,0)
    assigned_tasks = []

    assign_order = 0
    drone_position = []
    drone_time = []
    for drone in range(n_drones):
        drone_position += [base_station]
        drone_time += [0]
    # done = []

    tasks.sort(key = lambda x: x["time"],reverse=True)

    while len(tasks) > 0:
        # Get the task with the longest time
        task = tasks[0]
        task["assign_order"] = assign_order
        assign_order += 1
        # ------------------------------------------------------------------ 
        # Determine flight time and wait time, assign drone with minimum wait time
        task["ToF"] = 10000000
        task["wait_time"] = 10000000
        wait_time = 10000000
        for drone in range(n_drones):
            tof = dist(drone_position[drone],task["position"])/drone_speed
            wait_time = max(get_longest_conflict_time(task, assigned_tasks,0, drone = drone),tof + drone_time[drone])
            if(wait_time < task["wait_time"]):
                task["ToF"] = tof
                task["wait_time"] = wait_time
                task["drone"] = drone
        # ------------------------------------------------------------------
        # Task assignment
        task["start"] = task["wait_time"]
        task["end"] = task["start"] + task["time"]
        drone_position[task["drone"]] = task["position"]
        drone_time[task["drone"]] = task["end"]
        # ------------------------------------------------------------------
        # Update tasks list and current tasks list
        tasks.remove(task)
        assigned_tasks += [task]
        # ------------------------------------------------------------------
    finish_time = max([x["end"] for x in assigned_tasks])
    return [assigned_tasks,finish_time]  

def scheduling_SB_LTF(tasks,n_drones,drone_speed = 10.2):
    """Sensor-based Longest Tasks First(SB-LTF)

    Args:
        tasks (list): List of tasks to be scheduled.
        n_drones (int): Number of drones available.
        drone_speed (float, optional): Drone's speed. Defaults to 10.2 metets per second.

    Returns:
        [list,float]: [List of scheduled tasks, finish time]
    """
    # Initializing variables
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
    # ------------------------------------
    while n_tasks > 0:
        while(True in status_free and len(tasks) > 0): # While there is at least one drone free and at least one task to be assigned
            # Order the tasks by the Time of Flight
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
            tasks.sort(key = lambda x: x["time"],reverse=True)
            # Assign task with lowest time of flight
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