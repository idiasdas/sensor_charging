import matplotlib.pyplot as plt
from basic_functions import *
def plot_mean_number_of_positions(input_path = "/Users/idiasdas/dev/GLOBECOM2022/inputs/",file_name = 'figures/50i_mean_pos_per_drone_5x5.eps'):
    """Plots and saves the figure with the average number of positions visited by the drones.
       Considers 50 instances for each possible combination of the global parameters. 
       Sensors = 5,10,15,20,30,40 and 50.
       Drones from 3 to 11.
       25 positions (p=5).

    Args:
        input_path (str, optional): Directory with the inputs. Defaults to "/Users/idiasdas/dev/GLOBECOM2022/inputs/".
        file_name (str, optional): Path + name of figure file. Defaults to 'figures/50i_mean_pos_per_drone_5x5.eps'.
    """
    p = 5
    i_max = 50 # Numbe of instances considered for each combination of global parameters
    drone_speed = 0.5

    sensors = [5,10,15,20,30,40,50]
    colors = ["b-","g-","y-","r-","c-","k-","m-"]
    x_line = range(3,11)

    fig = plt.figure()
    ax = plt.subplot(111)
    fig.set_size_inches(6, 4)


    for s in range(len(sensors)):
        avg_p_per_d = []
        for d in range(3,11):
            total_tasks = 0
            for i in range(0,i_max):
                file = input_path+"d"+str(d)+"_s"+str(sensors[s])+"_p"+str(p)+"/" + str(i) + ".txt"
                tasks = get_tasks(file)
                total_tasks += len(tasks)/d
            avg_p_per_d += [total_tasks/(i_max)]
        plt.plot(x_line, avg_p_per_d, colors[s], label = str(str(sensors[s])) + " sensors")

        
    # plt.legend(loc = 2)
    # ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.legend(loc='upper right')

    # plt.legend()
    plt.xlabel("# Drones",size = 15)
    plt.ylabel("Mean number of positions / drone",size = 15)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.tight_layout()
    plt.savefig(file_name, format='eps',bbox_inches = 'tight')
    plt.close()

def plot_mean_number_of_positions_SMILP(input_path = "milp/backup_results_17feb_timelimit1200/output_simplified/",file_name = 'figures/avg_pos_per_drone_SMILP.eps'):
    """Plots and saves the figure with the average number of positions visited by the drones for the simplified MILP (SMILP).
       Considers 50 instances for each possible combination of the global parameters. 
       Sensors = 5,10,15,20,30,40 and 50.
       Drones from 3 to 11.
       25 positions (p=5).

    Args:
        input_path (str, optional): Directory with the inputs. Defaults to "/Users/idiasdas/dev/GLOBECOM2022/inputs/".
        file_name (str, optional): Path + name of figure file. Defaults to 'figures/50i_mean_pos_per_drone_5x5.eps'.
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
        avg_p_per_d = []
        for d in range(3,11):
            total_tasks = 0
            for i in range(0,i_max):
                file = input_path+"s"+str(sensors[s])+"_p"+str(p)+"/" + str(i) + ".txt"
                tasks = get_tasks(file)
                total_tasks += len(tasks)/d
            avg_p_per_d += [total_tasks/(i_max)]
        plt.plot(x_line, avg_p_per_d, colors[s], label = str(str(sensors[s])) + " sensors")

        
    # plt.legend(loc = 2)
    # ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.legend(loc='upper right')

    # plt.legend()
    plt.xlabel("# Drones",size = 15)
    plt.ylabel("Mean number of positions / drone",size = 15)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.tight_layout()
    plt.savefig(file_name, format='eps',bbox_inches = 'tight')
    plt.close()
