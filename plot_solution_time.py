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