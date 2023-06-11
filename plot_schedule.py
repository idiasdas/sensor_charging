from basic_functions import *
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def plot_schedule(tasks,n_drones,end_time, x_lim = -1, title = "", save = False,file_name = '/Users/idiasdas/dev/sensor_charging/figures/schedule.eps'):
    """Plots time diagram with the schedule of the tasks.

    Args:
        tasks (int): Total number of tasks.
        n_drones (int): Number of available drones.
        end_time (float): Final time of the schedule.
        x_lim (int, optional): Limits the horizontal size of the figure in seconds. Defaults to -1.
        title (str, optional): Figure title. Defaults to "".
        save (bool, optional): If true, saves the output figure. Defaults to False.
        file_name (str, optional): File name for the output figure. Defaults to '/Users/idiasdas/dev/sensor_charging/figures/schedule.eps'.
    """
    fig, ax = plt.subplots()
    fig.set_size_inches(15.5, 8.5)
    if(x_lim != -1):
        plt.xlim([-50, x_lim])
    else:
        plt.xlim([-50, end_time + 100])
    plt.ylim([-1, n_drones])
    y = range(-1,n_drones) # to give a little space on the bottom
    my_yticks = [str(tick) if tick in range(n_drones) else "" for tick in y] # only shows the drones ids
    plt.yticks(y, my_yticks)
    for task in tasks:
        ax.add_patch(Rectangle(( task["start"] ,task["drone"] - 0.3), task["end"] - task["start"], 0.6,
                              edgecolor = 'black',lw = 2,fill=False))
        ax.plot([ task["start"] - task["ToF"], task["start"] ],[ task["drone"], task["drone"]],"k-", color='red',lw = 2,label = str(task["id"]) + " = " + str(task["sensors"]))
        cx = task["start"] +(task["end"] - task["start"])/2
        cy = task["drone"]
#         ax.annotate(str(task["id"]), (cx, cy), color='k', weight='bold', fontsize=20, ha='center', va='center')
        ax.annotate(str(task["id"]), (cx, cy), color='k', fontsize=20, ha='center', va='center')
    
#     ax.annotate("Total time: " + str(end_time), (end_time/2, n_drones  - 0.2), color='black', weight='bold', fontsize=20, ha='center', va='center')
    ax.annotate(title, (end_time/2, n_drones  - 0.2), color='black', weight='bold', fontsize=20, ha='center', va='center')
    
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
#     ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
#     plt.legend(loc = 4,fontsize=12)
#     ax.legend(loc=4, bbox_to_anchor=(1.15, 0),fontsize=13)
    plt.xlabel("Time (s) ",size = 30)
    plt.ylabel("Drones",size = 30)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=25)
    if(save):
        plt.savefig(file_name, format='eps',bbox_inches = 'tight')
    plt.close()
    
    

