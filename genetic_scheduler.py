import random

MUTATION_RATE = 0.1
BATCH_SIZE = 50
GENERATIONS = 10

def Genetic_Scheduler(freeNodes, queue):
	# Estimate the cost of a given configuration
	# config: list mapping [ nodes → queue tasks ]
	best = []
	bestCost = None


	def init():
		opts = [t for t in queue]
		# Ensure the queue is at least nodes long
		for _ in range(len(freeNodes)-len(queue)):
			opts.append(None)

		for _ in freeNodes:
			best.append(opts.pop(random.randint(0, len(opts)-1)))

	def Mutate(parent):
		opts = [i for i in range(0, len(queue))]

		child = []
		for val in best:
			if len(opts) == 0:
				break

			if random.random() > MUTATION_RATE:
				child.append(None) # randomness will be fulfilled one inherited traits are assigned
			else:
				# print(val, opts)
				child.append(opts.pop(parent.index(val)))

		# There maybe more nodes available then tasks near the end of the simulation
		for (i, val) in enumerate(child):
			if len(opts) == 0:
				break

			if val is None:
				child[i] = opts.pop(random.randint(0, len(opts)-1))

		return child

	for b in range(GENERATIONS):
		batch = []
		for g in range(BATCH_SIZE):
			batch.append(Mutate(best))

		for child in batch:
			cost = 0
			for (nID, qID) in enumerate(child):
				if qID is None:
					continue
				else:
					cost = cost + freeNodes[nID].estimate_cost(queue[qID])

			if bestCost is None or cost < bestCost:
				bestCost = cost
				best = child


	# Assigned the tasks to the nodes
	for (nID, qID) in enumerate(best):
		freeNodes[nID].assign( queue[qID] )

	return