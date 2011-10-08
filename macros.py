#!/usr/bin/python2
import multiprocessing
import events

class Macros(multiprocessing.Process):
	
	def __init__(self, conf):
		multiprocessing.Process.__init__(self)
		self.conf = conf
		self.event = ""
		self.Detail = multiprocessing.Queue()
		self.Type = multiprocessing.Queue()
		self.Events = events.Catch(self.Detail, self.Type)
		self.Events.start()
		
	def run(self):
		if self.conf["Type"] == "Single":
			self.Single(self.conf["Macro"])
		elif self.conf["Type"] == "Multiple":
			self.Multiple(self.conf["Macro"])
		elif self.conf["Type"] == "Script":
			self.Script(self.conf["Macro"])
			
	def Single(self, macro):
		print macro
		macro = macro.split("-")
		while True:
			Detail = self.Detail.get()
			Type = self.Type.get()
			if events.Is_Key(Type):
				print macro[0]
				print events.Keysym(Detail)
				if events.Keysym(Detail) == macro[0]:	
					self.handler(macro[1])
						
			else:
				if "Button%s" % Detail == macro[0]:
					self.handler(macro[1])
				
					
	def Multiple(self, macro):
		NotImplemented
	
	def Script(self, macro):
		NotImplemented

	def handler(self, macro):
		print macro
		if "Button" in macro:
			events.Fake_Button(macro.strip("Button"))
		else:
			events.Fake_Key(macro)
			
	def kill(self):
		self.Events.terminate()
		self.Events.join()
		self.terminate()
		
