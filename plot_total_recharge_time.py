import matplotlib.pyplot as plt
from basic_functions import *
from scheduling_optimal import *
from scheduling_TSP import *
from scheduling_ToF import *
from scheduling_wait_time import *
from scheduling_shortest_tasks_first import *
from scheduling_longest_tasks_first import *
from scheduling_nodrone_wait_time import *
from scheduling_nodrone_ToF import *
from scheduling_nodrone_longest_tasks_first import *
from scheduling_nodrone_shortest_tasks_first import *

def plot_total_recharge_time(algos, input_style = 0, input_path_drone_based = "inputs/", input_path_sensor_based = "milp/backup_results_17feb_timelimit1200/output_simplified/", file_name = 'figures/recharge_time.eps', fig_title = "DB-LP + DB Algorithms", legend_style = 1):
    """Creates a figure with the total recharge time as the number of sensors increase. Saves it as file_name.

    Args:
        algo (list): List of dictionaries with the following keys:
            "algo": A scheduling function.
            "line": The line style.
            "label": The label.
        input_style (int, optional): 0 = Drone-based.1 = Sensor-based. Defaults to 0.
        input_path_drone_based (str, optional): Path to drone-based inputs. Defaults to "inputs/".
        input_path_sensor_based (str, optional): Path to sensor-based inputs. Defaults to "milp/backup_results_17feb_timelimit1200/output_simplified/".
        file_name (str, optional): The path + name of the figure file that will be created. Defaults to 'figures/recharge_time.eps'.
        fig_title (str, optional): The title of the figure. Defaults to "DB-LP + DB Algorithms".
        legend_style (int, optional): The style of the legend. Defaults to 0.
            0 = No legend.
            1 = Default plt legend.
            2 = Legend outside figure.
            3 = Export legend as eps file.
    """
    s = 5
    p = 5
    i_max = 50
    drone_speed = 0.5

    fig = plt.figure()
    ax = plt.subplot(111)
    fig.set_size_inches(6, 4)

    x_axis = range(3,11)
    ax.set_ylim([800, 2300])

    for algo in algos:
        time_avg = []
        for d in range(3,11):
            t = 0
            for s in [5,10,15,20,30,40,50]:
                for i in range(0,i_max):
                    if input_style == 0:
                        file = input_path_drone_based+"d"+str(d)+"_s"+str(s)+"_p"+str(p)+"/" + str(i) + ".txt"
                    else:
                        file = input_path_sensor_based+"s"+str(s)+"_p"+str(p)+"/" + str(i) + ".txt"
                    tasks = get_tasks(file)
                    done,time = algo["algo"](tasks,d,drone_speed)
                    t += time
        
            time_avg += [t/(i_max*7)]
        plt.plot(x_axis, time_avg, algo["line"],label = algo["label"])
    plt.title(fig_title, size = 15)
    plt.xlabel("# Drones",size = 15)
    plt.ylabel("Total Recharge Time (s)",size = 15)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    if legend_style == 1:
        ax.legend()
    elif legend_style == 2:
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(file_name, format='eps',bbox_inches = 'tight')
    if legend_style == 3:
        export_legend(fig, ax, file_name.replace(".eps","_legend.eps"))
    plt.close()


