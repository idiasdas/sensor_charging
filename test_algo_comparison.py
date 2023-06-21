from basic_functions import *
from plot_schedule import *
from plot_total_recharge_time import *
from scheduling_wait_time import *
from scheduling_longest_tasks_first import *
from scheduling_ToF import *
from scheduling_shortest_tasks_first import *
from scheduling_nodrone_wait_time import *
from scheduling_nodrone_longest_tasks_first import *
from scheduling_nodrone_shortest_tasks_first import *
from scheduling_nodrone_ToF import *

def algo_comparison(algo1, algo2, p = 5, drone_speed = 0.5, i_max = 50, drones = range(3,11), sensors = [5,10,15,20,30,40,50],drone_based = True, input_path = "inputs/", plot_first_example = False):
    """Compares two algorithms on a set of inputs. Returns True if the two algorithms give the same results, False otherwise.

    Args:
        algo1 (function): Scheduling function 1. 
        algo2 (function): Scheduling function 2.
        p (int, optional): Number of positions. Defaults to 5.
        drone_speed (float, optional): Drones' speed. Defaults to 0.5 which is low but helps visualize problems thanks to a higher time of flight.
        i_max (int, optional): Amount of instances for each parameter combination. Defaults to 50.
        drones (list, optional): List with amount of drones to be considered at each iteration. Defaults to range(3,11).
        sensors (list, optional): List with the amount of sensors to charge at each iteration. Defaults to [5,10,15,20,30,40,50].
        drone_based (bool, optional): If the input is drone_based or not. Defaults to True.
        input_path (str, optional): Path to input directory. Defaults to "inputs/" (Drone-based).
        plot_first_example (bool, optional): If True, plots the first schedule where the algorithms are different. Defaults to False.

    Returns:
        bool: True if the algorithms are equivalent, False otherwise.
    """
    if not drone_based:
        input_path = "milp/backup_results_17feb_timelimit1200/output_simplified/"
    eps = 0.0001
    is_equivalent = True
    count_diff = 0
    total_diff = 0
    for s in sensors:
        for d in range(3,11):
            for i in range(0,i_max):
                if drone_based:
                    file = input_path + "d"+str(d)+"_s"+str(s)+"_p"+str(p)+"/" + str(i) + ".txt"
                else:
                    file = input_path+"s"+str(s)+"_p"+str(p)+"/" + str(i) + ".txt"
                
                tasks = get_tasks(file)
                scheduling1,time1 = algo1(tasks, d, drone_speed)

                tasks = get_tasks(file)
                scheduling2,time2 = algo2(tasks, d, drone_speed)

                if abs(time1 - time2) > eps:
                    count_diff += 1
                    total_diff += (time1 - time2)
                    if plot_first_example:
                        print("\t- Different time for d = " + str(d) + ", s = " + str(s) + ", i = " + str(i))
                        plot_schedule(scheduling1, d, time1, file_name = "tests_outputs/test_equivalence_" + algo1.__name__ +".eps",save=True)
                        plot_schedule(scheduling2, d, time2, file_name = "tests_outputs/test_equivalence_" + algo2.__name__ +".eps",save=True)
                        print("\t-Saved different example as tests_outputs/test_equivalence_" + algo1.__name__ +".eps and tests_outputs/test_equivalence_" + algo2.__name__ +".eps")
                        print("\t-Stopped equivalence test.")
                        plot_first_example = False
                    is_equivalent = False
                if not (verify_schedule(scheduling1) and verify_schedule(scheduling2)): #If any of the schedules is not valid
                    print("\t- Invalid schedule for d = " + str(d) + ", s = " + str(s) + ", i = " + str(i))

    if(count_diff > 0):
        print("\t- Different time for " + str(count_diff) + " out of " + str(i_max*len(sensors)*len(drones)) + " inputs.")
        print("\t- Average difference: " + str(total_diff/count_diff))
    
    return is_equivalent

