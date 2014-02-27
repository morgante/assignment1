import threading
import Queue
import time

class Reception(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue

	def process(self, customer):
		time.sleep(1)
		return customer

	def run(self):
		while not self.queue.empty():
			customer = self.queue.get()

			self.process(customer)

			self.queue.task_done()


# Flow execution stuff down here

queue = Queue.Queue()

# Put a customer into the DLD
def enter(customer):
	queue.put(customer)

def run():
	print "Starting to run through the DLD queue: %s" % time.time()

	for i in range(5):
		reception = Reception(queue)
		reception.setDaemon(True)
		reception.start()

	queue.join()

	print "Finished the DLD queue: %s" % time.time()