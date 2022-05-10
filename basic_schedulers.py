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