import numpy as np
import ast
import itertools
# -------------------------------------------------------------------------------------------------------------------------------------------------
def get_tasks(file_path):
    """ Reads the output file from the MILP and returns a list of dictionaries describing the tasks 

    Args:
        file_path (str): The path to the output file of the MILP

    Returns:
        list: List of dictionaries describing the tasks
    """
    tasks = []
    file = open(file_path, 'r')
    data = file.readlines()
    id = 0
    for line in data[3:]:  # jumping the first 3 lines
        dic = ast.literal_eval(line)
        if not "id" in dic.keys():
            dic["id"] = id
        id += 1
        tasks += [dic]
    return tasks
# -------------------------------------------------------------------------------------------------------------------------------------------------
def get_lp_results(file_path, old_version = True):
    """ Reads the output file from the MILP and returns the values of lambda 1 ana lambda 2

    Args:
        file_path (str): The path to the output file of the MILP

    Returns:
        list: [lambda 1, lambda 2]
    """
    tasks = []
    file = open(file_path, 'r')
    data = file.readlines()

    line = data[1]

    if(old_version):
        lambda_1 = float(line.split("lambda1 =")[-1].split(",")[0])
    else:
        lambda_1 = float(line.split("lambda1 =")[-1].split(")")[0])
    lambda_2 = float(line.split("lambda2 =")[-1].split(")")[0])
    return [lambda_1, lambda_2]
# ----------------------------------------------------------------------------------------------------------------------------------------------
def get_sol_time(file_path):
    """Returns the solution time stated in the output files from the MILP

    Args:
        file_path (str): The path to the output file of the MILP

    Returns:
        float: Solution time in seconds
    """
    file = open(file_path, 'r')
    data = file.readlines()
    return (float(data[1].split("=")[-1].split("ms")[0]))/1000 # First line of the file contains the time in ms
# -------------------------------------------------------------------------------------------------------------------------------------------------
def dist(p,q):
    """Returns distance between two points

    Args:
        p (tuple): Coordinates of position p
        q (tuple): Coordinates of position q

    Returns:
        float: Distance between p and q
    """
    return np.sqrt(pow(p[0] - q[0],2) + pow(p[1] - q[1],2) + pow(p[2] - q[2],2))
# -------------------------------------------------------------------------------------------------------------------------------------------------
def check_conflicts(task,current_tasks, drone = None):
    """Returns true if there is a conflict between the task and any of the current tasks. Returns false otherwise

    Args:
        task (dict): Task description
        current_tasks (list): List of tasks
        drone (int,optional): If the task has no drone assigned to it, specify the drone to check conflicts with. Defaults to None, in which case task["drone"] is used.

    Returns:
        bool: True if the task has a conflict with some task on the list current_tasks
    """
    if(drone == None):
        drone = task["drone"]
    for c_task in current_tasks:
        if(c_task["drone"] == drone):
            return True
        if(c_task["position"] == task["position"]):
            return True
        common_sensors = [sensor for sensor in task["sensors"] if sensor in c_task["sensors"]]
        if(len(common_sensors)>0):
            return True
    return False
# -------------------------------------------------------------------------------------------------------------------------------------------------
def check_conflicts_nodrone(task,current_tasks):
    """Returns true if there is a conflict between the task and any of the current tasks. Returns false otherwise
       THIS FUNCTION SHOULD BE DELETED.
    Args:
        task (dict): Task description
        current_tasks (list): List of tasks
        drone (int): Drone to execute the task

    Returns:
        bool: True if the task has a conflict with some task on the list current_tasks
    """
    for c_task in current_tasks:
        if(c_task["position"] == task["position"]):
            return True
        common_sensors = [sensor for sensor in task["sensors"] if sensor in c_task["sensors"]]
        if(len(common_sensors)>0):
            return True
    return False
# -------------------------------------------------------------------------------------------------------------------------------------------------
def get_conflict_degree(tasks):
    """Returns the amount of conflicts between the tasks with different drones.

    Args:
        tasks (list): List of tasks

    Returns:
        int: Amount of conflicts
    """
    k = 0
    for x,y in itertools.combinations(tasks, r=2): # a conflict between tasks a and b is only counted once
        if(x["drone"] != y["drone"] and check_conflicts(x, [y])):
            k = k + 1
    return k
# -------------------------------------------------------------------------------------------------------------------------------------------------
def get_drone_per_sensor(tasks,n_sensors,n_drones):
    """Returns how many drones charge each sensor on average.

    Args:
        tasks (list): List of tasks
        n_sensors (int): Total number of sensors
        n_drones (int): Total number of drones

    Returns:
        float: Average amounte of drones per sensor
    """
    sensors = []
    for s in range(n_sensors):
        sensors += [0]
        drones = []
        for  d in range(n_drones):
            drones += [0]
        for task in tasks:
            if (s in task["sensors"] and drones[task["drone"]] == 0):
                drones[task["drone"]] = 1
        sensors[s] = sum(drones)
    return sum(sensors)/len(sensors)
# -------------------------------------------------------------------------------------------------------------------------------------------------
def get_total_time(tasks,drone_speed):
    """gives the total time a drone needs to complete a given sequence of tasks (duration + ToF)

    Args:
        tasks (list): List of tasks
        drone_speed (float): Drone's speed

    Returns:
        float: Total time
    """
    time = 0
    last_pos = (0,0,0)
    for task in tasks:
        time += dist(task["position"],last_pos)/drone_speed + task["time"]
        last_pos = task["position"]
    return time
