import matplotlib.pyplot as plt
from basic_functions import *

def plot_solution_time(input_path = "/Users/idiasdas/dev/GLOBECOM2022/inputs/", file_name  = "figures/solution_time.eps"):
    """Plots the solution time for different number of sensors and drones

    Args:
        input_path (str, optional): Path to MILP outputs. Defaults to "/Users/idiasdas/dev/GLOBECOM2022/inputs/".
        file_name (str, optional): File name for output figure. Defaults to "figures/solution_time.eps".
    """
    p = 5
    i_max = 50
    drone_speed = 0.5

    sensors = [5,10,15,20,30,40,50]
    colors = ["b--","g--","y--","r--","c--","k--","m--"]
    x_line = range(3,11)

    fig = plt.figure()
    ax = plt.subplot(111)
    fig.set_size_inches(6, 4)

    for s in range(len(sensors)):
        avg_h_per_d = []
        for d in range(3,11):
            total_h = 0
            for i in range(0,i_max):
                file = input_path + "d"+str(d)+"_s"+str(sensors[s])+"_p"+str(p)+"/" + str(i) + ".txt"
                total_h += get_sol_time(file)
            avg_h_per_d += [total_h/i_max]
        plt.plot(x_line, avg_h_per_d, colors[s], label = str(sensors[s]) + " sensors")

    plt.legend()
    plt.xlabel("# Drones",size = 15)
    plt.ylabel("Resolution time (s)",size = 15)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.yscale("log")
    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(file_name, format='eps',bbox_inches = 'tight')


def plot_solution_times_per_drones(sensors = [5,10,15,20,30,40,50],input_path = "inputs/",file_name = 'figures/MILP_Simplified_vs_OLD_MILP.eps'):
    """  Plots the solution times for the simplified MILP and the old MILP for different number of drones.

    Args:
        sensors (list, optional): List with numbers of sensors to plot. Defaults to [5,10,15,20,30,40,50].
        input_path (str, optional): Path to old MILP inputs. Defaults to "inputs/".
        file_name (str, optional): Name of the created figure file. Defaults to 'figures/MILP_Simplified_vs_OLD_MILP.eps'.
    """
    s = 5
    p = 5
    i_max = 50
    drone_speed = 0.5

    fig = plt.figure()
    ax = plt.subplot(111)
    fig.set_size_inches(6, 4)

    x_axis = range(3,11)
    time_avg = []
    for d in range(3,11):
        t = 0
        for s in sensors:
            for i in range(0,i_max):
                file = input_path+"d"+str(d)+"_s"+str(s)+"_p"+str(p)+"/" + str(i) + ".txt"
                sol_time = get_sol_time(file)
                t += sol_time
    
        time_avg += [t/(i_max*7)]
    plt.plot(x_axis, time_avg, "g-",label = "MILP")

    input_path = "milp/backup_results_17feb_timelimit1200/output_simplified/"
    i_max = 100
    time_avg = []
    for d in range(3,11):
        t = 0
        for s in sensors:
            for i in range(0,i_max):
                file = input_path+"s"+str(s)+"_p"+str(p)+"/" + str(i) + ".txt"
                sol_time = get_sol_time(file)
                t += sol_time
    
        time_avg += [t/(i_max*7)]
    plt.plot(x_axis, time_avg, "b-",label = "SMILP")
    plt.title("sensors = " + str(sensors))
    plt.xlabel("# Drones",size = 15)
    plt.ylabel("Total Solution Time (s)",size = 15)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(file_name, format='eps',bbox_inches = 'tight')
    plt.close()



def plot_solution_times_per_sensors(sensors = [5,10,15,20,30,40,50],input_path = "inputs/",file_name = 'figures/MILP_Simplified_vs_OLD_MILP.eps'):
    """Plots the solution times for the simplified MILP and the old MILP for different number of sensors.
        Solves the models for 3 to 10 drones.
        Considers 50 instances for each number of sensors.


    Args:
        sensors (list, optional): List of sensors to plot. Defaults to [5,10,15,20,30,40,50].
        input_path (str, optional): path to MILP output . Defaults to "inputs/".
        file_name (str, optional): Output figure file name. Defaults to 'figures/MILP_Simplified_vs_OLD_MILP.eps'.
    """
    s = 5
    p = 5
    i_max = 50
    drone_speed = 0.5

    fig = plt.figure()
    ax = plt.subplot(111)
    fig.set_size_inches(6, 4)

    x_axis = sensors
    time_avg = []
    
    
    for s in sensors:
        t = 0
        for d in range(3,11):
            for i in range(0,i_max):
                file = input_path+"d"+str(d)+"_s"+str(s)+"_p"+str(p)+"/" + str(i) + ".txt"
                sol_time = get_sol_time(file)
                t += sol_time
    
        time_avg += [t/(i_max*8)]
    plt.plot(x_axis, time_avg, "g-",label = "MILP")

    input_path = "milp/backup_results_17feb_timelimit1200/output_simplified/"
    i_max = 100
    time_avg = []
    for s in sensors:
        t = 0
        for d in range(3,11):
            for i in range(0,i_max):
                file = input_path+"s"+str(s)+"_p"+str(p)+"/" + str(i) + ".txt"
                sol_time = get_sol_time(file)
                t += sol_time
    
        time_avg += [t/(i_max*8)]
    plt.plot(x_axis, time_avg, "b-",label = "SMILP")
    # plt.title("sensors = " + str(sensors))
    plt.xlabel("# Sensors",size = 15)
    plt.ylabel("Solution Time (s)",size = 15)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(file_name, format='eps',bbox_inches = 'tight')
    plt.close()