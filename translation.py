import time
import threading

from models import *
from lib import Queue


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

class Translation():
	def __init__(self, reception):
		self.queue = Queue()

		for i in range(2):
			agent = TranslationAgent(self.queue, reception)
			agent.setDaemon(True)
			agent.start()

		self.queue.wait()

	def add(self, customer):
		print "Putting %s in translation queue" % customer.emirates_id.first_name
		self.queue.add(customer)