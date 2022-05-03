from shared import *


def Simulate(nodes, scheduler):
	# TODO
	# Move the creation of tasks to a generator parsed as an argument
	# Start off with a large set of tasks at the beginning
	# Then add a new task to the queue every X tick
	tasks = [
		Task(cpus=4, instructions=100),
		Task(cpus=2, instructions=100),
		Task(cpus=2, instructions=200)
	]

	queue = [x for x in tasks]

	while True:
		# Determine which nodes are currently not procesing a Task
		freeNodes = []
		for n in nodes:
			if not n.isProcessing():
				freeNodes.append(n)

		# If all nodes are available, and there are no tasks in the queue
		# Then all tasks have been completed
		if len(freeNodes) == len(nodes) and len(queue) == 0:
			break

		scheduler(freeNodes, queue)

		# Step forward the simulation
		for n in nodes:
			n.tick()

		# Add latency to the still awaiting tasks
		for t in queue:
			t.wait()

	return tasks



def FIFO_Schedule(freeNodes, queue):
	# FIFO scheduling
		# assign the earliest task that meets the requirement of the node
		for (nID, n) in enumerate(freeNodes):
			if len(queue) > 0:
				for (qID, t) in enumerate(queue):
					if t.meets(n):
						n.assign(queue.pop(qID))
						print("Assigned node {} task {} from the queue".format(nID, qID))



tasks = Simulate(
	nodes = [
		Node(cpus=2, ipt=10, cost=3.0),
		Node(cpus=4, ipt=10, cost=2.0)
	],
	scheduler=FIFO_Schedule
)

totalLatency      = sum([t.latency for t in tasks])
totalProcessTime  = sum([t.processTime for t in tasks])
totalCost         = sum([t.cost for t in tasks])

print("Total")
print("  Latency : {}".format(totalLatency))
print("  Comput  : {}".format(totalProcessTime))
print("  Cost    : {}".format(totalCost))

print("Avg")
print("  Latency : {}".format(totalLatency / len(tasks)))
print("  Comput  : {}".format(totalProcessTime / len(tasks)))
print("  Cost    : {}".format(totalCost / len(tasks)))