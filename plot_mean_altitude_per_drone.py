import matplotlib.pyplot as plt
from basic_functions import *

def plot_mean_altitude_per_drone(input_path = "/Users/idiasdas/dev/GLOBECOM2022/inputs/", file_name = "/Users/idiasdas/dev/sensor_charging/figures/50i_mean_altitude_per_drone_5x5.eps"):
    """Plots and saves the figure with the average altitude of the drones.
       Considers 20 instances for each possible combination of the global parameters. 
       Sensors = 5,10,15,20,30,40 and 50.
       Drones from 3 to 11.
       25 positions (p=5).

    Args:
        input_path (str, optional): Directory path for the inputs. Defaults to "/Users/idiasdas/dev/GLOBECOM2022/inputs/".
        file_name (str, optional): Path + name of figure file. Defaults to "/Users/idiasdas/dev/sensor_charging/figures/50i_mean_altitude_per_drone_5x5.eps".
    """
    p = 5
    i_max = 20
    drone_speed = 0.5

    sensors = [5,10,15,20,30,40,50]
    colors = ["b-","g-","y-","r-","c-","k-","m-"]
    x_line = range(3,11)

    fig = plt.figure()
    ax = plt.subplot(111)
    fig.set_size_inches(6, 4)


    for s in range(len(sensors)):
        avg_h_per_d = []
        for d in range(3,11):
            total_h = 0
            for i in range(0,20):
                file = input_path + "d"+str(d)+"_s"+str(sensors[s])+"_p"+str(p)+"/" + str(i) + ".txt"
                tasks = get_tasks(file)
                for task in tasks:
                    total_h += task["position"][2]/len(tasks)
                total_h = total_h
            avg_h_per_d += [total_h/20]
        d = range(3,11)
        plt.plot(d, avg_h_per_d, colors[s], label = str(sensors[s]) + " sensors")

    plt.ylim([0, 2])
    plt.legend(loc=4,ncol=2)
    plt.xlabel("# Drones",size = 15)
    plt.ylabel("Mean altitude per drone (m)",size = 15)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.tight_layout()
    plt.savefig(file_name, format='eps')
    plt.close()

def plot_mean_altitude_per_drone_SMILP(input_path = "/Users/idiasdas/dev/sensor_charging/milp/backup_results_17feb_timelimit1200/output_simplified/", file_name = "/Users/idiasdas/dev/sensor_charging/figures/mean_altitude_SMILP.eps"):
    """Plots and saves the figure with the average altitude of the drones for the simplified MILP (SMILP).
       Considers 20 instances for each possible combination of the global parameters. 
       Sensors = 5,10,15,20,30,40 and 50.
       Drones from 3 to 11.
       25 positions (p=5).

    Args:
        input_path (str, optional): Directory path for the inputs. Defaults to "/Users/idiasdas/dev/GLOBECOM2022/inputs/".
        file_name (str, optional): Path + name of figure file. Defaults to "/Users/idiasdas/dev/sensor_charging/figures/50i_mean_altitude_per_drone_5x5.eps".
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
        avg_h_per_d = []
        for d in range(3,11):
            total_h = 0
            for i in range(0,20):
                file = input_path + "s"+str(sensors[s])+"_p"+str(p)+"/" + str(i) + ".txt"
                tasks = get_tasks(file)
                for task in tasks:
                    total_h += task["position"][2]/len(tasks)
                total_h = total_h
            avg_h_per_d += [total_h/20]
        d = range(3,11)
        plt.plot(d, avg_h_per_d, colors[s], label = str(sensors[s]) + " sensors")

    plt.ylim([0, 2])
    plt.legend(loc=4,ncol=2)
    plt.xlabel("# Drones",size = 15)
    plt.ylabel("Mean altitude per drone (m)",size = 15)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.tight_layout()
    plt.savefig(file_name, format='eps')
    plt.close()