import Queue as LibQueue
from abc import ABCMeta, abstractmethod
import time

class Queue(object):
	def __init__(self):
		self.queue = LibQueue.Queue()

	def get(self):
		return self.queue.get()

	def add(self, item):
		return self.queue.put(item)

	def done(self):
		return self.queue.task_done()

	def peek(self):
		return self.queue.qsize()

	def wait(self):
		return self.queue.join()


class Station(object):
    __metaclass__ = ABCMeta
    type = 'station type'

    def __init__(self, reception):
		self.queue = Queue()

    def peek(self):
		self.queue.peek()

    def add(self, customer):
		print "Putting %(customer)s in %(name)s queue at %(time)s" % \
			{"customer":customer.emirates_id.first_name, "name": self.type, "time": time.time()}
		
		self.queue.add(customer)