def plot_recharge_time_DBLP_plus_SBLP(algos_db,algos_sb,sensors = [5,10,15,20,30,40,50],input_path_drone_based = "inputs/",input_path_sensor_based = "milp/backup_results_17feb_timelimit1200/output_simplified/", fig_title = "DBLP and SBLP inputs", file_name = 'figures/RT_DBLP_plus_SBLP.eps', legend_style = 1):
    """Plots the total recharge time for drone-based and sensor-based algorithms for DBLP and SBLP inputs.

    Args:
        algos_db (list): List of drone-based algorithms.
        algos_sb (list): List of sensor-based algorithms.
        sensors (list, optional): List of numbers of sensors to be considered. Defaults to [5,10,15,20,30,40,50].
        input_path (str, optional): Path to DBLP output. Defaults to "inputs/".
        input_path (str, optional): Path to SBLP output. Defaults to "milp/backup_results_17feb_timelimit1200/output_simplified/".
        fig_title (str, optional): Title for output figure. Defaults to "DBLP and SBLP inputs".
        file_name (str, optional): File name for output figure. Defaults to 'figures/RT_DBLP_plus_SBLP.eps'.
        legend_style (int, optional): The style of the legend. Defaults to 0.
            0 = No legend.
            1 = Default plt legend.
            2 = Legend outside figure.
            3 = Export legend as eps file.

    Returns:
        list: List with the average recharge times for each scheduling algorithm.
    """
    s = 5
    p = 5
    i_max = 50
    drone_speed = 0.5

    fig = plt.figure()
    ax = plt.subplot(111)
    ax.set_ylim([800, 2300])
    fig.set_size_inches(6, 4)

    x_axis = range(3,11)

    algos_times = []
    for algo in algos_db:
        time_avg = []
        for d in range(3,11):
            t = 0
            for s in sensors:
                for i in range(0,i_max):
                    file = input_path_drone_based+"d"+str(d)+"_s"+str(s)+"_p"+str(p)+"/" + str(i) + ".txt"
                    tasks = get_tasks(file)
                    done,time = algo["algo"](tasks,d,drone_speed)
                    t += time
        
            time_avg += [t/(i_max*7)]
        plt.plot(x_axis, time_avg, algo["line"],label = algo["label"])
        algos_times += [time_avg]

    i_max = 100
    time_avg = []
    for algo in algos_sb:
        time_avg = []
        for d in range(3,11):
            t = 0
            for s in sensors:
                for i in range(0,i_max):
                    file = input_path_sensor_based+"s"+str(s)+"_p"+str(p)+"/" + str(i) + ".txt"
                    tasks = get_tasks(file)
                    done,time = algo["algo"](tasks,d,drone_speed)
                    t += time
        
            time_avg += [t/(i_max*7)]
        plt.plot(x_axis, time_avg, algo["line"],label = algo["label"])
        algos_times += [time_avg]

    plt.title(fig_title, size = 15)
    plt.xlabel("# Drones",size = 15)
    plt.ylabel("Total Recharge Time (s)",size = 15)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    if legend_style == 1:
        ax.legend()
    elif legend_style == 2:
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(file_name, format='eps',bbox_inches = 'tight')
    if legend_style == 3:
        export_legend(fig, ax, file_name.replace(".eps","_legend.eps"))
    plt.close()
    return algos_times

