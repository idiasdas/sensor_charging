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
    plot_recharge_time_with_optimal_revised(db_old_algos, file_name = file_path + "RT_DBLP_OLD-DB-algos_OPTIMAL.eps", fig_title="OLD DB Algorithms (870)")

    # DB-LP inputs + optimized DB algorithms + optimal from GLOBECOM backup
    plot_recharge_time_with_optimal_revised(db_optimimzed_algos, file_name = file_path + "RT_DBLP_Optimized-DB-algos_OPTIMAL.eps", fig_title="")

    # DB-LP inputs + revised SB algorithms + optimal from GLOBECOM backup
    plot_recharge_time_with_optimal_revised(sb_revised_algos_plusTSP, file_name = file_path + "RT_DBLP_Revised_SB_OPTIMAL.eps", fig_title="")


def RT_comparison(file_path = "figures/new_figures/"):
    db_optimimzed_algos_plusTSP = [
        {"algo": scheduling_DB_TOF_optimized,    "label": "TOF",        "line": "y-"},
        {"algo": scheduling_DB_WT_optimized,     "label": "WT",         "line": "g-"},
        {"algo": scheduling_DB_STF_optimized,    "label": "STF",        "line": "k-"},
        {"algo": scheduling_DB_LTF_optimized,    "label": "LTF",        "line": "b-"},
        {"algo": scheduling_TSP,                 "label": "TSP",        "line": "r-"}]
    
    sb_revised_algos_plusTSP = [
        {"algo": scheduling_SB_TOF_revised,      "label": "TOF",        "line": "y-"},
        {"algo": scheduling_SB_WT_revised,       "label": "WT",         "line": "g-"},
        {"algo": scheduling_SB_STF_revised,      "label": "STF",        "line": "k-"},
        {"algo": scheduling_SB_LTF_revised,      "label": "LTF",        "line": "b-"},
        {"algo": scheduling_TSP,                 "label": "TSP",        "line": "r-"}]
    
    sb_revised_algos = [
        {"algo": scheduling_SB_TOF_revised,      "label": "TOF",        "line": "y-"},
        {"algo": scheduling_SB_WT_revised,       "label": "WT",         "line": "g-"},
        {"algo": scheduling_SB_STF_revised,      "label": "STF",        "line": "k-"},
        {"algo": scheduling_SB_LTF_revised,      "label": "LTF",        "line": "b-"}]
    
    # DB-LP inputs + DB algorithms + TSP
    plot_total_recharge_time(algos=db_optimimzed_algos_plusTSP, file_name = file_path + "RT_DBLP_DB_ALGOS.eps", fig_title="DB-LP + DB Algorithms", legend_style=3)
    
    # DB-LP inputs + SB algorithms + TSP
    plot_total_recharge_time(algos=sb_revised_algos_plusTSP, file_name = file_path + "RT_DBLP_SB_ALGOS.eps", fig_title="DB-LP + DB Algorithms", legend_style=0)
    
    # SB-LP inputs + SB algorithms
    plot_total_recharge_time(algos=sb_revised_algos,input_style = 1, file_name = file_path + "RT_SBLP_SB_ALGOS.eps", fig_title="SB-LP + SB Algorithms", legend_style=0)

def DB_versus_SB(file_path = "figures/new_figures/"):
    db_tof = {"algo": scheduling_DB_TOF_optimized,      "label": "DB-LP + DB-Scheduling",      "line": "r-"}
    db_wt  = {"algo": scheduling_DB_WT_optimized,       "label": "DB-LP + DB-Scheduling",      "line": "r-"}
    db_stf = {"algo": scheduling_DB_STF_optimized,      "label": "DB-LP + DB-Scheduling",      "line": "r-"}
    db_ltf = {"algo": scheduling_DB_LTF_optimized,      "label": "DB-LP + DB-Scheduling",      "line": "r-"}

    
    dblp_sb_tof = {"algo": scheduling_SB_TOF_revised,   "label": "DB-LP + SB-Scheduling",      "line": "g-"}
    dblp_sb_wt  = {"algo": scheduling_SB_WT_revised,    "label": "DB-LP + SB-Scheduling",      "line": "g-"}
    dblp_sb_stf = {"algo": scheduling_SB_STF_revised,   "label": "DB-LP + SB-Scheduling",      "line": "g-"}
    dblp_sb_ltf = {"algo": scheduling_SB_LTF_revised,   "label": "DB-LP + SB-Scheduling",      "line": "g-"}

    sb_tof = {"algo": scheduling_SB_TOF_revised,        "label": "SB-LP + SB-Scheduling",      "line": "b-"}
    sb_wt  = {"algo": scheduling_SB_WT_revised,         "label": "SB-LP + SB-Scheduling",      "line": "b-"}
    sb_stf = {"algo": scheduling_SB_STF_revised,        "label": "SB-LP + SB-Scheduling",      "line": "b-"}
    sb_ltf = {"algo": scheduling_SB_LTF_revised,        "label": "SB-LP + SB-Scheduling",      "line": "b-"}

    plot_recharge_time_DBLP_plus_SBLP(algos_db=[db_tof,dblp_sb_tof],    algos_sb=[sb_tof],  fig_title = "Time of Filght (TOF)",         file_name=file_path + "RT_TOF.eps", legend_style=3)
    plot_recharge_time_DBLP_plus_SBLP(algos_db=[db_wt,dblp_sb_wt],      algos_sb=[sb_wt],   fig_title = "Wait Time (WT)",               file_name=file_path + "RT_WT.eps",  legend_style=0)
    plot_recharge_time_DBLP_plus_SBLP(algos_db=[db_stf,dblp_sb_stf],    algos_sb=[sb_stf],  fig_title = "Shortest Tasks First (STF)",   file_name=file_path + "RT_STF.eps", legend_style=0)
    plot_recharge_time_DBLP_plus_SBLP(algos_db=[db_ltf,dblp_sb_ltf],    algos_sb=[sb_ltf],  fig_title = "Longest Tasks First (LTF)",    file_name=file_path + "RT_LTF.eps", legend_style=0)


# RT_with_optimal()
# RT_comparison()
# DB_versus_SB()
plot_solution_times_per_sensors(file_name='figures/new_figures/solution_time_DBLP_vs_SBLP.eps')
