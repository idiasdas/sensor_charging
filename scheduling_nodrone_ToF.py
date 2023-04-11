from basic_functions import *

def scheduling_algo_nodrone_tof(tasks,n_drones,drone_speed = 10.2):
    
    """Scheduling Algorithm Drone olbivious task assignment - Time of Flight(DOTA-ToF)

    Args:
        tasks (list): List of tasks to be scheduled.
        n_drones (int): Number of drones available.
        drone_speed (float, optional): Drone's speed. Defaults to 10.2 metets per second.

    Returns:
        list: List of tasks scheduled.
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
            tasks.sort(key = lambda x: x["ToF"],reverse=False)
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
# def scheduling_algo_nodrone_tof(tasks,n_drones,drone_speed = 10.2):
#     time = 0
#     n_tasks = len(tasks)
#     base_station = (0,0,0)
#     current_tasks = []
#     last_position = []
#     status_free = []
#     for drone in range(n_drones):
#         last_position += [base_station]
#         status_free += [True]
#     done = []
    
#     while n_tasks > 0:   
#         go = True
#         while(go):
#             for task in tasks:
#                 task["ToF"] = 10000000
#                 task["total_wait"] = 10000000
#                 total_wait = 10000000
#                 for drone in range(n_drones):
#                     if(status_free[drone]):
#                         tof = dist(last_position[drone],task["position"])/drone_speed
#                         if(get_wait_time_nodrone(task,drone, current_tasks,time) > task["ToF"]):
#                             total_wait = get_wait_time_nodrone(task,drone, current_tasks,time)
#                         else:
#                             total_wait = tof
#                         if(total_wait < task["total_wait"]):
#                             task["ToF"] = tof
#                             task["total_wait"] = total_wait
#                             task["drone"] = drone
#             tasks.sort(key = lambda x: x["ToF"],reverse=False)
#             task_added = False
#             for task in tasks:
#                 if(not check_conflicts_nodrone(task, current_tasks) and (status_free[task["drone"]])):
#                     task["ToF"] = 10000000
#                     task["total_wait"] = 10000000
#                     total_wait = 10000000
#                     for drone in range(n_drones):
#                         if(status_free[drone]):
#                             tof = dist(last_position[drone],task["position"])/drone_speed
#                             if(get_wait_time_nodrone(task,drone, current_tasks,time) > task["ToF"]):
#                                 total_wait = get_wait_time_nodrone(task,drone, current_tasks,time)
#                             else:
#                                 total_wait = tof
#                             if(total_wait < task["total_wait"]):
#                                 task["ToF"] = tof
#                                 task["total_wait"] = total_wait
#                                 task["drone"] = drone

#                     task["start"] = time + task["ToF"]
#                     task["end"] = task["start"] + task["time"]
#                     last_position[task["drone"]] = task["position"]
#                     current_tasks += [task]
#                     tasks.remove(task)
#                     task_added = True
#                     status_free[task["drone"]] = False
#                     break # whenever a task is added the tasks must be sorted again, keeps adding until none can be added
                    
#             if(not task_added):
#                 go = False
        
#         # Forward in time
#         time = min([x["end"] for x in current_tasks])
#         #Finish tasks
#         for task in list(current_tasks):
#             if(time >= task["end"]):
#                 done += [task]
#                 status_free[task["drone"]] = True
#                 current_tasks.remove(task)
#                 n_tasks = n_tasks - 1
#     return [done,time]