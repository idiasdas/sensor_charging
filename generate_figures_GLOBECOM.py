from basic_functions import *

from scheduling_ToF import *
from scheduling_nodrone_ToF import *

from scheduling_wait_time import *
from scheduling_nodrone_wait_time import *

from scheduling_longest_tasks_first import *
from scheduling_nodrone_longest_tasks_first import *

from scheduling_shortest_tasks_first import *
from scheduling_nodrone_shortest_tasks_first import *

from plot_total_recharge_time import *



def drone_based_plus_old_optimal870(file_name = 'figures/RechargeTime_Optimal870Examples.eps'):
    """Plots the recharge time for all algorithms on the 870 instances in which we computed the optimal solution.
     This function is extremeally disgusting and should be replaced. """
    # plot_recharge_time_with_optimal()
    algos = [
            {"algo":scheduling_algo_tof,"label":"DB-ToF","line":"y-"},
            {"algo":scheduling_algo_wait_time,"label":"DB-WT","line":"g-"},
            {"algo":scheduling_algo_shortest_tasks_first,"label":"DB-STF","line":"k-"},
            {"algo":scheduling_algo_longest_tasks_first,"label":"DB-LTF","line":"b-"},
            {"algo":scheduling_TSP,"label":"TSP","line":"r-"}]
    
    plot_recharge_time_with_optimal_revised(algos, file_name = "figures/onecanonlyhope.eps")


def DBLP_DB_algos(old = False):
    """Plots the total recharge time for th eold drone based algorithms as shown in the paper for GLOBECOM 2022. 
    
    New names:
        MILP = Drone based linear program
        DOTA = Drone based scheduling algorithm
    """
    if old:
        algos = [
            {"algo":scheduling_algo_tof,"label":"DB-ToF","line":"y-"},
            {"algo":scheduling_algo_wait_time,"label":"DB-WT","line":"g-"},
            {"algo":scheduling_algo_shortest_tasks_first,"label":"DB-STF","line":"k-"},
            {"algo":scheduling_algo_longest_tasks_first,"label":"DB-LTF","line":"b-"},
            {"algo":scheduling_TSP,"label":"TSP","line":"r-"}]
        fig_title = "DB-LP + OLD DB Algorithms"
        plot_total_recharge_time(algos,fig_title,file_name='figures/Recharge_time_DBLP_DBalgos.eps')
    else:
        algos = [
            {"algo":scheduling_algo_tof_optimized,"label":"DB-ToF","line":"y-"},
            {"algo":scheduling_algo_wait_time_optimized,"label":"DB-WT","line":"g-"},
            {"algo":scheduling_algo_shortest_tasks_first_optimized,"label":"DB-STF","line":"k-"},
            {"algo":scheduling_algo_longest_tasks_first_optimized,"label":"DB-LTF","line":"b-"},
            {"algo":scheduling_TSP,"label":"TSP","line":"r-"}]
        fig_title = "DB-LP + Optimized DB Algorithms"
        plot_total_recharge_time(algos,fig_title,file_name='figures/Recharge_time_DBLP_DBalgos.eps')


def DBLP_SB_algos():
    algos = [
            {"algo":scheduling_algo_nodrone_tof_revised,"label":"SB-ToF","line":"y-"},
            {"algo":scheduling_algo_nodrone_wt_revised,"label":"SB-WT","line":"g-"},
            {"algo":scheduling_algo_nodrone_stf_revised,"label":"SB-STF","line":"k-"},
            {"algo":scheduling_algo_nodrone_ltf_revised,"label":"SB-LTF","line":"b-"}]
    fig_title = "DB-LP + NEW SB Algorithms"
    plot_total_recharge_time(algos,fig_title,file_name='figures/Recharge_time_DBLP_SBalgos.eps')


def SBLP_SB_algos(old = False):
    """Plots the total recharge time for the sensor based algorithms with the SB-LP as input."""
    if old:
        algos = [
            {"algo":scheduling_algo_nodrone_tof,"label":"SB-ToF","line":"y-"},
            {"algo":scheduling_algo_nodrone_wait_time,"label":"SB-WT","line":"g-"},
            {"algo":scheduling_algo_nodrone_stf,"label":"SB-STF","line":"k-"},
            {"algo":scheduling_algo_nodrone_ltf,"label":"SB-LTF","line":"b-"}]
        fig_title = "SB-LP + OLD SB Algorithms"
        plot_total_recharge_time_SMILP_DATA(algos, fig_title = fig_title,file_name='figures/Recharge_time_SBLP_SBalgos.eps')
    else:
        algos = [
            {"algo":scheduling_algo_nodrone_tof_revised,"label":"SB-ToF","line":"y-"},
            {"algo":scheduling_algo_nodrone_wt_revised,"label":"SB-WT","line":"g-"},
            {"algo":scheduling_algo_nodrone_stf_revised,"label":"SB-STF","line":"k-"},
            {"algo":scheduling_algo_nodrone_ltf_revised,"label":"SB-LTF","line":"b-"}]
        fig_title = "SB-LP + NEW SB Algorithms"
        plot_total_recharge_time_SMILP_DATA(algos,fig_title = fig_title,file_name='figures/Recharge_time_SBLP_SBalgos.eps')

drone_based_plus_old_optimal870()
DBLP_DB_algos()
DBLP_SB_algos()
SBLP_SB_algos()