from basic_functions import *
from scheduling_optimal import *


results_optimal = []
file = open("/Users/idiasdas/dev/sensor_charging/optimal_output/backup_optimal_results_GLOBECOM.txt", 'r')
data = file.readlines()
for line in data:
        results_optimal += [float(line.split()[-1])]
file.close()