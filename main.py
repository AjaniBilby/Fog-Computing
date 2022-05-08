from simulation import *



def FIFO_Schedule(freeNodes, queue):
	# FIFO scheduling
	# assign the earliest task that meets the requirement of the node
	for (nID, n) in enumerate(freeNodes):
		for (qID, t) in enumerate(queue):
			if t.meets(n):
				n.assign(queue.pop(qID))

				freeNodes.pop(nID) # n now has a task and should not be double assigned
				break

	return

# def Handcraft_Scheduler():

gen = TaskGenerator()
tasks = [gen.generate() for _ in range (0, 10)]
tasks[2].latency = 1

tasks.sort(reverse=True)

for t in tasks:
	print(t)


# tasks = Simulate(
# 	nodes = [
# 		Node(0, cpus=2, ipt=150, cost=3.0),
# 		Node(1, cpus=4, ipt=100, cost=2.0),
# 		Node(1, cpus=8, ipt=100, cost=2.0)
# 	],
# 	scheduler=FIFO_Schedule,
# 	task_generator=TaskGenerator(
# 		        cpus = [1, 8],
# 		instructions = [1, 10]
# 	)
# )

# totalLatency      = sum([t.latency for t in tasks])
# totalProcessTime  = sum([t.processTime for t in tasks])
# totalCost         = sum([t.cost for t in tasks])

# print("Total")
# print("  Latency : {}".format(totalLatency))
# print("  Comput  : {}".format(totalProcessTime))
# print("  Cost    : {}".format(totalCost))

# print("Avg")
# print("  Latency : {}".format(totalLatency / len(tasks)))
# print("  Comput  : {}".format(totalProcessTime / len(tasks)))
# print("  Cost    : {}".format(totalCost / len(tasks)))