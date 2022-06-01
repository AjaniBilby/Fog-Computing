from simulation import *
from basic_schedulers import *
from genetic_scheduler import Genetic_Scheduler


gen = TaskGenerator(
	        cpus = [1, 8],       # [min, max]
	instructions = [50,   2000], # [min, max]
	      memory = [0.25,   16], # [min, max]
	   bandwidth = [0.001, 1.0], # [min, max]
	         max = 1000          # how many tasks to be generated before simulation stops
)

#Initialise nodes
nodes = [
	Node(0,ipt=100, cpus=1, memoryCapacity=1,  memoryUsageCost=0.08,  bwCost=0.016, cpuUsageCost=0.0001),
	Node(1,ipt=150, cpus=1, memoryCapacity=1,  memoryUsageCost=0.08,  bwCost=0.016, cpuUsageCost=0.0001),
	Node(2,ipt=100, cpus=2, memoryCapacity=1,  memoryUsageCost=0.05,  bwCost=0.008, cpuUsageCost=0.0006),
	Node(3,ipt=500, cpus=4, memoryCapacity=8,  memoryUsageCost=0.003, bwCost=0.005, cpuUsageCost=0.0004),
	Node(4,ipt=400, cpus=8, memoryCapacity=32, memoryUsageCost=0.001, bwCost=0.005, cpuUsageCost=0.0003),
]
concurrency = len(nodes)*1.5


print("\nFIFO:")
(tasks, stats) = Simulate(
	task_generator = gen,
	scheduler = FIFO_Schedule,
	nodes = nodes,
	max_concurrent_tasks = concurrency
)
PrettyStatsPrint(stats)


print("\nSimple Scheduler:")
(tasks, stats) = Simulate(
	task_generator = gen,
	scheduler = Handcraft_Scheduler,
	nodes = nodes,
	max_concurrent_tasks = concurrency
)
PrettyStatsPrint(stats)



print("\nGenetic:")
(tasks, stats) = Simulate(
	task_generator = gen,
	scheduler = Genetic_Scheduler,
	nodes = nodes,
	max_concurrent_tasks = concurrency
)
PrettyStatsPrint(stats)