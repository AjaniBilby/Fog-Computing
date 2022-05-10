from simulation import *
from basic_schedulers import *
from genetic_scheduler import Genetic_Scheduler


gen = TaskGenerator(
	        cpus = [1, 8],    # [min, max]
	instructions = [50, 500], # [min, max]
	max          = 5000        # how many tasks to be generated before simulation stops
)
nodes = [
	Node(0, cpus=2, ipt=150, cost=3.0),
	Node(4, cpus=4, ipt=100, cost=2.0),
	Node(8, cpus=8, ipt=100, cost=2.0)
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