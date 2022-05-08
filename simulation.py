# Random number generator where state can be easily maintained for task generation
def LCG(seed, a=1664525, c=1013904223, m=2**32):
	return (a*seed + c) % m


class TaskGenerator:
	def __init__(self, cpus = [1, 8], instructions = [100, 10000]):
		self.cpus = cpus
		self.instrs = instructions
		self.state = 0
		self.count = 0

	def generate(self):
		self.state = LCG(self.state)
		c = ( self.state % (self.cpus[1] - self.cpus[0]) ) + self.cpus[0]
		self.state = LCG(self.state)
		i = ( self.state % (self.instrs[1] - self.instrs[0]) ) + self.instrs[0]
		id = self.count
		self.count = id + 1

		return Task(c, i)

	def reset(self):
		self.state = 0



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
		return "Task({}, {}, {}%)".format(self.cpus, self.instrs, int(self.progress/self.instrs*100))


class Node:
	def __init__(self, id, ipt, cpus, cost):
		self.id = id
		self.ipt = ipt
		self.cpus = cpus
		self.cost = cost

		self.operation = None

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

	def __repr__(self):
		if self.isProcessing():
			return "{}:\n  {}".format(self, self.operation)
		else:
			return str(self)

	def __str__(self):
		return "Node({}, {}, {})".format(self.id, self.cpus, self.ipt)




def Simulate(nodes, scheduler, task_generator):
	max_concurrent_tasks = 8
	max_tasks = 100
	tasks = []
	queue = []

	while True:
		while max_tasks > len(tasks) and len(queue) < max_concurrent_tasks:
			t = task_generator.generate()
			tasks.append(t)
			queue.append(t)

		# Determine which nodes are currently not procesing a Task
		freeNodes = []
		for n in nodes:
			if not n.isProcessing():
				freeNodes.append(n)

		if len(queue) == max_concurrent_tasks:
			print("Warn: No nodes can process available tasks")

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
