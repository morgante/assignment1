import Queue as LibQueue

class Queue():
	def __init__(self):
		self.queue = LibQueue.Queue()

	def get(self):
		return self.queue.get()

	def add(self, item):
		return self.queue.put(item)

	def done(self):
		return self.queue.task_done()

	def peek(self):
		return 3;

	def wait(self):
		return self.queue.join()