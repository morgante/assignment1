import threading
import time

from translation import Translation
from licensing import Licensing
from eyetest import EyeTesting
from lib import Queue, Station

# Reception controls everything, and there is only one receptionist but she works instantaneously
class Reception(Station):
	type = 'reception'
	prefix = 'R'

	def __init__(self, queue, customers):
		self.queue = queue

		self.finished = []
		self.failures = []
		self.desired = len(customers)

		self.translation = Translation(self)
		self.testing = EyeTesting(self)
		self.licensing = Licensing(self)

	def process(self, customer):
		print "Processing reception for %s" % customer.emirates_id.first_name

		if (customer in self.failures):
			return

		if (customer.eye_test is None):
			self.testing.add(customer)
			print "Eye testing queue is %s people" % self.testing.peek()

		if (customer.drivers_license_translation is None):
			self.translation.add(customer)
			print "Translation queue is %s people" % self.translation.peek()

		if (customer.eye_test is not None and customer.drivers_license_translation is not None and customer.uae_license is None):
			self.licensing.add(customer)

		if (customer.uae_license is not None):
			print "%s is finished at %s" % (customer.emirates_id.first_name, time.time())
			self.finished.append(customer)

	def fail(self, customer, cycle=True):
		self.failures.append(customer)

		if (cycle):
			self.add(customer)

	def run(self):
		while len(self.finished) + len(self.failures) < self.desired:
			customer = self.queue.get()

			self.process(customer)

			self.queue.done(customer)

		self.queue.wait()

		print "Finished the DLD queue: %s" % time.time()

		return self.finished

def run(customers):
	print "Starting to run through the DLD queue: %s" % time.time()

	queue = Queue('R')
	reception = Reception(queue, customers)

	for customer in customers:
		if (customer.emirates_id is None):
			print "Unknown customer has failed permanently dueto lack of Emirates ID"
			reception.fail(customer, False)
		else:
			queue.add(customer)

	return reception.run()
