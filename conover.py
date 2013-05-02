#!/usr/bin/env python
# -*- coding: utf8 -*-
from _winreg import *
import sys

def check_enabled(aReg):
	overriden = False
	print "Checking connection override... ",
	aKey = OpenKey(aReg, r"Software\Classes\Software\Microsoft\Xlive") 
	for i in range(1024):                                           
		try:
			n,v,t = EnumValue(aKey,i)
			if 'ConnectionOverride' == n:
				print "it is on. Interface: %s" % v
				overriden = v
				break
		except EnvironmentError:
			print "it is off."
			break          
	CloseKey(aKey)
	return overriden

	
def enable(aReg, what=r'Hamachi'):
	print "Enabling"
	aKey = OpenKey(aReg, r"Software\Classes\Software\Microsoft\Xlive", 0, KEY_WRITE)
	try:   
	   SetValueEx(aKey,"ConnectionOverride",0, REG_SZ, what) 
	except EnvironmentError:                                          
		print "Encountered problems writing into the Registry..."
	CloseKey(aKey)
	
def disable(aReg):
	print "Disabling"
	aKey = OpenKey(aReg, r"Software\Classes\Software\Microsoft\Xlive", 0, KEY_WRITE)
	DeleteValue(aKey, r"ConnectionOverride")
	CloseKey(aKey)
	pass

if __name__ == "__main__":
	aReg = ConnectRegistry(None,HKEY_CURRENT_USER)
	enabled = check_enabled(aReg)
	
	if len(sys.argv) > 1:
		if "enable" == sys.argv[1] and not enabled:
			enable(aReg, 'Tunngle' if len(sys.argv) >= 3 and 'Tunngle' == sys.argv[2] else r'Hamachi')
		elif "disable" == sys.argv[1] and enabled:
			disable(aReg)
	else:
		print "Usage: %s [disable|enable [Hamachi|Tunngle]]" % sys.argv[0]
		
	CloseKey(aReg)
	