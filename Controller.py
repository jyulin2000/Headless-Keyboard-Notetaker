from Keytracker import Keytracker
from Synchronizer import Synchronizer
from threading import Thread
from collections import deque

# REPLACE THIS WITH YOUR WORKING DIRECTORY FOR YOUR PROJECT
WORKING_DIRECTORY = "/home/pi/Projects/Headless-Keyboard-Notetaker"

class Controller:
	def __init__(self):
		self.__keytracker = Keytracker(self)
		self.__synchronizer = Synchronizer()
		self.__filename_threads = deque()
		
	def start(self):
		self.__synchronizer.start()
		self.__keytracker.start()
		
		self.__join_all_threads()
		
	def alert_new_file(self, filename): 
		self.__drop_dead_threads()
	
		t = Thread(target = self.__synchronizer.alert_new_file, args = (filename,))
		t.start()
		self.__filename_threads.append(t)
	
	# Allow any closed filename threads to be garbage collected
	def __drop_dead_threads(self):
		for i in range(len(self.__filename_threads)):
			t = self.__filename_threads.pop()
			if t.is_alive():
				self.__filename_threads.appendleft(t)
			else:
				t.join()
		
	def __join_all_threads(self):
		self.__synchronizer.close()
		self.__synchronizer.join()
		while len(self.__filename_threads) > 0:
			self.__filename_threads.pop().join()
				
