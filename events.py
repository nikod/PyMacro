#!/usr/bin/python2

import sys
import os
import multiprocessing
from Xlib import X, XK, display
from Xlib.ext import record
from Xlib.protocol import rq

class Catch(multiprocessing.Process):  
	
	def __init__(self):
		multiprocessing.Process.__init__(self)
		self.disp = display.Display()
		self.event = lambda x: True

	
	def run(self):			  
		ctx = self.disp.record_create_context(
				0,
				[record.AllClients],
				[{
						"core_requests": (0, 0),
						"core_replies": (0, 0),
						"ext_requests": (0, 0, 0, 0),
						"ext_replies": (0, 0, 0, 0),
						"delivered_events": (0, 0),
						"device_events": (X.KeyPress, X.MotionNotify),
						"errors": (0, 0),
						"client_started": False,
						"client_died": False,
				}])
		  
		self.disp.record_enable_context(ctx, self.record_callback)
		self.disp.record_free_context(ctx)
	  
	def record_callback(self,reply):
		data = reply.data
		while len(data):
			event, data = rq.EventField(None).parse_binary_value(data, self.disp.display, None, None)
	  
			if event.type == X.KeyPress:
				self.event(event.detail)
			elif event.type == X.ButtonPress:
				self.event(event.detail)


if __name__ == "__main__":
	catch = Catch()
	catch.start()
