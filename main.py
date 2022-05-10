from simulation import *
from basic_schedulers import *
from genetic_scheduler import Genetic_Scheduler


gen = TaskGenerator(
	        cpus = [1, 8],    # [min, max]
	instructions = [50, 500], # [min, max]
	max          = 5000        # how many tasks to be generated before simulation stops
)

#Initialise nodes
# Node(id,ipt,cpus,memoryUsageCost,bwCost,cpuUsageCost)
nodes = [
	# Node(0, cpus=2, ipt=150, cost=3.0),
	# Node(1, cpus=4, ipt=100, cost=2.0),
	# Node(1, cpus=8, ipt=100, cost=2.0)
	Node(0,ipt=150,cpus=2,memoryUsageCost=3,bwCost=1,cpuUsageCost=2.5,memoryCapacity=1000),
	Node(1,ipt=100,cpus=4,memoryUsageCost=5,bwCost=2,cpuUsageCost=3,memoryCapacity=1500),
	Node(2,ipt=100,cpus=8,memoryUsageCost=4,bwCost=3,cpuUsageCost=4,memoryCapacity=2000)
]



# print("\nFIFO:")
# (tasks, stats) = Simulate(
# 	task_generator = gen,
# 	scheduler = FIFO_Schedule,
# 	nodes = nodes,
# 	max_concurrent_tasks = 8
# )
# PrettyStatsPrint(stats)


# print("\nSimple Scheduler:")
# (tasks, stats) = Simulate(
# 	task_generator = gen,
# 	scheduler = Handcraft_Scheduler,
# 	nodes = nodes,
# 	max_concurrent_tasks = 8
# )
# PrettyStatsPrint(stats)



print("\nGenetic:")
(tasks, stats) = Simulate(
	task_generator = gen,
	scheduler = Genetic_Scheduler,
	nodes = nodes,
	max_concurrent_tasks = 8
)
PrettyStatsPrint(stats)