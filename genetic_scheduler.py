import enum
import random

MUTATION_RATE = 0.1
BATCH_SIZE = 100
GENERATIONS = 20

def Genetic_Scheduler(freeNodes, queue):
	# Estimate the cost of a given configuration
	# config: list mapping [ nodes → queue tasks ]
	best = []
	bestCost = None

	# Start off with an inital valid genom
	# Otherwise the algorithm was sometimes getting stuck within an invalid starting point
	def init():
		offset = 0
		for n in freeNodes:
			if offset >= len(queue):
				best.append(None)
			elif queue[offset].meets(n):
				best.append(offset)
				offset = offset + 1
			else:
				best.append(None)
	init()

	# Check the geno isn't trying to assign tasks to nodes that can't handle it
	def isValidAssignments(geno):
		for (nID, qID) in enumerate(geno):
			if qID is not None:
				if not queue[qID].meets(freeNodes[nID]):
					return False

		return True

	def Mutate(parent):
		opts = [i for i in range(0, len(queue))]

		child = []
		for val in parent:
			if len(opts) == 0:
				break

			if val is None or random.random() > MUTATION_RATE:
				child.append(None) # randomness will be fulfilled one inherited traits are assigned
			else:
				child.append(opts.pop(opts.index(val)))

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
			if not isValidAssignments(child):
				continue

			cost = 0
			for (nID, qID) in enumerate(child):
				if qID is None:
					continue
				else:
					cost = cost + freeNodes[nID].estimateCost(queue[qID])

			if bestCost is None or cost < bestCost:
				bestCost = cost
				best = child


	# Assigned the tasks to the nodes
	# print("Final {}".format(best))
	for (nID, qID) in enumerate(best):
		if qID is None:
			continue
		freeNodes[nID].assign( queue[qID] )

	return