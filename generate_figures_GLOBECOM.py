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
    plot_recharge_time_with_optimal()


