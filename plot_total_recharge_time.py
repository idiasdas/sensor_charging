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

def plot_total_recharge_time(algos, fig_title, input_path = "/Users/idiasdas/dev/sensor_charging/inputs/",file_name = '/Users/idiasdas/dev/sensor_charging/figures/NODRONE_50i_recharge_time_5x5_sensors_all.eps'):
    """Creates a figure with the total recharge time as the number of sensors increase. Saves it as file_name.

    Args:
        input_path (str, optional): The path to the inputs used to run the schedulings algorithms. Defaults to "/Users/idiasdas/dev/sensor_charging/inputs/".
        file_name (str, optional): The path + name of the figure file that will be created. Defaults to '/Users/idiasdas/dev/sensor_charging/figures/NODRONE_50i_recharge_time_5x5_sensors_all.eps'.
    """
    s = 5
    p = 5
    i_max = 50
    drone_speed = 0.5

    fig = plt.figure()
    ax = plt.subplot(111)
    fig.set_size_inches(6, 4)

    x_axis = range(3,11)
    ax.set_ylim([800, 2500])
    
    for algo in algos:
        time_avg = []
        for d in range(3,11):
            t = 0
            for s in [5,10,15,20,30,40,50]:
                for i in range(0,i_max):
                    file = input_path+"d"+str(d)+"_s"+str(s)+"_p"+str(p)+"/" + str(i) + ".txt"
                    tasks = get_tasks(file)
                    done,time = algo["algo"](tasks,d,drone_speed)
                    if(algo["algo"] != scheduling_TSP):
                        if(not verify_schedule(done)):
                            print("Improper Scheduling.")
                            print("\t- " + str(algo["algo"]))
                            print("\t- D: " + str(d) + " S: " + str(s) + " i: " + str(i))
                            exit(1)
                    t += time
        
            time_avg += [t/(i_max*7)]
        plt.plot(x_axis, time_avg, algo["line"],label = algo["label"])
    plt.title(fig_title)
    plt.xlabel("# Drones",size = 15)
    plt.ylabel("Total Recharge Time (s)",size = 15)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(file_name, format='eps',bbox_inches = 'tight')
    plt.close()

def plot_total_recharge_time_SMILP_DATA(input_path = "/Users/idiasdas/dev/sensor_charging/milp/backup_results_17feb_timelimit1200/output_simplified/",file_name = '/Users/idiasdas/dev/sensor_charging/figures/Recharge_time_SMILP_DATA.eps'):
    """Creates a figure with the total recharge time as the number of sensors increase. Saves it as file_name.

    Args:
        input_path (str, optional): The path to the inputs used to run the schedulings algorithms. Defaults to "/Users/idiasdas/dev/sensor_charging/inputs/".
        file_name (str, optional): The path + name of the figure file that will be created. Defaults to '/Users/idiasdas/dev/sensor_charging/figures/NODRONE_50i_recharge_time_5x5_sensors_all.eps'.
    """
    s = 5
    p = 5
    i_max = 50
    drone_speed = 0.5

    fig = plt.figure()
    ax = plt.subplot(111)
    ax.set_ylim([800, 2500])
    fig.set_size_inches(6, 4)

    x_axis = range(3,11)
    algos = [{"algo":scheduling_algo_nodrone_wait_time,"label":"DATA-WT","line":"g-"},
            {"algo":scheduling_algo_nodrone_ltf,"label":"DATA-LTF","line":"b-"},
            {"algo":scheduling_algo_nodrone_stf,"label":"DATA-STF","line":"k-"},
            {"algo":scheduling_algo_nodrone_tof,"label":"DATA-ToF","line":"y-"}]
    for algo in algos:
        time_avg = []
        for d in range(3,11):
            t = 0
            for s in [5,10,15,20,30,40,50]:
                for i in range(0,i_max):
                    file = input_path+"s"+str(s)+"_p"+str(p)+"/" + str(i) + ".txt"
                    tasks = get_tasks(file)
                    done,time = algo["algo"](tasks,d,drone_speed)
                    # if(algo["algo"] != scheduling_TSP):
                    #     if(not verify_schedule(done)):
                    #         print("Improper Scheduling.")
                    #         print("\t- " + str(algo["algo"]))
                    #         print("\t- D: " + str(d) + " S: " + str(s) + " i: " + str(i))
                    #         exit(1)
                    t += time
        
            time_avg += [t/(i_max*7)]
        plt.plot(x_axis, time_avg, algo["line"],label = algo["label"])
    plt.title("SMILP + DATA")
    plt.xlabel("# Drones",size = 15)
    plt.ylabel("Total Recharge Time (s)",size = 15)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(file_name, format='eps',bbox_inches = 'tight')
    plt.close()

