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

		return self.progress > self.instrs


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
