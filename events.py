#!/usr/bin/python2

import multiprocessing
from Xlib import X, display, XK
from Xlib.ext import record, xtest
from Xlib.protocol import rq

class Catch(multiprocessing.Process):  
	
	def __init__(self, Detail, Type):
		multiprocessing.Process.__init__(self)
		self.disp = display.Display()
		self.Detail = Detail
		self.Type = Type

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
	  
			if event.type == X.KeyPress or event.type == X.ButtonPress:
				self.Detail.put(event.detail)
				self.Type.put(event.type)
					
def Is_Key(event):
	if event == X.KeyPress:
		return True
	else:
		return False

def String_to_Keycode(key):
	d=display.Display()
	keysym = XK.string_to_keysym(key)
	keycode = d.keysym_to_keycode(keysym)
	return keycode

def Keysym_to_String (key):
	d=display.Display()
	keysym = d.keycode_to_keysym(key, 0)
	return lookup_keysym(keysym)
	
def lookup_keysym(keysym):
    for name in dir(XK):
        if name[:3] == "XK_" and getattr(XK, name) == keysym:
            return name[3:]
    return Keycode(keysym)
	
def Fake_Key(Key):
	d=display.Display()
	Key = String_to_Keycode(Key)
	xtest.fake_input(d, X.KeyPress, Key) 
	d.sync()
	xtest.fake_input(d, X.KeyRelease, Key)
	d.sync()
	
def Fake_Button(Button):
	d=display.Display()
	xtest.fake_input(d, X.ButtonPress, int(Button)) 
	d.sync() 
	xtest.fake_input(d, X.ButtonRelease, int(Button))
	d.sync()
