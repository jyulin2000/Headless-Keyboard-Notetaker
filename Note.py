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
import Controller

space_chars = " \n\t"
stop_chars = ".,:;\"?!i=+[]{}()/?\\|~`@#$%^&*"
class Note:
	def __init__(self, filename=""):
		self.__path = self.__get_path_to_notes()
		self.__buffer = deque()
		self.__title_mode = False
		self.__title_buffer = None
		
		if filename == "":
			filename = self.__default_filename()
		else:
			filename = self.__valid_filename(filename)
		filename = self.__unique_filename(filename)
	
		self.__original_filename = filename
		self.__cur_filename = filename	
		self.__file = open(self.path_to(filename), 'w')
	
	# Add the given character to the input buffer or title buffer, 
	# depending on mode.
	def write_char(self, ch):
		buffer = self.__get_current_buffer() 
		if ch == "":
			return
		else:
			buffer.append(ch)
	
	# Backspace the last character
	def char_backspace(self):
		buffer = self.__get_current_buffer()
		if len(buffer) > 0:
			buffer.pop()
	
	# Backspace the last word
	# Mimics the behavior of ctrl-backspace in Google Docs
	def word_backspace(self):
		buffer = self.__get_current_buffer()
		
		# First pop off all spaces
		# I think python has short circuiting, otherwise fix this
		while len(buffer) > 0 and buffer[-1] == " ":
			buffer.pop()
		if len(buffer) > 0:
			c = buffer.pop()
			if c in space_chars:
				return
			elif c in stop_chars:
				while len(buffer) > 0 and buffer[-1] in stop_chars:
					buffer.pop()
			else:
				while (len(buffer) > 0 and 
					buffer[-1] not in stop_chars and
					buffer[-1] not in space_chars):
					buffer.pop()
	
	# Record entered keys to the title buffer, instead of the normal one	
	def start_title(self):
		self.__title_buffer = deque()
		self.__title_mode = True
	
	# Save full inputted title string, return to normal recording
	def end_title(self):
		if len(self.__title_buffer) == 0:
			self.__cur_filename = self.__original_filename
		
		else:
			title = ""
			while len(self.__title_buffer) > 0:
				title += self.__title_buffer.popleft()
				
			title = self.__valid_filename(title)
			self.__cur_filename = self.__unique_filename(title)

		self.__title_mode = False
		self.__title_buffer = None
	
	# Return the current title
	def get_title(self):
		return self.__cur_filename
	
	# Return whether default title (date/time) is used
	def uses_default_title(self):
		return self.__cur_filename == self.__original_filename	
	
	# Writes the input buffer to file on disc,
	# returns the final filename of the note
	def end(self):
		while len(self.__buffer) > 0:
			self.__file.write(self.__buffer.popleft())
		
		self.__file.close()
		
		if self.__cur_filename != self.__original_filename:
			shutil.move(self.path_to(self.__original_filename),
						self.path_to(self.__cur_filename))
		
		return "%s.txt" % self.__cur_filename

	# Returns full path to the existing notes folder,
	# creates notes folder if it does not exist already.
	def __get_path_to_notes(self):
		p = Controller.WORKING_DIRECTORY + "/notes"
		if not os.path.exists(p):
			try:
				os.mkdir(p)
			except OSError:
				pass
		return p
	
	# Produces full path to given filename with extension .txt
	def path_to(self, s):
		return "%s/%s.txt" % (self.__path, s)
	
	def __get_current_buffer(self):
		return self.__title_buffer if self.__title_mode else self.__buffer

	# Produces a valid filename from the given string.
	# I'm allowing spaces
	def __valid_filename(self, s):
		valid_chars = "-_.() %s%s" % (ascii_letters, digits)
		filename = ''.join(c for c in s if c in valid_chars)
		#filename = filename.replace(' ', '_')
		return filename
	
	# Adjusts the given filename if it already exists.
	# Assumes filename is already valid.
	def __unique_filename(self, s):
		if os.path.exists(self.path_to(s)):
			n = 1
			f = "%s (%d)"
			while os.path.exists(self.path_to(f % (s, n))):
				n += 1
			return f % (s, n)	
		else:
			return s
	
	# Use the formatted current date/time as the default filename.
	# Seconds seem granular enough to guarantee uniqueness,
	# but there is a check later to ensure no duplicate filenames,
	# just to be sure.
	#
	# String format: MM-DD-YYYY-HHMMSS
	def __default_filename(self):
		d = datetime.now().date()
		t = datetime.now().time()
		return "%02d-%02d-%04d-%02d%02d%02d" % (d.month, d.day, d.year, t.hour, t.minute, t.second)		
