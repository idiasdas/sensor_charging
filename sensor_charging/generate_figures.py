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
from plot_solution_time import *
from plot_idle_time import *
from plot_schedule import *

from plot_mean_altitude_per_drone import *
from plot_mean_number_of_positions import *
from plot_mean_time_per_position import *

def RT_with_optimal(file_path = "figures/old_optimal/"):
    db_old_algos = [
        {"algo": scheduling_DB_TOF,             "label": "DB-TOF",      "line": "y-"},
        {"algo": scheduling_DB_WT,              "label": "DB-WT",       "line": "g-"},
        {"algo": scheduling_DB_STF,             "label": "DB-STF",      "line": "k-"},
        {"algo": scheduling_DB_LTF,             "label": "DB-LTF",      "line": "b-"},
        {"algo": scheduling_TSP,                "label": "TSP",         "line": "r-"}]

    db_optimimzed_algos = [
        {"algo": scheduling_DB_TOF_optimized,   "label": "DB-TOF",      "line": "y-"},
        {"algo": scheduling_DB_WT_optimized,    "label": "DB-WT",       "line": "g-"},
        {"algo": scheduling_DB_STF_optimized,   "label": "DB-STF",      "line": "k-"},
        {"algo": scheduling_DB_LTF_optimized,   "label": "DB-LTF",      "line": "b-"},
        {"algo": scheduling_TSP,                "label": "TSP",         "line": "r-"}]

    sb_revised_algos_plusTSP = [
        {"algo": scheduling_SB_TOF_revised,     "label": "SB-TOF",      "line": "y-"},
        {"algo": scheduling_SB_WT_revised,      "label": "SB-WT",       "line": "g-"},
        {"algo": scheduling_SB_STF_revised,     "label": "SB-STF",      "line": "k-"},
        {"algo": scheduling_SB_LTF_revised,     "label": "SB-LTF",      "line": "b-"},
        {"algo": scheduling_TSP,                "label": "TSP",         "line": "r-"}]

    # DB-LP inputs + old DB algorithms + optimal from GLOBECOM backup
    plot_recharge_time_with_optimal_revised(db_old_algos, file_name = file_path + "RT_DBLP_OLD_DB_algos_OPTIMAL.eps", fig_title="OLD DB Algorithms (870)")

    # DB-LP inputs + optimized DB algorithms + optimal from GLOBECOM backup
    plot_recharge_time_with_optimal_revised(db_optimimzed_algos, file_name = file_path + "RT_DBLP_Optimized_DB_OPTIMAL.eps", fig_title="")

    # DB-LP inputs + revised SB algorithms + optimal from GLOBECOM backup
    plot_recharge_time_with_optimal_revised(sb_revised_algos_plusTSP, file_name = file_path + "RT_DBLP_Revised_SB_OPTIMAL.eps", fig_title="")


def RT_comparison(file_path = "figures/new_figures/"):
    db_optimimzed_algos_plusTSP = [
        {"algo": scheduling_DB_TOF_optimized,    "label": "Time of Flight",        "line": "y-"},
        {"algo": scheduling_DB_WT_optimized,     "label": "Wait Time",         "line": "g-"},
        {"algo": scheduling_DB_STF_optimized,    "label": "Shortest First",        "line": "k-"},
        {"algo": scheduling_DB_LTF_optimized,    "label": "Longest First",        "line": "b-"},
        {"algo": scheduling_TSP,                 "label": "TSP",        "line": "r-"}]

    sb_revised_algos_plusTSP = [
        {"algo": scheduling_SB_TOF_revised,      "label": "SB-TOF",        "line": "y-"},
        {"algo": scheduling_SB_WT_revised,       "label": "SB-WT",         "line": "g-"},
        {"algo": scheduling_SB_STF_revised,      "label": "SB-STF",        "line": "k-"},
        {"algo": scheduling_SB_LTF_revised,      "label": "SB-LTF",        "line": "b-"},
        {"algo": scheduling_TSP,                 "label": "SB-TSP",        "line": "r-"}]

    sb_revised_algos = [
        {"algo": scheduling_SB_TOF_revised,      "label": "SB-TOF",        "line": "y-"},
        {"algo": scheduling_SB_WT_revised,       "label": "SB-WT",         "line": "g-"},
        {"algo": scheduling_SB_STF_revised,      "label": "SB-STF",        "line": "k-"},
        {"algo": scheduling_SB_LTF_revised,      "label": "SB-LTF",        "line": "b-"}]

    # DB-LP inputs + DB algorithms + TSP
    plot_total_recharge_time(algos=db_optimimzed_algos_plusTSP, file_name = file_path + "RT_DBLP_DB_ALGOS.eps", fig_title=" ", legend_style=2)

    # DB-LP inputs + SB algorithms + TSP
    plot_total_recharge_time(algos=sb_revised_algos_plusTSP, file_name = file_path + "RT_DBLP_SB_ALGOS.eps", fig_title="DB-LP + SB Algorithms", legend_style=1)

    # SB-LP inputs + SB algorithms
    plot_total_recharge_time(algos=sb_revised_algos,input_style = 1, file_name = file_path + "RT_SBLP_SB_ALGOS.eps", fig_title="SB-LP + SB Algorithms", legend_style=1)