# print("Plotting total recharge time...")
# plot_total_recharge_time(file_name='/Users/idiasdas/dev/sensor_charging/figures/Results_nodrone.eps')
# print("Done!")

def plot_recharge_time_MILP_plus_SMILP(algos_dota,algos_data,sensors = [5,10,15,20,30,40,50],input_path = "/Users/idiasdas/dev/sensor_charging/inputs/",fig_title = "WAIT TIME", file_name = '/Users/idiasdas/dev/sensor_charging/figures/MILP_vs_SMILP-WT.eps'):
    """Plots the recharge time for the MILP and SMILP algorithms.

    Args:
        algos_dota (list): List of algorithms to be used for the MILP output.
        algos_data (list): List of algorithms to be used for the SMILP output.
        sensors (list, optional): List of numbers of sensors to be considered. Defaults to [5,10,15,20,30,40,50].
        input_path (str, optional): Path to MILP output. Defaults to "/Users/idiasdas/dev/sensor_charging/inputs/".
        fig_title (str, optional): Title for output figure. Defaults to "WAIT TIME".
        file_name (str, optional): File name for output figure. Defaults to '/Users/idiasdas/dev/sensor_charging/figures/MILP_vs_SMILP-WT.eps'.

    Returns:
        list: List with the average recharge times for each scheduling algorithm.
    """
    s = 5
    p = 5
    i_max = 50
    drone_speed = 0.5

    fig = plt.figure()
    ax = plt.subplot(111)
    ax.set_ylim([800, 2500])
    fig.set_size_inches(6, 4)

    x_axis = range(3,11)

    algos_times = []
    for algo in algos_dota:
        time_avg = []
        for d in range(3,11):
            t = 0
            for s in sensors:
                for i in range(0,i_max):
                    file = input_path+"d"+str(d)+"_s"+str(s)+"_p"+str(p)+"/" + str(i) + ".txt"
                    tasks = get_tasks(file)
                    done,time = algo["algo"](tasks,d,drone_speed)
                    t += time
        
            time_avg += [t/(i_max*7)]
        plt.plot(x_axis, time_avg, algo["line"],label = algo["label"])
        algos_times += [time_avg]

    input_path = "/Users/idiasdas/dev/sensor_charging/milp/backup_results_17feb_timelimit1200/output_simplified/"
    i_max = 100
    time_avg = []
    for algo in algos_data:
        time_avg = []
        for d in range(3,11):
            t = 0
            for s in sensors:
                for i in range(0,i_max):
                    file = input_path+"s"+str(s)+"_p"+str(p)+"/" + str(i) + ".txt"
                    tasks = get_tasks(file)
                    done,time = algo["algo"](tasks,d,drone_speed)
                    t += time
        
            time_avg += [t/(i_max*7)]
        plt.plot(x_axis, time_avg, algo["line"],label = algo["label"])
        algos_times += [time_avg]

    plt.title(fig_title)
    plt.xlabel("# Drones",size = 15)
    plt.ylabel("Total Recharge Time (s)",size = 15)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(file_name, format='eps',bbox_inches = 'tight')
    plt.close()
    return algos_times

