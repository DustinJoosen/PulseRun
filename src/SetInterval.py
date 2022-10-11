import threading
import time


class SetInterval:
	def __init__(self, action, interval):
		self.action = action
		self.interval = interval
		self.stopEvent = threading.Event()

		thread = threading.Thread(target=self.__setInterval)
		thread.start()

	def __setInterval(self):
		nextTime = time.time()+self.interval
		while not self.stopEvent.wait(nextTime-time.time()):
			nextTime += self.interval
			self.action()

	def cancel(self):
		self.stopEvent.set()