def test_equivalence(algo1, algo2, file_name,plot_recharge_time = True, plot_first_example=False, drone_based = True):
    """Compares two algorithms, if they are not equivalent plots a figure with the total recharge time for each algorithm.

    Args:
        algo1 (dict): Scheduling function 1.
        algo2 (dict): Scheduling function 2.
        file_name (str): path + name for output figure if needed.
        plot_recharge_time (bool, optional): If True plots the total recharge time if agorithms are different. Defaults to True.
        plot_first_example (bool, optional): If True plots the schedule of the first example where the algorithms are different. Defaults to False.
        drone_based (bool, optional): If True, runs the algorithms on the DBLP output, else uses SBLP as input. Defaults to True.
    """    
    print("* Testing "+algo1["algo"].__name__+" and " + algo2["algo"].__name__ + " for equivalence.")
    if algo_comparison(algo1["algo"], algo2["algo"],drone_based=drone_based, plot_first_example=plot_first_example):
        print("* (SUCCESS)")
    else:
        if(plot_recharge_time):
            print("* Plotting difference between algorithms over all inputs")
            if not drone_based:
                plot_total_recharge_time_SMILP_DATA([algo1,algo2], file_name=file_name)
            else:
                plot_total_recharge_time([algo1,algo2], file_name=file_name, legend_outside_figure=False)
        print("* (FAIL)")
    print("---------------------------------------------------------------")

def test_all():
    """Compares the optmized/revised versions with the algorithms old versions."""
    # -----------------------------------------------------------------------------------------------------
    # Old drone-based versions vs optimzed versions
    # -----------------------------------------------------------------------------------------------------
    algo1 = {"algo":scheduling_DB_WT, "label":"DB-WT","line":"b-"}
    algo2 = {"algo":scheduling_DB_WT_optimized, "label":"DB-WT optimized","line":"r-"}
    test_equivalence(algo1, algo2, "tests_outputs/test_eq_DB_WT.eps")

    algo1 = {"algo":scheduling_DB_TOF, "label":"DB-TOF","line":"b-"}
    algo2 = {"algo":scheduling_DB_TOF_optimized, "label":"DB-TOF optimized","line":"r-"}
    test_equivalence(algo1, algo2, "tests_outputs/test_eq_DB_TOF.eps")

    algo1 = {"algo":scheduling_DB_LTF, "label":"DB-LTF","line":"b-"}
    algo2 = {"algo":scheduling_DB_LTF_optimized,"label":"DB-LTF optimized","line":"r-"}
    test_equivalence(algo1, algo2, "tests_outputs/test_eq_DB_LTF.eps")

    algo1 = {"algo":scheduling_DB_STF, "label":"DB-STF","line":"b-"}
    algo2 = {"algo":scheduling_DB_STF_optimized, "label":"DB-STF optimized","line":"r-"}
    test_equivalence(algo1, algo2, "tests_outputs/test_eq_DB_STF.eps")
    # -----------------------------------------------------------------------------------------------------
    # Old sensor based versions vs revised versions over DBLP inputs and SBLP inputs
    # -----------------------------------------------------------------------------------------------------
    algo1 = {"algo":scheduling_SB_WT, "label":"SB-WT","line":"b-"}
    algo2 = {"algo":scheduling_SB_WT_revised, "label":"SB-WT revised","line":"r-"}
    test_equivalence(algo1, algo2, "tests_outputs/test_eq_SB_WT(DBLP).eps")
    test_equivalence(algo1, algo2, "tests_outputs/test_eq_SB_WT(SBLP).eps", drone_based=False)

    algo1 = {"algo":scheduling_SB_LTF, "label":"SB-LTF","line":"b-"}
    algo2 = {"algo":scheduling_SB_LTF_revised, "label":"SB-LTF revised","line":"r-"}
    test_equivalence(algo1, algo2, "tests_outputs/test_eq_SB_LTF(DBLP).eps")
    test_equivalence(algo1, algo2, "tests_outputs/test_eq_SB_LTF(SBLP).eps", drone_based=False)

    algo1 = {"algo":scheduling_SB_STF, "label":"SB-STF","line":"b-"}
    algo2 = {"algo":scheduling_SB_STF_revised, "label":"SB-STF revised","line":"r-"}
    test_equivalence(algo1, algo2, "tests_outputs/test_eq_SB_STF(DBLP).eps")
    test_equivalence(algo1, algo2, "tests_outputs/test_eq_SB_STF(SBLP).eps", drone_based=False)

    algo1 = {"algo":scheduling_SB_TOF, "label":"SB-TOF","line":"b-"}
    algo2 = {"algo":scheduling_SB_TOF_revised, "label":"SB-TOF revised","line":"r-"}
    test_equivalence(algo1, algo2, "tests_outputs/test_eq_SB_TOF(DBLP).eps")
    test_equivalence(algo1, algo2, "tests_outputs/test_eq_SB_TOF(SBLP).eps", drone_based=False)


test_all()