import Queue as LibQueue
from abc import ABCMeta, abstractmethod
import time

queues = []

# This is the queuing controller/interface, additional strategies can implement it
class Queue(object):
	def __init__(self, prefix):
		self.queue = LibQueue.Queue()
		self.numbers = {}
		self.prefix = prefix
		self.last_number = 0

		queues.append(self)

	def get(self):
		customer = self.queue.get()

		id = customer.emirates_id.id_number

		# Check that their number is still valid
		if (id in self.numbers):
			# Remove them from all other queues
			for q in queues:
				q.remove(customer)

			return customer
		else:
			self.done(customer)

			return self.queue.get()

	def get_ticket(self):
		number = self.last_number + 1
		# Wrap numbers
		if (number > 9999):
			number = 0

		ticket = self.prefix + '%04i' % number
		self.last_number = number
		return ticket

	def add(self, customer):
		id = customer.emirates_id.id_number

		if (id not in self.numbers):
			self.numbers[id] = self.get_ticket()

			return self.queue.put(customer)

	def remove(self, customer):
		id = customer.emirates_id.id_number

		if (id in self.numbers):
			print "Removing %s from a queue" % id
			self.numbers.pop(id, None)

	def done(self, customer):
		self.remove(customer)

		return self.queue.task_done()

	def peek(self):
		return self.queue.qsize()

	def wait(self):
		return self.queue.join()


class Station(object):
    __metaclass__ = ABCMeta
    type = 'station type'
    prefix = 'S'

    def __init__(self, reception):
		self.queue = Queue(self.prefix)

    def peek(self):
		self.queue.peek()

    def add(self, customer):
		print "Putting %(customer)s in %(name)s queue at %(time)s" % \
			{"customer":customer.emirates_id.first_name, "name": self.type, "time": time.time()}
		
		self.queue.add(customer)