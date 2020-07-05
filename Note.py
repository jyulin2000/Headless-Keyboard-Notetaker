# Handles file creation/writing 
#
# A Note takes input from a recording session, character by character,
# and stores it in a queue, popping the top character if backspace is
# pressed. When the Note is ended, it writes the queue to its file and closes it.
# 
# This object only does a few trivial tasks, but it makes things cleaner.
# 
# Filename rules:
# If a filename is given, ensure it is
#	(1) Not a duplicate name, and
#	(2) Conforms to proper filename format
# Otherwise, use the current date/time to produce a filename.

from datetime import datetime
from string import ascii_letters, digits
from os import getcwd

class Note:
	def __init__(self, filename=""):
		self.__path = getcwd()
	
		if filename == "":
			filename = self.__default_filename()
		else:
			filename = self.__valid_filename(filename)
		
		self.__original_filename = filename	
		self.__file = open("%s/notes/%s.txt" % (self.__path, filename), 'w')
	
	def write_char(self, ch):
		if ch == "":
			return
		elif ch == "backspace":
			print("\nbackspace pressed: figure out how to handle this")
			return
		else:
			self.__file.write(ch)
	
	def end(self):
		self.__file.close()
	
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
