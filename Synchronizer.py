# Keep track of notes in the local filesystem and upload them
# to Google Keep, using an unofficial api.
# Runs on a separate thread that tries to upload any 
# non-synchronized files to Keep, then pauses and waits
# for new notes to be generated to be uploaded.

import threading
from collections import deque
import os
import pickle
from gkeepapi import Keep
from time import sleep

file_queue_name = "file_queue.pickle"

# Keep track of notes locally and upload them to Google Keep
class Synchronizer(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.__running = False
		
		self.__file_queue = deque()
	
		# This is for ensuring safe access to the file queue,
		# which is updated whenever a new note file is created.
		# deques are thread-safe/atomic, but I wanted to prevent
		# any weird stuff from happening if the upload loop
		# is running and a new file is added at the same time.
		self.__file_queue_lock = threading.Lock()
		
		# Using this event we pause the thread, allowing it to
		# execute only when there are new files to be synced.
		self.__event = threading.Event()

		self.__notes_path = os.getcwd() + "/notes"
		self.__auth_path = os.getcwd() + "/google_auth/auth"
		self.__keep = Keep()
		self.__logged_in = False
	
	def run(self):
		if not os.path.exists(self.__notes_path):
			os.mkdir(self.__notes_path)
		if os.path.exists(file_queue_name):
			with open(file_queue_name, 'rb') as f:
				 	self.__file_queue = pickle.load(f)
		
		self.__running = True
		while self.__running:
			if not self.__logged_in:
				self.__logged_in = self.__login()

			if self.__logged_in:
				self.__upload_file_queue()
			
			self.__event.wait()
	
		# Try one last time to upload unsynced files
		if len(self.__file_queue) > 0:
			pass
	
		with open(file_queue_name, 'wb') as f:
			pickle.dump(self.__file_queue, f, pickle.HIGHEST_PROTOCOL)

	# Add a filename to be synchronized with Keep
	# Each call to this method will be run in its own
	# unique Thread by Controller.
	def alert_new_file(self, filename):
		with self.__file_queue_lock:
			self.__file_queue.append(filename)
		
		self.__event.set()
		self.__event.clear()
	
	# Allow thread to join
	def close(self):
		self.__running = False
		self.__event.set()
	
	# Try to upload each queued file once.
	# Requeue if something fails
	# We never want to get stuck in here or this thread can't join,
	# so ensure we don't by putting timeouts on the sync attempts 
	def __upload_file_queue(self):
		with self.__file_queue_lock:	
			for i in range(len(self.__file_queue)):
				filename = self.__file_queue.pop()
				#print(filename)
				self.__file_queue.appendleft(filename)				 

	# Use provided authentication to get an instance of the Keep API
	def __login(self):
		user = ""
		pswrd = ""
		
		if os.path.exists(self.__auth_path):
			try:
				with open(self.__auth_path, 'r') as f:
					user_pass = f.readline()[:-1].split(',')
					user = user_pass[0]
					pswrd = user_pass[1]
			except:
				return False
		
		return self.__keep.login(user, pswrd)	
