#!/usr/bin/python2

from Xlib import XK

for name in dir(XK):
	if name[:3] == "XK_":
		print name[3:]
