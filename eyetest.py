import time
import threading

from models import *
from lib import Queue, Station


class EyeTestAgent(threading.Thread):
	def __init__(self, queue, reception):
		threading.Thread.__init__(self)
		self.queue = queue
		self.reception = reception

	def process(self, customer):
		print "Processing eye test for %s" % customer.emirates_id.first_name

		time.sleep(1)

		customer.eye_test = True
		return customer

	def run(self):
		print "Eye Test Agent(%s) is available" % self.getName()
		while True:
			customer = self.queue.get()

			self.process(customer)

			self.reception.add(customer)

			self.queue.done()

class EyeTesting(Station):
	type = 'eye test'

	def __init__(self, reception):
		super(EyeTesting, self).__init__(reception)

		for i in range(2):
			agent = EyeTestAgent(self.queue, reception)
			agent.setDaemon(True)
			agent.start()

		self.queue.wait()