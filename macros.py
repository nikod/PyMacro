#!/usr/bin/python2
import multiprocessing
import events
import time
import subprocess

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
		macro = macro.split("-")
		while True:
			Detail = self.Detail.get()
			Type = self.Type.get()
			if events.Is_Key(Type):
				if events.Keysym_to_String(Detail) == macro[0]:	
					self.handler([macro[1]])
						
			else:
				if "Button%s" % Detail == macro[0]:
					self.handler([macro[1]])
				
					
	def Multiple(self, macro):
		macro = macro.split("(")
		macro[1] = macro[1].strip(")")
		while True:
			Detail = self.Detail.get()
			Type = self.Type.get()
			if events.Is_Key(Type):
				if events.Keysym_to_String(Detail) == macro[0]:	
					self.handler(macro[1].split("-"))
						
			else:
				if "Button%s" % Detail == macro[0]:
					macro = macro[1].split("-")
					self.handler(macro)
	
	def Script(self, macro):
		macro = macro.split("-")
		while True:
			Detail = self.Detail.get()
			Type = self.Type.get()
			if events.Is_Key(Type):
				if events.Keysym_to_String(Detail) == macro[0]:	
					subprocess.Popen(macro[1])
						
			else:
				if "Button%s" % Detail == macro[0]:
					subprocess.Popen(macro[1])
		
	def handler(self, macro):
		for i in range(len(macro)):
			if "|" in macro[i]:
				delay = macro[i].split("|")[0]
				macro[i] = macro[i].split("|")[1]
				time.sleep(int(delay))
				
			if "Button" in macro[i]:
				events.Fake_Button(macro[i].strip("Button"))
			else:
				events.Fake_Key(macro[i])
			
	def kill(self):
		self.Events.terminate()
		self.Events.join()
		self.terminate()
		
