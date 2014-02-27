import threading
import Queue
import time

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

			self.queue.task_done()

class Translation():
	def __init__(self, reception):
		self.queue = Queue.Queue()

		for i in range(2):
			agent = TranslationAgent(self.queue, reception)
			agent.setDaemon(True)
			agent.start()

		self.queue.join()

	def add(self, customer):
		print "Putting %s in translation queue" % customer.emirates_id.first_name
		self.queue.put(customer)

# Reception controls everything, and there is only one receptionist but she works instantaneously
class Reception():
	def __init__(self, queue, customers):
		self.queue = queue
		self.finished = 0
		self.desired = len(customers)

		self.translation = Translation(self)

	def add(self, customer):
		self.queue.put(customer)

	def process(self, customer):
		print "Processing reception for %s" % customer.emirates_id.first_name

		if (customer.drivers_license_translation is None):
			self.translation.add(customer)
		else:
			print "%s is finished at %s" % (customer.emirates_id.first_name, time.time())
			self.finished += 1

		return customer

	def run(self):
		while self.finished < self.desired:
			customer = self.queue.get()

			self.process(customer)

			self.queue.task_done()

		self.queue.join()

def run(customers):
	print "Starting to run through the DLD queue: %s" % time.time()

	queue = Queue.Queue()
	reception = Reception(queue, customers)

	for customer in customers:
		queue.put(customer)

	reception.run()

	print "Finished the DLD queue: %s" % time.time()