def plot_recharge_time_with_optimal(input_path = "inputs/",file_name = 'figures/RechargeTime_Optimal870Examples.eps'):
    """This is the most disgusting code I have ever written in my life. I'm sorry Alan.
    """
    s = 5
    p = 5
    i_max = 50
    print("comecou")
    drone_speed = 0.5

    results_wait_time = []
    results_longest = []
    results_shortest = []
    results_tof = []
    results_tsp = []
    results_nodrone_wait_time = []
    results_nodrone_tof = []
    results_nodrone_shortest = []
    results_nodrone_longest = []

    # algos = [scheduling_algo_5,scheduling_algo_3,scheduling_algo_4,scheduling_algo_6,scheduling_TSP,scheduling_algo_nodrone_wait_time,scheduling_algo_nodrone_tof,scheduling_algo_nodrone_shortest,scheduling_algo_nodrone_longest]
    labels = ["DOTA-ToF","DOTA-WT","DOTA-STF","DOTA-LTF","TSP","DATA-WT","DATA-ToF","DATA-STF","DATA-LTF"]
    for d in range(3,11):
        avg_per = 0
        k = 0
        max_diff = 0
        for s in [5,10,15,20,30,40,50]:
            for i in range(0,i_max):
                file = input_path + "d"+str(d)+"_s"+str(s)+"_p"+str(p)+"/" + str(i) + ".txt"
                tasks = get_tasks(file)
                if(len(tasks)<=9):
                    done2,wait_time = scheduling_DB_WT(tasks,d,drone_speed)
                    results_wait_time += [wait_time]
                    
                    tasks = get_tasks(file)
                    done2,tof = scheduling_DB_TOF(tasks,d,drone_speed)
                    results_tof += [tof]
                    
                    tasks = get_tasks(file)
                    done2,shortest = scheduling_DB_STF(tasks,d,drone_speed)
                    results_shortest += [shortest]
                    
                    tasks = get_tasks(file)
                    done2,longest = scheduling_DB_LTF(tasks,d,drone_speed)
                    results_longest += [longest]
                    
                    tasks = get_tasks(file)
                    done2,tsp = scheduling_TSP(tasks,d,drone_speed)
                    results_tsp += [tsp]
                    
                    tasks = get_tasks(file)
                    done2,nodrone_wt = scheduling_SB_WT(tasks,d,drone_speed)
                    results_nodrone_wait_time += [nodrone_wt]
                    
                    tasks = get_tasks(file)
                    done2,nodrone_tof = scheduling_SB_TOF(tasks,d,drone_speed)
                    results_nodrone_tof += [nodrone_tof]
                    
                    tasks = get_tasks(file)
                    done2,nodrone_shortest = scheduling_SB_STF(tasks,d,drone_speed)
                    results_nodrone_shortest += [nodrone_shortest]
                    
                    tasks = get_tasks(file)
                    done2,nodrone_longest = scheduling_SB_LTF(tasks,d,drone_speed)
                    results_nodrone_longest += [nodrone_longest]
    
    results_optimal = []
    file = open("optimal_output/backup_optimal_results_GLOBECOM.txt", 'r')
    data = file.readlines()
    for line in data:
          results_optimal += [float(line.split()[-1])]
    file.close()

    i_max = 50
    s = 15
    j = 0
    just_to_know = 0
    plot_optimal = []
    plot_tof = []
    plot_wait_time = []
    plot_longest= []
    plot_shortest= []
    plot_tsp = []
    plot_nodrone_wt = []
    plot_nodrone_tof = []
    plot_nodrone_shortest = []
    plot_nodrone_longest = []
    for d in range(3,11):
        avg_optimal = 0
        avg_wait_time = 0
        avg_tof = 0
        avg_shortest = 0
        avg_longest = 0
        avg_tsp = 0
        avg_nodrone_wt = 0
        avg_nodrone_tof = 0
        avg_nodrone_shortest = 0
        avg_nodrone_longest = 0
        k = 0
        for s in [5,10,15,20,30,40,50]:
            for i in range(0,i_max):
                file = "/Users/idiasdas/dev/GLOBECOM2022/inputs/d"+str(d)+"_s"+str(s)+"_p"+str(p)+"/" + str(i) + ".txt"
                tasks = get_tasks(file)
                if (len(tasks) <= 9):
                    if(s <=15):
                        avg_optimal += results_optimal[j]
                        avg_wait_time += results_wait_time[j]
                        avg_tof += results_tof[j]
                        avg_shortest += results_shortest[j]
                        avg_longest += results_longest[j]
                        avg_tsp += results_tsp[j]
                        avg_nodrone_wt += results_nodrone_wait_time[j]
                        avg_nodrone_tof += results_nodrone_tof[j]
                        avg_nodrone_shortest += results_nodrone_shortest[j]
                        avg_nodrone_longest += results_nodrone_longest[j]
                        k = k + 1
                        just_to_know = just_to_know + 1
                    j= j+1          
        plot_optimal += [avg_optimal/k]
        plot_tof += [avg_tof/k]
        plot_wait_time += [avg_wait_time/k]
        plot_longest += [avg_longest/k]
        plot_shortest += [avg_shortest/k]
        plot_tsp += [avg_tsp/k]
        plot_nodrone_wt += [avg_nodrone_wt/k]
        plot_nodrone_tof += [avg_nodrone_tof/k]
        plot_nodrone_shortest += [avg_nodrone_shortest/k]
        plot_nodrone_longest += [avg_nodrone_longest/k]
    
    lines = ["y-","g-","k-","b-","r-","m-"]
    fig = plt.figure()
    ax = plt.subplot(111)
    ax.set_ylim([600, 1200])
    fig.set_size_inches(6, 4)
    x_axis = range(3,11)

    plt.plot(x_axis, plot_tof, "y-",label = "DOTA-ToF")
    plt.plot(x_axis, plot_wait_time, "g-",label = "DOTA-WT")
    plt.plot(x_axis, plot_shortest, "k-",label = "DOTA-STF")
    plt.plot(x_axis, plot_longest, "b-",label = "DOTA-LTF")
    plt.plot(x_axis, plot_tsp, "r-",label = "TSP")
    plt.plot(x_axis, plot_optimal, "m-",label = "DOTA-Optimal")
    # plt.plot(x_axis, plot_nodrone_wt, "g-",label = "DATA-WT")
    # plt.plot(x_axis, plot_nodrone_tof, "y-",label = "DATA-ToF")
    # plt.plot(x_axis, plot_nodrone_shortest, "k-",label = "DATA-STF")
    # plt.plot(x_axis, plot_nodrone_longest, "b-",label = "DATA-LTF")
    
    # plt.legend()
    plt.xlabel("# Drones",size = 15)
    plt.ylabel("Total Recharge Time (s)",size = 15)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    # plt.tight_layout()
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(file_name, format='eps',bbox_inches = 'tight')
    # plt.show()

