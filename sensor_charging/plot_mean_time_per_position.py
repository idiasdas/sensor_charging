from basic_functions import *
import matplotlib.pyplot as plt

def plot_mean_time_per_position(input_path = "/Users/idiasdas/dev/GLOBECOM2022/inputs/",file_name = 'figures/50i_mean_time_per_pos_5x5.eps'):
    """Plots and saves the figure with the average time spent in eahc position visited by the drones.
       Considers 50 instances for each possible combination of the global parameters. 
       Sensors = 5,10,15,20,30,40 and 50.
       Drones from 3 to 11.
       25 positions (p=5).

    Args:
        input_path (str, optional): Path to the input files. Defaults to "/Users/idiasdas/dev/GLOBECOM2022/inputs/".
        file_name (str, optional): Filename for the output figure. Defaults to 'figures/50i_mean_time_per_pos_5x5.eps'.
    """
    p = 5
    i_max = 50
    drone_speed = 0.5

    sensors = [5,10,15,20,30,40,50]
    colors = ["b-","g-","y-","r-","c-","k-","m-"]
    x_line = range(3,11)

    fig = plt.figure()
    ax = plt.subplot(111)
    fig.set_size_inches(6, 4)


    for s in range(len(sensors)):
        avg_t_per_p = []
        for d in range(3,11):
            total_time_per_p = 0
            for i in range(0,i_max):
                file = input_path + "d"+str(d)+"_s"+str(sensors[s])+"_p"+str(p)+"/" + str(i) + ".txt"
                tasks = get_tasks(file)
                for task in tasks:
                    total_time_per_p += task["time"]/len(tasks)
            avg_t_per_p += [total_time_per_p/i_max]
        plt.plot(x_line, avg_t_per_p, colors[s], label = str(sensors[s]) + " sensors")
        
    # plt.legend(loc = 2)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # plt.legend()
    plt.legend(loc=4,ncol=2)
    plt.ylim([0, 500])
    plt.xlabel("# Drones",size = 15)
    plt.ylabel("Mean time per position (s) ",size = 15)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.tight_layout()
    plt.savefig(file_name, format='eps')
    plt.close()

def plot_mean_time_per_position_SMILP(input_path = "milp/backup_results_17feb_timelimit1200/output_simplified/",file_name = 'figures/50i_mean_time_per_pos_5x5_SMILP.eps'):
    """Plots and saves the figure with the average time spent in eahc position visited by the drones.
       Considers 50 instances for each possible combination of the global parameters. 
       Sensors = 5,10,15,20,30,40 and 50.
       Drones from 3 to 11.
       25 positions (p=5).

    Args:
        input_path (str, optional): Path to the input files. Defaults to "/Users/idiasdas/dev/GLOBECOM2022/inputs/".
        file_name (str, optional): Filename for the output figure. Defaults to 'figures/50i_mean_time_per_pos_5x5.eps'.
    """
    p = 5
    i_max = 100
    drone_speed = 0.5

    sensors = [5,10,15,20,30,40,50]
    colors = ["b-","g-","y-","r-","c-","k-","m-"]
    x_line = range(3,11)

    fig = plt.figure()
    ax = plt.subplot(111)
    fig.set_size_inches(6, 4)


    for s in range(len(sensors)):
        avg_t_per_p = []
        for d in range(3,11):
            total_time_per_p = 0
            for i in range(0,i_max):
                file = input_path + "s"+str(sensors[s])+"_p"+str(p)+"/" + str(i) + ".txt"
                tasks = get_tasks(file)
                for task in tasks:
                    total_time_per_p += task["time"]/len(tasks)
            avg_t_per_p += [total_time_per_p/i_max]
        plt.plot(x_line, avg_t_per_p, colors[s], label = str(sensors[s]) + " sensors")
        
    # plt.legend(loc = 2)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # plt.legend()
    plt.legend(loc=4,ncol=2)
    plt.ylim([0, 500])
    plt.xlabel("# Drones",size = 15)
    plt.ylabel("Mean time per position (s) ",size = 15)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.tight_layout()
    plt.savefig(file_name, format='eps')
    plt.close()


def plot_mean_time_per_position_SMILP_per_sensors(input_path = "milp/backup_results_17feb_timelimit1200/output_simplified/",file_name = 'figures/50i_mean_time_per_pos_5x5_SMILP_per_sensors.eps'):
    """Plots the time per task for different numbers of sensors.
       Considers 50 instances for each possible combination of the global parameters. 
       Sensors = 5,10,15,20,30,40 and 50.
       Drones from 3 to 11.
       25 positions (p=5).

    Args:
        input_path (str, optional): Path to the input files. Defaults to "/Users/idiasdas/dev/GLOBECOM2022/inputs/".
        file_name (str, optional): Filename for the output figure. Defaults to 'figures/50i_mean_time_per_pos_5x5.eps'.
    """
    p = 5
    i_max = 100
    drone_speed = 0.5

    sensors = [5,10,15,20,30,40,50]
    # colors = ["b","g","y","r","c","k","m"]
    x_line = range(len(sensors))

    fig = plt.figure()
    ax = plt.subplot(111)
    fig.set_size_inches(6, 4)

    avg_t_per_p = []
    for s in range(len(sensors)):
        total_time_per_p = 0
        for i in range(0,i_max):
            file = input_path + "s"+str(sensors[s])+"_p"+str(p)+"/" + str(i) + ".txt"
            tasks = get_tasks(file)
            for task in tasks:
                total_time_per_p += task["time"]/len(tasks)
        avg_t_per_p += [total_time_per_p/i_max]
        # ax.bar(s,total_time_per_p/i_max, color = colors[s])
    plt.plot(x_line, avg_t_per_p)
    
    # plt.legend(loc = 2)
    # ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # plt.legend()
    # plt.legend(loc=4,ncol=2)

    plt.ylim([0, 500])
    plt.xlabel("# Sensors",size = 15)
    plt.ylabel("Mean time per position (s) ",size = 15)
    plt.xticks(range(len(sensors)),labels = sensors,fontsize=14)
    plt.yticks(fontsize=14)
    plt.tight_layout()
    plt.savefig(file_name, format='eps')
    plt.close()