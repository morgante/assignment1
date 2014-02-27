import time
import threading
import random

from models import *
from lib import Queue, Station


class EyeTestAgent(threading.Thread):
	def __init__(self, queue, reception):
		threading.Thread.__init__(self)
		self.queue = queue
		self.reception = reception

	def process(self, customer):
		print "Processing eye test for %s" % customer.emirates_id.first_name

		time.sleep(random.randint(120,300))

		customer.eye_test = EyeTest(customer.emirates_id.first_name, customer.emirates_id.last_name, \
			customer.emirates_id.nationality, customer.emirates_id.gender, customer.emirates_id.date_of_birth, None)
		
		return customer

	def run(self):
		print "Eye Test Agent(%s) is available" % self.getName()
		while True:
			customer = self.queue.get()

			self.process(customer)

			self.reception.add(customer)

			self.queue.done(customer)

class EyeTesting(Station):
	type = 'eye test'
	prefix = 'B'

	def __init__(self, reception):
		super(EyeTesting, self).__init__(reception)

		for i in range(2):
			agent = EyeTestAgent(self.queue, reception)
			agent.setDaemon(True)
			agent.start()

		self.queue.wait()