def plot_recharge_time_with_optimal_revised(algos,input_path = "inputs/",file_name = 'figures/RechargeTime_Optimal870Examples.eps',fig_title = "Recharge Time with Optimal (870)"):
    """Plots the total recharge time for each algorithm with DB-LP as input plus plots the GLOBECOM optimal solution.

    Args:
        algos (list): List of dictionaries with the algorithms to plot.
        
        input_path (str, optional): Path to the DB-LP output to use as input for the algorithms. Defaults to "inputs/".
        
        file_name (str, optional): Neme of the figure file that will be created. Defaults to 'figures/RechargeTime_Optimal870Examples.eps'.
        
        fig_title (str, optional): Title of the figure. Defaults to "Recharge Time with Optimal (870)".
    """    

    p = 5
    i_max = 50
    drone_speed = 0.5
    # Initialize figure
    fig = plt.figure()
    ax = plt.subplot(111)
    ax.set_ylim([600, 1200])
    fig.set_size_inches(6, 4)
    x_axis = range(3,11)
    # Plot recharge time for each algorithm
    for algo in algos:
        algo_avg = []
        for d in range(3,11):
            avg_per_drone = 0
            k = 0
            for s in [5,10,15]:
                for i in range(0,i_max):
                    file = input_path + "d"+str(d)+"_s"+str(s)+"_p"+str(p)+"/" + str(i) + ".txt"
                    tasks = get_tasks(file)
                    if(len(tasks) <= 9):
                        scheduling , recharge_time = algo["algo"](tasks,d,drone_speed)
                        avg_per_drone += recharge_time
                        k += 1
            algo_avg += [avg_per_drone/k]
        plt.plot(x_axis, algo_avg, algo["line"],label = algo["label"])
    # Plot optimal time using results of optimal experiment for GLOBECOM
    results_optimal = []
    file = open("optimal_output/backup_optimal_results_GLOBECOM.txt", 'r')
    data = file.readlines()
    for line in data:
          results_optimal += [float(line.split()[-1])]
    file.close()
    plot_optimal = []

    j = 0
    for d in range(3,11):
        avg_optimal_per_drone = 0
        k = 0
        for s in [5,10,15,20,30,40,50]:
            for i in range(0,i_max):
                file = "/Users/idiasdas/dev/GLOBECOM2022/inputs/d"+str(d)+"_s"+str(s)+"_p"+str(p)+"/" + str(i) + ".txt"
                tasks = get_tasks(file)
                if (len(tasks) <= 9):
                    if(s <= 15):
                        avg_optimal_per_drone += results_optimal[j]
                        k += 1
                    j = j + 1
        plot_optimal += [avg_optimal_per_drone/k]
    plt.plot(x_axis, plot_optimal, "m-",label = "DB-Optimal")
    # Figure details
    plt.title(fig_title, size = 15)
    plt.xlabel("# Drones",size = 15)
    plt.ylabel("Total Recharge Time (s)",size = 15)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(file_name, format='eps',bbox_inches = 'tight')