def DB_versus_SB(file_path = "figures/new_figures/"):
    db_tof = {"algo": scheduling_DB_TOF_optimized,      "label": "DB-LP + DB-TOF",      "line": "r-"}
    db_wt  = {"algo": scheduling_DB_WT_optimized,       "label": "Drone-Based WT",       "line": "r-"}
    db_stf = {"algo": scheduling_DB_STF_optimized,      "label": "DB-LP + DB-STF",      "line": "r-"}
    db_ltf = {"algo": scheduling_DB_LTF_optimized,      "label": "DB-LP + DB-LTF",      "line": "r-"}


    dblp_sb_tof = {"algo": scheduling_SB_TOF_revised,   "label": "DB-LP + SB-TOF",      "line": "g-"}
    dblp_sb_wt  = {"algo": scheduling_SB_WT_revised,    "label": "DB-LP + SB-WT",       "line": "g-"}
    dblp_sb_stf = {"algo": scheduling_SB_STF_revised,   "label": "DB-LP + SB-STF",      "line": "g-"}
    dblp_sb_ltf = {"algo": scheduling_SB_LTF_revised,   "label": "DB-LP + SB-LTF",      "line": "g-"}

    sb_tof = {"algo": scheduling_SB_TOF_revised,        "label": "SB-LP + SB-TOF",      "line": "b-"}
    sb_wt  = {"algo": scheduling_SB_WT_revised,         "label": "Sensor-Based WT",       "line": "b-"}
    sb_stf = {"algo": scheduling_SB_STF_revised,        "label": "SB-LP + SB-STF",      "line": "b-"}
    sb_ltf = {"algo": scheduling_SB_LTF_revised,        "label": "SB-LP + SB-LTF",      "line": "b-"}

    plot_recharge_time_DBLP_plus_SBLP(algos_db=[db_tof,dblp_sb_tof],    algos_sb=[sb_tof],  fig_title = "Time of Filght (TOF)",         file_name=file_path + "RT_TOF.eps", legend_style=1)
    plot_recharge_time_DBLP_plus_SBLP(algos_db=[db_wt,dblp_sb_wt],      algos_sb=[sb_wt],   fig_title = "Wait Time (WT)",               file_name=file_path + "RT_WT.eps",  legend_style=1)
    plot_recharge_time_DBLP_plus_SBLP(algos_db=[db_wt],      algos_sb=[sb_wt],   fig_title = " ",               file_name=file_path + "DB_vs_SB_WT.eps",  legend_style=1)
    plot_recharge_time_DBLP_plus_SBLP(algos_db=[db_stf,dblp_sb_stf],    algos_sb=[sb_stf],  fig_title = "Shortest Tasks First (STF)",   file_name=file_path + "RT_STF.eps", legend_style=1)
    plot_recharge_time_DBLP_plus_SBLP(algos_db=[db_ltf,dblp_sb_ltf],    algos_sb=[sb_ltf],  fig_title = "Longest Tasks First (LTF)",    file_name=file_path + "RT_LTF.eps", legend_style=1)

def IT_comparison(file_path = "figures/new_figures/"):
    algo1 = {"algo": scheduling_DB_WT_optimized,    "label": "DB-WT",     "line":"b-"}
    algo2 = {"algo": scheduling_SB_WT_revised,      "label": "SB-WT",       "line":"r-"}
    plot_idle_time_plus_std([algo1, algo2], fig_title="", file_name = file_path + "Idle_WT.eps")

    algo1 = {"algo": scheduling_DB_TOF_optimized,   "label": "DB-TOF",    "line":"b-"}
    algo2 = {"algo": scheduling_SB_TOF_revised,     "label": "SB-TOF",      "line":"r-"}
    plot_idle_time_plus_std([algo1, algo2], fig_title="", file_name = file_path + "Idle_TOF.eps")

    algo1 = {"algo": scheduling_DB_LTF_optimized,   "label": "DB-LTF",    "line":"b-"}
    algo2 = {"algo": scheduling_SB_LTF_revised,     "label": "SB-LTF",      "line":"r-"}
    plot_idle_time_plus_std([algo1, algo2], fig_title="", file_name = file_path + "Idle_LTF.eps")

    algo1 = {"algo": scheduling_DB_STF_optimized,   "label": "DB-STF",    "line":"b-"}
    algo2 = {"algo": scheduling_SB_STF_revised,     "label": "SB-STF",      "line":"r-"}
    plot_idle_time_plus_std([algo1, algo2], fig_title="", file_name = file_path + "Idle_STF.eps")

def lp_analysis(file_path = 'figures/examples/'):
    plot_mean_altitude_per_drone_SMILP()
    plot_mean_altitude_per_sensors_SMILP()

    plot_mean_number_of_positions_SMILP()

    plot_mean_number_of_positions()

    plot_mean_time_per_position_SMILP_per_sensors()
    # plot_mean_time_per_position_SMILP()


def examples(file_path = 'figures/examples/'):
    tasks = [{"id": 'A',"drone":0, "ToF": 1, "start" : 3, "time":2, "color":"k"},
         {"id": 'B',"drone":1, "ToF": 2, "start" : 4, "time":2, "color":"k"}]
    plot_toy_schedule(tasks, 2 , x_lim=7, file_name = file_path + 'toy_example.eps', thickness=3)

# print("RT with Optimal")
# RT_with_optimal()

# print("RT comparison")
RT_comparison()

# print("RT comparison for DBLP and SBLP plus algos")
# DB_versus_SB()

# print("Solution time comparison")
# plot_solution_times_per_sensors(file_name='figures/new_figures/solution_time_DBLP_vs_SBLP.eps')

# print("Idle time comparison")
# IT_comparison()

# print("LP analysis")
# lp_analysis()


# print("Done")
# examples()

