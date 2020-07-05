# A Note wraps a File object, taking input from a recording session, 
# and writing progress to the disc incrementally, in case the process 
# is interrupted.
# 
# This object only does a few trivial tasks, but it makes things cleaner.
#
# If a filename is given, ensure it is
#	(1) Not a duplicate name, and
#	(2) Conforms to proper filename format
# Otherwise, use the current date/time to produce a filename.

from datetime import datetime
from string import ascii_letters, digits
from os import getcwd()

class Note:
	def __init__(self, filename=""):
		self.__path = getcwd()
		self.__thread = Thread(target = self.__write)

		if filename == "":
			filename = self.__default_filename()
		else:
			filename = self.__valid_filename(filename)
		
		self.__file = open("%s.txt" % filename, 'w')
	
	# Write the given string to the file, 
	def log_string(self, s):
		self.__file.write(s)
			
		self.__counter++
		if self.__counter >= limit:
			self.__counter = 0
			if self.__thread.is_alive():
				self.__thread.join() 
			self.__thread = new Thread(self.__write())
			self.__thread.start()
	
	# Called at the end of a recording session
	def close(self):
		if self.__thread.is_alive():
			self.__thread.join()
		self.__file.close()
	
	# Write current progress to disc
	# This is called in a separate thread to prevent a holdup
	def __write(self):
		self.__file.flush()
		fsync()

	# Produces a valid filename from the given string.
	# Replaces spaces with underscores
	def __valid_filename(self, s):
		valid_chars = "-_.() %s%s" % (ascii_letters, digits)
		filename = ''.join(c for c in s if c in valid_chars)
		filename = filename.replace(' ', '_')
		return filename

	# Use the formatted current date/time as the default filename.
	# Seconds seem granular enough to guarantee uniqueness,
	# but there is a check later to ensure no duplicate filenames,
	# just to be sure.
	# String format: MM-DD-YYYY-HHMMSS
	def __default_filename(self):
		d = datetime.now().date()
		t = datetime.now().time()
		return "%02d-%02d-%04d-%02d%02d%02d" % (d.month, d.day, d.year, t.hour, t.minute, t.second)		
