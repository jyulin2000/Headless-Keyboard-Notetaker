import keyboard
from threading import Semaphore
from string import ascii_letters

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
		self.__recording = False # Recording state

	def callback(self, event):
		name = self.__process_event_name(event)
		
		if self.__recording:
			if name == "\n":
				name = ""
				self.__log = ""
			if name == "e" and self.__alt_on: 
				name = ""
				self.__stop_recording()
							
			if name not in ignore_keys: self.__log += name
	
		else:
			if name == "\n":
				self.__start_recording()
			elif name == "q" and self.__alt_on:
				name = ""
				self.__semaphore.release()
	
	def __write_log(self):
		return
	
	# Translates raw keyboard stroke input into the desired character	
	def __process_event_name(self, event):
		name = event.name
		if event.scan_code == 12: name = '-' # The minus key maps wrong, so just hardcode it
		if self.__shift_on: name = self.__shift(name)
		if name in replacement_map: name = replacement_map[name]
		
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
	
	# Same thing for the alt key (so we can detect commands for state-changes)
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
	
	def __start_recording(self):
		self.__recording = True
		print("Recording...")
	
	def __stop_recording(self):
		self.__recording = False
		self.__log = ""
		print("Recording session ended.")
	
if __name__ == "__main__":
	keytracker = Keytracker()
	keytracker.start()
		
