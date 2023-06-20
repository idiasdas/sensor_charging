import numpy as np
import matplotlib.pyplot as plt
from basic_functions import *
from scheduling_ToF import *
from scheduling_wait_time import *
from scheduling_shortest_tasks_first import *
from scheduling_longest_tasks_first import *
from scheduling_nodrone_wait_time import *
from scheduling_nodrone_ToF import *
from scheduling_nodrone_longest_tasks_first import *
from scheduling_nodrone_shortest_tasks_first import *

def plot_idle_time(inputs_path = "/Users/idiasdas/dev/GLOBECOM2022/inputs/", file_name = "figures/DATAvsDOTA_idletime.eps"):
    """Creates and saves an eps figure with the average time in which the drones stay idle as the number of drones changes for each algorithm.
       Considers the 50 instances of examples with 50 sensors and 25 positions (p = 5)    

    Args:
        inputs_path (str, optional): Directory path with input files. Defaults to "/Users/idiasdas/dev/GLOBECOM2022/inputs/".
        file_name (str, optional): Path + name of image file (eps figure). Defaults to "figures/idle_time.eps".
    """
    s = 50
    p = 5
    i_max = 50
    drone_speed = 0.5
    fig = plt.figure()
    ax = plt.subplot(111)
    ax.set_ylim([0, 2300])
    fig.set_size_inches(6, 4)
    x_axis = range(3,11)
    algos = [{"algo":scheduling_DB_TOF,"label":"DOTA-ToF","line":"y-"},
            {"algo":scheduling_DB_WT,"label":"DOTA-WT","line":"g-"},
            {"algo":scheduling_DB_STF,"label":"DOTA-STF","line":"k-"},
            {"algo":scheduling_DB_LTF,"label":"DOTA-LTF","line":"b-"}]
            # {"algo":scheduling_TSP,"label":"TSP","line":"r-"},
            # {"algo":scheduling_algo_nodrone_wait_time,"label":"DATA-WT","line":"g-"},
            # {"algo":scheduling_algo_nodrone_ltf,"label":"DATA-LTF","line":"b-"},
            # {"algo":scheduling_algo_nodrone_stf,"label":"DATA-STF","line":"k-"},
            # {"algo":scheduling_algo_nodrone_tof,"label":"DATA-ToF","line":"y-"}]
    for algo in algos:
        time_avg = []
        for d in range(3,11):
            t = 0
            for i in range(0,i_max):
                file = inputs_path + "d"+str(d)+"_s"+str(s)+"_p"+str(p)+"/" + str(i) + ".txt"
                tasks = get_tasks(file)
                done,time = algo["algo"](tasks,d,drone_speed)
                total_time, tof, wait_time = get_all_times(d,done) # wait_time here is idle_time
                t += wait_time
        
            time_avg += [t/i_max]
        plt.plot(x_axis, time_avg, algo["line"],label = algo["label"])

    # plt.legend()
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.xlabel("# Drones",size = 15)
    plt.ylabel("Idle Time (s)",size = 15)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.savefig(file_name, format='eps',bbox_inches = 'tight')
    plt.close()

def plot_idle_time_plus_std(inputs_path = "/Users/idiasdas/dev/GLOBECOM2022/inputs/", file_name = "figures/DATAvsDOTA_idletime.eps"):
    """Creates and saves an eps figure with the average time in which the drones stay idle as the number of drones changes for each algorithm.
       Considers the 50 instances of examples with 50 sensors and 25 positions (p = 5)    

    Args:
        inputs_path (str, optional): Directory path with input files. Defaults to "/Users/idiasdas/dev/GLOBECOM2022/inputs/".
        file_name (str, optional): Path + name of image file (eps figure). Defaults to "figures/idle_time.eps".
    """
    s = 50
    p = 5
    i_max = 50
    drone_speed = 0.5
    fig = plt.figure()
    ax = plt.subplot(111)
    fig.set_size_inches(6, 4)
    x_axis = range(3,11)
    algos = [#{"algo":scheduling_algo_tof,"label":"ToF","line":"y-","linestyle":"-","color":"y"},
            {"algo":scheduling_DB_WT,"label":"DOTA-WT","line":"g-","linestyle":"-","color":"g"},
            # {"algo":scheduling_algo_shortest_tasks_first,"label":"Shortest Tasks First","line":"k-","linestyle":"-","color":"b"},
            # {"algo":scheduling_algo_longest_tasks_first,"label":"Longest Tasks First","line":"b-","linestyle":"-","color":"k"},
            # {"algo":scheduling_TSP,"label":"TSP","line":"r-"},
            {"algo":scheduling_algo_nodrone_wait_time,"label":"DATA-WT","line":"b--","linestyle":"--","color":"b"},
            # {"algo":scheduling_algo_nodrone_ltf,"label":"DATA-LTF","line":"b--","linestyle":"--","color":"b"},
            # {"algo":scheduling_algo_nodrone_stf,"label":"DATA-STF","line":"k--","linestyle":"--","color":"k"},
            # {"algo":scheduling_algo_nodrone_tof,"label":"DATA-ToF","line":"y--","linestyle":"--","color":"y"}
            ]
    for algo in algos:
        time_avg = []
        time_std = []
        for d in range(3,11):
            t = 0
            idle_times_list = []
            for i in range(0,i_max):
                file = inputs_path + "d"+str(d)+"_s"+str(s)+"_p"+str(p)+"/" + str(i) + ".txt"
                tasks = get_tasks(file)
                done,time = algo["algo"](tasks,d,drone_speed)
                total_time, tof, wait_time = get_all_times(d,done) # wait_time here is idle_time
                idle_times_list += [wait_time]
                t += wait_time
        
            time_avg += [t/i_max]
            time_std += [np.std(idle_times_list)]
        # plt.plot(x_axis, time_avg, algo["line"],label = algo["label"])
        plt.errorbar(x_axis, time_avg, time_std, linestyle = algo["linestyle"],color = algo["color"], marker='None',capsize=3,label = algo["label"])

    # plt.legend()
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.xlabel("# Drones",size = 15)
    plt.ylabel("Idle Time (s)",size = 15)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.savefig(file_name, format='eps',bbox_inches = 'tight')
    plt.close()

def plot_total_idle_time_SMILP_DATA(input_path = "milp/backup_results_17feb_timelimit1200/output_simplified/",file_name = 'figures/Idletime_SMILP_DATA.eps'):
    """Creates a figure with the total idle time as the number of sensors increase. Saves it as file_name.

    Args:
        input_path (str, optional): The path to the inputs used to run the schedulings algorithms. Defaults to "inputs/".
        file_name (str, optional): The path + name of the figure file that will be created. Defaults to 'figures/Idletime_SMILP_DATA.eps'.
    """
    s = 5
    p = 5
    i_max = 50
    drone_speed = 0.5

    fig = plt.figure()
    ax = plt.subplot(111)
    ax.set_ylim([0, 2300])
    fig.set_size_inches(6, 4)

    x_axis = range(3,11)
    algos = [{"algo":scheduling_algo_nodrone_wait_time,"label":"DATA-WT","line":"g-"},
            {"algo":scheduling_algo_nodrone_ltf,"label":"DATA-LTF","line":"b-"},
            {"algo":scheduling_algo_nodrone_stf,"label":"DATA-STF","line":"k-"},
            {"algo":scheduling_SB_TOF,"label":"DATA-ToF","line":"y-"}]
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
                    total_time, tof, wait_time = get_all_times(d,done) # wait_time here is idle_time
                    t += wait_time
        
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