import time
import threading

from models import *
from lib import Queue, Station

class Printer():
	def __init__(self):
		self.idle = True
		self.time = 1 # How long it takes to print a card

	def is_idle(self):
		return self.idle

	def print_card(self, customer):
		if (not self.is_idle()):
			print "PRINTER JAMMMED"

		print "Starting to print card for %s at %s" % (customer.emirates_id.first_name, time.time())
		self.idle = True

		time.sleep(self.time)

		customer.uae_license = UAE_Drivers_License(customer)

		print "Finished printing card for %s at %s" % (customer.emirates_id.first_name, time.time())

		return 's';


class PrintAgent(threading.Thread):
	def __init__(self, queue, reception):
		threading.Thread.__init__(self)
		self.queue = queue
		self.reception = reception
		self.printer = Printer()

	def process(self, customer):
		self.printer.print_card(customer)

		# Send them to reception (and out the door)
		self.reception.add(customer)

	def run(self):
		print "PrintStation (%s) is starting" % self.getName()
		while True:
			customer = self.queue.get()

			self.process(customer)

			self.queue.done()

class Printing(Station):
	type = 'print'

	def __init__(self, reception):
		super(Printing, self).__init__(reception)

		station = PrintAgent(self.queue, reception)
		station.setDaemon(True)
		station.start()

		self.queue.wait()