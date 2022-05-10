from simulation import *


def FIFO_Schedule(freeNodes, queue):
	# FIFO scheduling
	# assign the earliest task that meets the requirement of the node
	for (nID, n) in enumerate(freeNodes):
		for (qID, t) in enumerate(queue):
			if t.meets(n):
				n.assign(queue.pop(qID))

				freeNodes.pop(nID) # n now has item1 task and should not be double assigned
				break

	return

def Handcraft_Scheduler(freeNodes, queue):
	queue.sort(key=lambda x: (x.cpus, x.latency), reverse=True)
	# FIFO by priotieses scheduling higher CPU tasks first
	# Hence a higher CPU node won't get scheduled a lower CPU task when a higher CPU task is available

	for (qID, t) in enumerate(queue):
		for (nID, n) in enumerate(freeNodes):
			if t.meets(n):
				n.assign(queue.pop(qID))

				freeNodes.pop(nID) # n now has item1 task and should not be double assigned
				break

	return

def Genetic_Scheduler(freeNodes, queue):
	# Estimate the cost of a given configuration
	# config: list mapping [ nodes → queue tasks ]
	def Configuration_Cost(config):
		cost = 0
		for (nID, n) in enumerate(freeNodes):
			cost = cost + n.estimate_cost(queue[config[nID]])

		return cost


	# TODO implement

	return


def PrettyStatsPrint(stats):
	print("Total")
	print("  Latency : {}".format(stats['total']['latency']))
	print("  Comput  : {}".format(stats['total']['processTime']))
	print("  Cost    : {}".format(stats['total']['cost']))
	print("  Ticks   : {}".format(stats['total']['tick']))
	print("  Idle    : {}".format(stats['total']['idle']))

	print("Avg")
	print("  Latency : {}".format(stats['avg']['latency']))
	print("  Comput  : {}".format(stats['avg']['processTime']))
	print("  Cost    : {}".format(stats['avg']['cost']))
	print("  Idle    : {}".format(stats['avg']['idle']))

# Initialise TaskGenerator
gen = TaskGenerator(
	        cpus = [1, 8],    # [min, max]
	instructions = [50, 500], # [min, max]
	max          = 500        # how many tasks to be generated before simulation stops
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



print("\nFIFO:")
(tasks, stats) = Simulate(
	task_generator = gen,
	scheduler = FIFO_Schedule,
	nodes = nodes
)
PrettyStatsPrint(stats)


print("\nSimple Scheduler:")
(tasks, stats) = Simulate(
	task_generator = gen,
	scheduler = Handcraft_Scheduler,
	nodes = nodes
)
PrettyStatsPrint(stats)



# print("\nGenetic:")
# (tasks, stats) = Simulate(
# 	task_generator = gen,
# 	scheduler = Genetic_Scheduler,
# 	nodes = nodes
# )
# PrettyStatsPrint(stats)