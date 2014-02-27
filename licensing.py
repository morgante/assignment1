import time
import threading

from models import *
from lib import Queue, Station
from printer import Printing


class LicensingAgent(threading.Thread):
	def __init__(self, queue, reception):
		threading.Thread.__init__(self)
		self.queue = queue
		self.reception = reception
		self.printer = Printing(reception)

	def process(self, customer):
		print "Processing licensing for %s" % customer.emirates_id.first_name

		# Enter biographical information, existing license, visa (passport), and emirates ID
		app = Application(customer.emirates_id.first_name, customer.emirates_id.last_name, \
			customer.drivers_license_translation, customer.passport, customer.emirates_id)

		# Enter eye test
		app.eye_test = customer.eye_test

		# Enter payment
		app.paid = True

		# Make this take some time
		time.sleep(1)
		
		# Send them to print it
		self.printer.add(customer)
		
		return customer

	def run(self):
		print "Licensing Agent(%s) is starting" % self.getName()
		while True:
			customer = self.queue.get()

			self.process(customer)

			self.queue.done(customer)

class Licensing(Station):
	type = 'licensing'

	def __init__(self, reception):
		super(Licensing, self).__init__(reception)

		for i in range(2):
			agent = LicensingAgent(self.queue, reception)
			agent.setDaemon(True)
			agent.start()

		self.queue.wait()