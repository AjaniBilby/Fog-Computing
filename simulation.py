# Random number generator where state can be easily maintained for task generation
def LCG(seed, a=1664525, c=1013904223, m=2**32):
	return (a*seed + c) % m


class TaskGenerator:
	def __init__(self, cpus = [1, 8], instructions = [100, 10000], max = 1000):
		self.cpus   = cpus
		self.instrs = instructions
		self.max    = max
		self.state  = 0
		self.count  = 0

	def generate(self):
		if self.count >= self.max:
			return None

		self.state = LCG(self.state)
		c = ( self.state % (self.cpus[1] - self.cpus[0]) ) + self.cpus[0]
		self.state = LCG(self.state)
		i = ( self.state % (self.instrs[1] - self.instrs[0]) ) + self.instrs[0]
		id = self.count
		self.count = id + 1

		return Task(c, i)

	def reset(self):
		self.state = 0
		self.count = 0



class Task:
	def __init__(self, cpus, instructions):
		self.cpus = cpus
		self.instrs = instructions
		self.progress = 0

		self.pID = 0
		self.latency = 0
		self.processTime = 0
		self.cost = 0

	def meets(self, node):
		return node.cpus >= self.cpus

	def wait(self):
		self.latency = self.latency + 1

	def tick(self, ipt, cost):
		self.processTime = self.processTime + 1
		self.progress = self.progress + ipt
		self.cost = self.cost + cost

		return self.progress >= self.instrs

	def __repr__(self):
		return "Task({}, {})".format(self.cpus, self.instrs)

	def __str__(self):
		return "Task(cpus: {}, latency: {}ms, instr: {}, {}%)".format(self.cpus, self.latency, self.instrs, int(self.progress/self.instrs*100))


class Node:
	def __init__(self, id, ipt, cpus, cost):
		self.id = id
		self.ipt = ipt
		self.cpus = cpus
		self.cost = cost

		self.operation = None
		self.idle = 0

	def costOfExecution(self, task):
		return task.instrs/self.ipt * self.cost

	def isProcessing(self):
		return self.operation != None

	def assign(self, task):
		if self.isProcessing():
			raise Exception("Node Already processing")

		self.processing = task.instrs
		self.operation = task
		task.pID = self.id

	def tick(self):
		if self.isProcessing():
			done = self.operation.tick(self.ipt, self.cost)

			if done:
				self.operation = None
		else:
			self.idle = self.idle + 1

	def estimate_cost(self, task):
		return task.instr/self.ipt * self.cost

	def reset(self):
		self.operation = None
		self.idle = 0

	def __repr__(self):
		if self.isProcessing():
			return "{}:\n  {}".format(self, self.operation)
		else:
			return str(self)

	def __str__(self):
		return "Node({}, {}, {})".format(self.id, self.cpus, self.ipt)




def Simulate(nodes, scheduler, task_generator, max_concurrent_tasks=8, experiment_name="default"):
	tasks = []
	queue = []
	ticks = 0

	# Reset the internal states
	task_generator.reset()
	for n in nodes:
		n.reset()

	max_cpus = max([n.cpus for n in nodes])

	# TODO
	# Init the CSV headers
	# csv.open("{}.csv".format(experiment_name))
	# for c in range(1, max_cpus):
	# 	csv.write("Q{},".format(c))
	# for n in range(1, len(nodes)):
	# 	csv.write("N{},".format(n))
	# csv.new_line()

	while True:
		while len(queue) < max_concurrent_tasks:
			t = task_generator.generate()
			if t is None:
				break

			tasks.append(t)
			queue.append(t)

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

		if len(queue) == max_concurrent_tasks and len(freeNodes) == len(nodes):
			print("Scheduled tasks that no node on this network can compute")
			exit(1)

		# Step forward the simulation
		for n in nodes:
			n.tick()

		# Add latency to the still awaiting tasks
		for t in queue:
			t.wait()


		# TODO
		# Write row to CSV
		# num tasks in queue per CPU division
		# Y/N for each node's processing status
		# i.e
		# C1, C4, C8, N1, N2, N3
		#  3,  5,  1, Y,  N,  Y
		#
		# tally = []
		# for i in range(0, max_cpus-1):
		# 	tally[i] = 0
		# for q in queue:
		# 	tally[q.cpus-1] = tally[q.cpus-1] + 1
		#
		# for t in tally:
		# 	csv.write("{},".format(t))
		# for n in nodes:
		# 	csv.write("{},".format(n.isProcessing()))
		# csv.new_line()

		ticks = ticks + 1

	stats = {
		'total': {
			'latency': sum([t.latency for t in tasks]),
			'processTime': sum([t.processTime for t in tasks]),
			'cost': sum([t.cost for t in tasks]),
			'idle': sum([n.idle for n in nodes]),
			'tick': ticks
		},
		'avg': {}
	}

	stats['avg']['latency'] = stats['total']['latency'] / len(tasks)
	stats['avg']['processTime'] = stats['total']['processTime'] / len(tasks)
	stats['avg']['cost'] = stats['total']['cost'] / len(tasks)
	stats['avg']['idle'] = stats['total']['idle'] / len(nodes)

	# TODO
	# Close the CSV file
	# csv.close()

	return (tasks, stats)
