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

def generate_all_figures(file_path = "figures/"):
    """Plots all the figures for the journal version including the ones for the GLOBECOM paper

    Args:
        file_path (str, optional): Path to save the figures. Defaults to "figures/".
    """    
    db_old_algos = [
        {"algo":scheduling_DB_TOF,              "label":"DB-TOF",       "line":"y-"},
        {"algo":scheduling_DB_WT,               "label":"DB-WT",        "line":"g-"},
        {"algo":scheduling_DB_STF,              "label":"DB-STF",       "line":"k-"},
        {"algo":scheduling_DB_LTF,              "label":"DB-LTF",       "line":"b-"},
        {"algo":scheduling_TSP,                 "label":"TSP",          "line":"r-"}]
    
    db_optimimzed_algos = [
        {"algo":scheduling_DB_TOF_optimized,    "label":"DB-TOF",       "line":"y-"},
        {"algo":scheduling_DB_WT_optimized,     "label":"DB-WT",        "line":"g-"},
        {"algo":scheduling_DB_STF_optimized,    "label":"DB-STF",       "line":"k-"},
        {"algo":scheduling_DB_LTF_optimized,    "label":"DB-LTF",       "line":"b-"},
        {"algo":scheduling_TSP,                 "label":"TSP",          "line":"r-"}]
    
    sb_revised_algos_plusTSP = [
        {"algo":scheduling_SB_TOF_revised,      "label":"SB-TOF",       "line":"y-"},
        {"algo":scheduling_SB_WT_revised,       "label":"SB-WT",        "line":"g-"},
        {"algo":scheduling_SB_STF_revised,      "label":"SB-STF",       "line":"k-"},
        {"algo":scheduling_SB_LTF_revised,      "label":"SB-LTF",       "line":"b-"},
        {"algo":scheduling_TSP,                 "label":"TSP",          "line":"r-"}]
    
    sb_revised_algos = [
        {"algo":scheduling_SB_TOF_revised,      "label":"SB-TOF",       "line":"y-"},
        {"algo":scheduling_SB_WT_revised,       "label":"SB-WT",        "line":"g-"},
        {"algo":scheduling_SB_STF_revised,      "label":"SB-STF",       "line":"k-"},
        {"algo":scheduling_SB_LTF_revised,      "label":"SB-LTF",       "line":"b-"}]
    
    # Make figure using DB-LP output for old DB algorithms plus optimal with output from GLOBECOM backup
    plot_recharge_time_with_optimal_revised(db_old_algos, file_name = file_path + "RT_DBLP_OLD-DB-algos_OPTIMAL.eps", fig_title="OLD DB Algorithms (870)")

    # Make figure using DB-LP output for optimized DB algorithms plus optimal with output from GLOBECOM backup
    plot_recharge_time_with_optimal_revised(db_optimimzed_algos, file_name = file_path + "RT_DBLP_Optimized-DB-algos_OPTIMAL.eps", fig_title="Optimized DB Algorithms (870)")

    # Make figure using DB-LP output for old DB algorithms for all instances
    plot_total_recharge_time(algos=db_old_algos, file_name = file_path + "RT_DBLP_OLD-DB-algos.eps", fig_title="OLD DB Algorithms (2800)")

    # Make figure using DB-LP output for optimized DB algorithms for all instances
    plot_total_recharge_time(algos=db_optimimzed_algos, file_name = file_path + "RT_DBLP_Optimized-DB-algos.eps", fig_title="Optimized DB Algorithms (2800)")

    # Make figure using DB-LP output for revised SB algorithms plus TSP
    plot_total_recharge_time(algos=sb_revised_algos_plusTSP, file_name  = file_path + "RT_DBLP_SBalgos_plusTSP.eps", fig_title="DB-LP + revised SB Algorithms + TSP (2800)")

    # Make figure using SB-LP output for revised SB algorithms
    sensor_based_input_path = "milp/backup_results_17feb_timelimit1200/output_simplified/"
    plot_total_recharge_time(algos=sb_revised_algos,input_path=sensor_based_input_path,input_style=1, file_name = file_path + "RT_SBLP_SBalgos.eps", fig_title="SB-LP + revised SB Algorithms (2800)") 

def RT_comparison(file_path = "figures/new_figures/"):
    db_optimimzed_algos = [
        {"algo":scheduling_DB_TOF_optimized,    "label":"TOF",  "line":"y-"},
        {"algo":scheduling_DB_WT_optimized,     "label":"WT",   "line":"g-"},
        {"algo":scheduling_DB_STF_optimized,    "label":"STF",  "line":"k-"},
        {"algo":scheduling_DB_LTF_optimized,    "label":"LTF",  "line":"b-"},
        {"algo":scheduling_TSP,                 "label":"TSP",  "line":"r-"}]
    
    sb_revised_algos_plusTSP = [
        {"algo":scheduling_SB_TOF_revised,      "label":"TOF",  "line":"y-"},
        {"algo":scheduling_SB_WT_revised,       "label":"WT",   "line":"g-"},
        {"algo":scheduling_SB_STF_revised,      "label":"STF",  "line":"k-"},
        {"algo":scheduling_SB_LTF_revised,      "label":"LTF",  "line":"b-"},
        {"algo":scheduling_TSP,                 "label":"TSP",  "line":"r-"}]
    
    sb_revised_algos = [
        {"algo":scheduling_SB_TOF_revised,      "label":"TOF",  "line":"y-"},
        {"algo":scheduling_SB_WT_revised,       "label":"WT",   "line":"g-"},
        {"algo":scheduling_SB_STF_revised,      "label":"STF",  "line":"k-"},
        {"algo":scheduling_SB_LTF_revised,      "label":"LTF",  "line":"b-"}]
    

    plot_total_recharge_time(algos=db_optimimzed_algos, file_name = file_path + "DBLP_DB_ALGOS.eps", fig_title="DB-LP + DB Algorithms", legend_style=3)
    
    plot_total_recharge_time(algos=sb_revised_algos_plusTSP, file_name = file_path + "DBLP_SB_ALGOS.eps", fig_title="DB-LP + DB Algorithms", legend_style=0)
    
    plot_total_recharge_time(algos=sb_revised_algos,input_style = 1, file_name = file_path + "SBLP_SB_ALGOS.eps", fig_title="SB-LP + SB Algorithms", legend_style=0)
    
# generate_all_figures()
RT_comparison(file_path="figures/new_figures/")
