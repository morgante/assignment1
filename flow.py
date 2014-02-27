import threading
import time

from printer import Printing
from translation import Translation
from eyetest import EyeTesting
from lib import Queue, Station

# Reception controls everything, and there is only one receptionist but she works instantaneously
class Reception(Station):
	type = 'reception'

	def __init__(self, queue, customers):
		self.queue = queue

		self.finished = 0
		self.desired = len(customers)

		self.translation = Translation(self)
		self.testing = EyeTesting(self)
		self.printer = Printing(self)

	def process(self, customer):
		print "Processing reception for %s" % customer.emirates_id.first_name

		if (customer.eye_test is None):
			self.testing.add(customer)
			print "Eye testing queue is %s people" % self.testing.peek()

		if (customer.drivers_license_translation is None):
			self.translation.add(customer)
			print "Translation queue is %s people" % self.translation.peek()

		if (customer.eye_test is not None and customer.drivers_license_translation is not None):
			self.printer.add(customer)

		if (customer.uae_license is not None):
			print "%s is finished at %s" % (customer.emirates_id.first_name, time.time())
			self.finished += 1

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