def plot_recharge_time_with_optimal(input_path = "/Users/idiasdas/dev/sensor_charging/inputs/",file_name = '/Users/idiasdas/dev/sensor_charging/figures/RechargeTime_Optimal870Examples.eps'):
    """This is the most disgusting code I have ever written in my life. I'm sorry Alan.
    """
    s = 5
    p = 5
    i_max = 50
    print("comecou")
    drone_speed = 0.5

    results_wait_time = []
    results_longest = []
    resulsts_shortest = []
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
                        done2,wait_time = scheduling_algo_wait_time(tasks,d,drone_speed)
                        results_wait_time += [wait_time]
                        
                        tasks = get_tasks(file)
                        done2,tof = scheduling_algo_tof(tasks,d,drone_speed)
                        results_tof += [tof]
                        
                        tasks = get_tasks(file)
                        done2,shortest = scheduling_algo_shortest_tasks_first(tasks,d,drone_speed)
                        resulsts_shortest += [shortest]
                        
                        tasks = get_tasks(file)
                        done2,longest = scheduling_algo_longest_tasks_first(tasks,d,drone_speed)
                        results_longest += [longest]
                        
                        tasks = get_tasks(file)
                        done2,tsp = scheduling_TSP(tasks,d,drone_speed)
                        results_tsp += [tsp]
                        
                        tasks = get_tasks(file)
                        done2,nodrone_wt = scheduling_algo_nodrone_wait_time(tasks,d,drone_speed)
                        results_nodrone_wait_time += [nodrone_wt]
                        
                        tasks = get_tasks(file)
                        done2,nodrone_tof = scheduling_algo_nodrone_tof(tasks,d,drone_speed)
                        results_nodrone_tof += [nodrone_tof]
                        
                        tasks = get_tasks(file)
                        done2,nodrone_shortest = scheduling_algo_nodrone_stf(tasks,d,drone_speed)
                        results_nodrone_shortest += [nodrone_shortest]
                        
                        tasks = get_tasks(file)
                        done2,nodrone_longest = scheduling_algo_nodrone_ltf(tasks,d,drone_speed)
                        results_nodrone_longest += [nodrone_longest]
    
    results_optimal = []
    file = open("/Users/idiasdas/dev/sensor_charging/optimal_output/backup_optimal_results_GLOBECOM.txt", 'r')
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
                        avg_shortest += resulsts_shortest[j]
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

def plot_solution_times_per_drones(sensors = [5,10,15,20,30,40,50],input_path = "/Users/idiasdas/dev/sensor_charging/inputs/",file_name = '/Users/idiasdas/dev/sensor_charging/figures/MILP_Simplified_vs_OLD_MILP.eps'):
    """  Plots the solution times for the simplified MILP and the old MILP for different number of drones.

    Args:
        sensors (list, optional): List with numbers of sensors to plot. Defaults to [5,10,15,20,30,40,50].
        input_path (str, optional): Path to old MILP inputs. Defaults to "/Users/idiasdas/dev/sensor_charging/inputs/".
        file_name (str, optional): Name of the created figure file. Defaults to '/Users/idiasdas/dev/sensor_charging/figures/MILP_Simplified_vs_OLD_MILP.eps'.
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

    input_path = "/Users/idiasdas/dev/sensor_charging/milp/backup_results_17feb_timelimit1200/output_simplified/"
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

def plot_solution_times_per_sensors(sensors = [5,10,15,20,30,40,50],input_path = "/Users/idiasdas/dev/sensor_charging/inputs/",file_name = '/Users/idiasdas/dev/sensor_charging/figures/MILP_Simplified_vs_OLD_MILP.eps'):
    """Plots the solution times for the simplified MILP and the old MILP for different number of sensors.
        Solves the models for 3 to 10 drones.
        Considers 50 instances for each number of sensors.


    Args:
        sensors (list, optional): List of sensors to plot. Defaults to [5,10,15,20,30,40,50].
        input_path (str, optional): path to MILP output . Defaults to "/Users/idiasdas/dev/sensor_charging/inputs/".
        file_name (str, optional): Output figure file name. Defaults to '/Users/idiasdas/dev/sensor_charging/figures/MILP_Simplified_vs_OLD_MILP.eps'.
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

    input_path = "/Users/idiasdas/dev/sensor_charging/milp/backup_results_17feb_timelimit1200/output_simplified/"
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