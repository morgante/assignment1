import time
import threading
from datetime import datetime
import random

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
		# Emirates ID is basic requirement
		if (customer.emirates_id is None):
			print "Unknown customer fails due to lack of Emirates ID"
			return self.reception.fail(customer)

		name = customer.emirates_id.first_name

		print "Processing licensing for %s" % name

		# Confirm that they have valid EID
		if (customer.emirates_id.expiry_date < datetime.now()):
			print "%s fails because their ID is expired" % name
			return self.reception.fail(customer)

		# Confirm that they have passport
		if (customer.passport is None or customer.passport.expiry_date < datetime.now()):
			print "%s fails because they lack a valid passport" % name
			return self.reception.fail(customer)

		# Confirm that they have license
		if (customer.drivers_license is None or customer.drivers_license.expiry_date < datetime.now()):
			print "%s fails because they lack a valid license" % name
			return self.reception.fail(customer)

		# Confirm that they have a license translation
		if (customer.drivers_license_translation is None):
			customer.drivers_license_translation = None
			return self.reception.add(customer)

		# Confirm that they have an eye test
		if (customer.eye_test is None or customer.eye_test.expiry_date < datetime.now()):
			customer.eye_test = None
			return self.reception.add(customer)

		# Confirm consistency
		# --- date of birth, first name, last name, nationality, gender
		if (not customer.emirates_id.date_of_birth == customer.passport.date_of_birth == customer.drivers_license.date_of_birth or \
			not customer.emirates_id.last_name == customer.passport.last_name == customer.drivers_license.last_name or \
			not customer.emirates_id.nationality == customer.passport.nationality == customer.drivers_license.nationality or \
			not customer.emirates_id.gender == customer.passport.gender == customer.drivers_license.gender or \
			not customer.emirates_id.first_name == customer.passport.first_name == customer.drivers_license.first_name
			):
			print "%s fails because they have inconsistent information" % name
			return self.reception.fail(customer)

		# Enter biographical information, existing license, visa (passport), and emirates ID
		app = Application(customer.emirates_id.first_name, customer.emirates_id.last_name, \
			customer.drivers_license_translation, customer.passport, customer.emirates_id)

		# Enter eye test
		app.eye_test = customer.eye_test

		# Enter payment
		app.paid = True

		# Make this take some time
		time.sleep(random.randint(120,300))
		
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
	prefix = 'A'

	def __init__(self, reception):
		super(Licensing, self).__init__(reception)

		for i in range(2):
			agent = LicensingAgent(self.queue, reception)
			agent.setDaemon(True)
			agent.start()

		self.queue.wait()