# -------------------------------------------------------------------------------------------------------------------------------------------------
def get_longest_conflict_time(task, current_tasks, time, no_self = False, drone = None):
    """Returns how long a drone needs to wait until it is conflict free

    Args:
        task (dict): Task's description
        current_tasks (list): List of tasks
        time (float): Current time
        no_self (bool, optional): True if we should ignore the tasks with the same drone as task["drone"]. Defaults to False.
        drone (int, optional): Drone to execute the task. Defaults to None, in which case task["drone"] is used.
    Returns:
        float: Wait time
    """
    if(not check_conflicts(task,current_tasks, drone = drone)):
        return 0
    if(no_self):
        conflicts  = [ x["end"] for x in current_tasks if check_conflicts(task, [x], drone = drone) and task["drone"] != x["drone"]]
    else:
        conflicts  = [ x["end"] for x in current_tasks if check_conflicts(task, [x], drone = drone)]
    wait_time = max(conflicts) - time
    if(wait_time < 0):
        print(" Error wait time")
        exit(1)
    return wait_time
# -------------------------------------------------------------------------------------------------------------------------------------------------
def get_wait_time_nodrone(task,drone, current_tasks, time, no_self = False):
    """Returns how long a drone needs to wait until it is conflict free (Modified for the no drone algorithms)

    Args:
        task (dict): Task's description
        drone (int): Drone's ID
        current_tasks (list): List of tasks
        time (float): Current time
        no_self (bool, optional): True if we should ignore the tasks with the same drone as task["drone"]. Defaults to False.

    Returns:
        float: Wait time
    """
    if(not check_conflicts_nodrone(task,current_tasks)):
        return 0
    if(no_self):
        conflicts  = [ x["end"] for x in current_tasks if check_conflicts_nodrone(x, [task]) and drone != x["drone"]]
    else:
        conflicts  = [ x["end"] for x in current_tasks if check_conflicts_nodrone(x, [task])]
    wait_time = max(conflicts) - time
    if(wait_time < 0):
        print(" Error wait time")
        exit(1)
    return wait_time
# -------------------------------------------------------------------------------------------------------------------------------------------------
def get_end_time_drone(drone, current_tasks):
    """Returns the end time of the tasks the drone is currently responsible for.

    Args:
        drone (int): The drone's id.
        current_tasks (list): List of tasks being currently executed.

    Returns:
        float: The end time of the task the drone is responsible for.
    """
    end_time = 0
    for c_task in current_tasks:
        if(c_task["drone"] == drone and c_task["end"] > end_time):
            end_time = c_task["end"]
    return end_time
            
# -------------------------------------------------------------------------------------------------------------------------------------------------
def get_all_times(n_drones, tasks):
    """Returns the stats of a set of scheduled tasks

    Args:
        n_drones (int): Total number of drones
        tasks (list): List of tasks already scheduled 

    Returns:
        list: Average total time, Average time of flight, Average Idle time
    """
    tasks_per_d = []
    total_time = []
    recharge_time = []
    tof = []
    diff = []
    k = 0
    for drone in range(n_drones):
        tasks_per_d = [x for x in tasks if x["drone"] == drone]
        if(len(tasks_per_d)>0):
            recharge_time = sum([x["time"] for x in tasks_per_d])
            total_time += [max([x["end"] for x in tasks_per_d])]
            tof += [sum([x["ToF"] for x in tasks_per_d])]
            wait_time = max([x["end"] for x in tasks_per_d]) - sum([x["ToF"] for x in tasks_per_d]) - recharge_time
            if(wait_time > 1):
                diff += [wait_time]
                k = k + 1
    avg_total_time = sum(total_time)/len(total_time)
    avg_tof = sum(tof)/len(tof)
    if(len(diff)>0):
        avg_wait_time = sum(diff)/len(diff)
    else:
        avg_wait_time = 0
    return [avg_total_time,avg_tof, avg_wait_time]
# -------------------------------------------------------------------------------------------------------------------------------------------------
def verify_schedule(tasks):
    """Verifies if a scheduling is conflict free. No tasks in conflict can be executed simultaeneously. Returns True if no conflicts happen on the given scheduling.

    Args:
        tasks (list): List of scheduled tasks with their corresponding start and finish times.

    Returns:
        bool: True if the schedule is conflict free. False otherwise.
    """
    eps = 0.0001 # small number to avoind rounding errors
    for task1 in tasks:
        for task2 in tasks:
            if task1["id"] != task2["id"]:
                if check_conflicts(task1,[task2]):
                    if(task1["start"] >= task2["start"] + eps and task1["start"] < task2["end"] - eps): #Task 1 starts during the execution of task 2
                        print("ERROR: improper scheduling between tasks " + str(task1["id"])+ " and " + str(task2["id"]))
                        return False
                    if(task1["drone"] == task2["drone"]):
                        if(task1["start"] - task1["ToF"] >= task2["start"] + eps and task1["start"] - task1["ToF"] < task2["end"] - eps): #Both tasks are executed by the same drone and the drone flies to execute task 1 during the execution of task 2
                            print("ERROR: improper scheduling between tasks " + str(task1["id"])+ " and " + str(task2["id"]))
                            return False
    return True

def print_schedule(tasks):
    """Prints the tasks in a schedule in the order they start.

    Args:
        tasks (list): List of tasks that have already been scheduled.
    """    
    tasks.sort(key = lambda x: x["start"],reverse=False)
    print("\t\t- id","\t","start","\t\t","end","\t\t","drone","\t\t","flight_start", "\t\t","sensors",sep=' ')
    for task in tasks:
        print("\t\t- "+ str(task["id"]) +"\t " + "{:.4f}".format(task["start"]) +"\t " + "{:.4f}".format(task["end"]) +"\t " + str(task["drone"]) +"\t\t " + "{:.4f}".format(task["start"] - task["ToF"]),"\t\t",task["sensors"], sep=' ')