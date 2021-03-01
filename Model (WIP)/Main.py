from World import WorldModel
from time import time

# Run a simulation of the ABM with parameters as follows
num_agents = 1000
num_traps = 5
num_deer = 50
width = 808
height = 672
mapfile = "MapData/AllXY.csv"

times = []

for i in range(15):
    start = time()
    sim = WorldModel(num_agents, num_traps, num_deer, width, height, mapfile)
    for i in range(1):
        sim.step()
    end = time()
    times.append(end - start)
print("Average time elapsed: " + str(sum(times)/len(times)))
print("This gives an average time per midge of " + str(sum(times)/(len(times)*num_agents)) + " seconds")