import time
import threading

from models import *
from lib import Queue, Station


class TranslationAgent(threading.Thread):
	def __init__(self, queue, reception):
		threading.Thread.__init__(self)
		self.queue = queue
		self.reception = reception

	def process(self, customer):
		print "Processing translation for %s" % customer.emirates_id.first_name

		time.sleep(1)

		customer.drivers_license_translation = True
		return customer

	def run(self):
		print "Translation Agent(%s) is starting" % self.getName()
		while True:
			customer = self.queue.get()

			self.process(customer)

			self.reception.add(customer)

			self.queue.done()

class Translation(Station):
	type = 'translation'

	def __init__(self, reception):
		super(Translation, self).__init__(reception)

		for i in range(2):
			agent = TranslationAgent(self.queue, reception)
			agent.setDaemon(True)
			agent.start()

		self.queue.wait()