import threading
import time


class SetInterval:
	def __init__(self, action, interval):
		self.action = action
		self.interval = interval
		self.stop_event = threading.Event()

		thread = threading.Thread(target=self.__set_interval)
		thread.start()

	def __set_interval(self):
		next_time = time.time() + self.interval
		while not self.stop_event.wait(next_time - time.time()):
			next_time += self.interval
			self.action()

	def cancel(self):
		self.stop_event.set()
