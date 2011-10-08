#!/usr/bin/python2
import subprocess
import conf
import macros
import threading
import time

class Window(threading.Thread):  

	def __init__(self):
		threading.Thread.__init__(self)
		
	def Title(self):
			return subprocess.Popen(["xprop", "-id", subprocess.Popen(["xprop", "-root", "_NET_ACTIVE_WINDOW"],
									stdout=subprocess.PIPE).communicate()[0].strip().split()[-1], "WM_NAME"],
									stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].strip().split('"', 1)[-1][:-1]

	def Recognition(self,conf):
		it_is = False
		name = ""
		indice = None
		for i in range(len(conf)):
			if conf[i]["Name"] == self.Title():
				it_is = True
				name = conf[i]["Name"]
				indice = i
		return it_is, name, indice

	
	def run(self):
		config = conf.Read()
		while True:
			it_is, name, indice = self.Recognition(config)
			if it_is:
				Macro = macros.Macros(config[indice])
				Macro.start()
				while name == self.Title():
					time.sleep(0.20)
				Macro.kill()
				Macro.join()	
			else:
				time.sleep(0.20)
	
