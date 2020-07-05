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
import os
import shutil
from collections import deque

class Note:
	def __init__(self, filename=""):
		self.__path = os.getcwd() + "/notes"
		self.__buffer = deque()
		self.__title_mode = False
		self.__title_buffer = None
		
		if filename == "":
			filename = self.__default_filename()
		else:
			filename = self.__valid_filename(filename)
		
		self.__original_filename = filename
		self.__cur_filename = filename	
		self.__file = open("%s/%s.txt" % (self.__path, filename), 'w')
	
	def write_char(self, ch):
		buffer = self.__title_buffer if self.__title_mode else self.__buffer
		if ch == "":
			return
		elif ch == "backspace":
			buffer.pop()
		else:
			buffer.append(ch)
	
	def start_title(self):
		self.__title_buffer = deque()
		self.__title_mode = True
	
	def end_title(self):
		title = ""
		while len(self.__title_buffer) > 0:
			title += self.__title_buffer.popleft()
		
		title = self.__valid_filename(title)
		self.__cur_filename = title

		self.__title_mode = False
		self.__title_buffer = None

	def end(self):
		while len(self.__buffer) > 0:
			self.__file.write(self.__buffer.popleft())
		
		self.__file.close()
		
		if self.__cur_filename != self.__original_filename:
			shutil.move("%s/%s.txt" % (self.__path, self.__original_filename),
						"%s/%s.txt" % (self.__path, self.__cur_filename))

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
