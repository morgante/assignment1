import time
import threading
import random

from models import *
from lib import Queue, Station


class TranslationAgent(threading.Thread):
	def __init__(self, queue, reception):
		threading.Thread.__init__(self)
		self.queue = queue
		self.reception = reception

	def process(self, customer):
		print "Processing translation for %s" % customer.emirates_id.first_name

		time.sleep(random.randint(300, 600))

		customer.drivers_license_translation = Drivers_License_Translation(customer.drivers_license)
		return customer

	def run(self):
		print "Translation Agent(%s) is starting" % self.getName()
		while True:
			customer = self.queue.get()

			self.process(customer)

			self.reception.add(customer)

			self.queue.done(customer)

class Translation(Station):
	type = 'translation'
	prefix = 'C'

	def __init__(self, reception):
		super(Translation, self).__init__(reception)

		for i in range(2):
			agent = TranslationAgent(self.queue, reception)
			agent.setDaemon(True)
			agent.start()

		self.queue.wait()