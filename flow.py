import threading
import time

from printer import Printing
from translation import Translation
from lib import Queue

# Reception controls everything, and there is only one receptionist but she works instantaneously
class Reception():
	def __init__(self, queue, customers):
		self.queue = queue
		self.finished = 0
		self.desired = len(customers)

		self.translation = Translation(self)
		self.printer = Printing(self)

	def add(self, customer):
		self.queue.add(customer)

	def process(self, customer):
		print "Processing reception for %s" % customer.emirates_id.first_name

		if (customer.uae_license is not None):
			print "%s is finished at %s" % (customer.emirates_id.first_name, time.time())
			self.finished += 1
		elif (customer.drivers_license_translation is None):
			self.translation.add(customer)
		else:
			print "Printing reception for %s" % customer.emirates_id.first_name
			self.printer.add(customer)

		return customer

	def run(self):
		while self.finished < self.desired:
			customer = self.queue.get()

			self.process(customer)

			self.queue.done()

		self.queue.wait()

def run(customers):
	print "Starting to run through the DLD queue: %s" % time.time()

	queue = Queue()
	reception = Reception(queue, customers)

	for customer in customers:
		queue.add(customer)

	reception.run()

	print "Finished the DLD queue: %s" % time.time()