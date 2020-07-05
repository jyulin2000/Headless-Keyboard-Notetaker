# Process raw keystroke callbacks from the keyboard module into desired input
# Detect designated key sequences to change recording state/end execution
# Uses an internal Note object to write recorded input to a file

import keyboard
from threading import Semaphore
from string import ascii_letters
from Note import Note

replacement_map = {"space":' ', "tab":'\t', "enter":'\n'}

# We have to manually shift characters because we're reading in the literal keystrokes
shift_map = {'`':'~', '1':'!', '2':'@', '3':'#', '4':'$', '5':'%', '6':'^', '7':'&',
				'8':'*', '9':'(', '0':')', '-':'_', '=':'+', '[':'{', ']':'}', '\\':'|',
				';':':', '\'':'"', ',':'<', '.':'>', '/':'?'}

ignore_keys = {"alt", "shift", "esc", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8",
				"f9", "f10", "f11", "f12", "delete", "up", "down", "left", "right",
				"caps lock", "ctrl"}

class Keytracker:
	def __init__(self):
		self.__log = ""
		self.__semaphore = Semaphore(0)
		self.__shift_on = False # Press state of shift key
		self.__alt_on = False # Press state of alt key
		self.__note = None

		# Recording state:
		# 'o': off
		# 't': recording title
		# 'r': recording
		self.__recording = 'o'
	
	# Respond to a keystroke, behavior depends on current state			
	def callback(self, event):
		# If an error is raised we'll get trapped in execution by the semaphore
		# So wrap the entire block in a try/catch so we can release it
		# if something goes wrong.
		try:
			name = self.__process_event_name(event)
			
			if self.__recording == 'o':
				if name == '\n':
					self.__start_recording_title()
				elif name == "q" and self.__alt_on:
					self.__semaphore.release()	
					return
			
			elif self.__recording == 't':
				if name == '\n':
					self.__note = Note()
					self.__start_recording()
			
			elif self.__recording == 'r':
				if self.__alt_on:
					if name == 'e': # Command to end note
						self.__note.end()
						self.__stop_recording()
						return
					if name == 'q': # Quit program directly from recording session
						self.__note.end()
						self.__stop_recording()
						self.__semaphore.release()
						return
					elif name == 't': # Command to re-enter title
						return
				
				self.__note.write_char(name)				
			
			else:
				return
	
		except:
			self.__semaphore.release()

	# Translates raw keyboard stroke input into the desired character	
	def __process_event_name(self, event):
		name = event.name
		if event.scan_code == 12: name = '-' # The minus key maps wrong, so just hardcode it
		if self.__shift_on: name = self.__shift(name)
		if name in replacement_map: name = replacement_map[name]
		if name in ignore_keys: name = ""
	
		return name		
	
	# Return the keyboard-shifted character corresponding to the given one
	def __shift(self, ch):
		if len(ch) == 1:
			if ch in ascii_letters:
				return ch.upper()
			elif ch in shift_map:
				return shift_map[ch]
			else:
				return ch
		
		else: return ch	

	# The tracker needs to keep track of the state of the shift button,
	# in order to know when to manually shift characters. The two toggle
	# functions are bound to the events when the shift button is either
	# pressed or released, so we always know its current state.	
	def toggle_shift_on(self, event):
		self.__shift_on = True
	def toggle_shift_off(self, event):
		self.__shift_on = False
	
	# Same thing for the alt key (so we can detect commands for state changes)
	def toggle_alt_on(self, event):
		self.__alt_on = True
	def toggle_alt_off(self, event):
		self.__alt_on = False	
		
	def start(self):
		keyboard.on_press(callback=self.callback)
		keyboard.on_press_key("shift", callback=self.toggle_shift_on)
		keyboard.on_release_key("shift", callback=self.toggle_shift_off)
		keyboard.on_press_key("alt", callback=self.toggle_alt_on)
		keyboard.on_release_key("alt", callback=self.toggle_alt_off)

		self.__semaphore.acquire()
	
	def __start_recording_title(self):
		self.__recording = 't'
		print("Recording title...")
	
	def __start_recording(self):
		self.__recording = 'r'
		print("Recording...")
	
	def __stop_recording(self):
		self.__recording = 'o'
		print("Recording session ended.")
	
if __name__ == "__main__":
	keytracker = Keytracker()
	keytracker.start()
		
