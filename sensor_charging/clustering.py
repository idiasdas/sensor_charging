import numpy as np
# import matplotlib.pyplot as plt

def create_sensors(n_sensors):
    sensors = []
    for i in range(n_sensors):
        sensors.append(np.random.uniform(0,100,2)) # 2D random coordinates between 0 and 100
    return sensors

def clustering(n_sensors = 10, range = 30):
    sensors = create_sensors(n_sensors)
    clusters = []
    for i in range(n_sensors):
        clusters.append([sensors[i]])
        for j in range(n_sensors):
            if i != j:
                if np.linalg.norm(sensors[i]-sensors[j]) <= range:
                    clusters[i].append(sensors[j])
    return clusters