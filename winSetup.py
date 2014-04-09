#!/usr/bin/env python
#-*- coding:utf-8 -*-

import _winreg
import os, sys
import re

REGEX_PATH = re.compile(r"^[A-Z]{1}:(\\[A-Za-z\s]+){0,5}\\?$")
REGEX_HKEY = re.compile(r"")

class PackageInstall:
	def __init__(self, path="C:"):
		self.path = path.replace("\\", "_")

	def _fontRegister(self):
		_sub_key = "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Console\\TrueTypeFont"
		try:
				_preKeyHandle = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, _sub_key, 0, _winreg.KEY_ALL_ACCESS)
				_winreg.SetValueEx(_preKeyHandle, "000", 0, _winreg.REG_SZ, "Source Code Pro")
		except WindowsError as err:
				print str(err)
				sys.exit(2)
		finally:
				_winreg.CloseKey(_preKeyHandle)

	def _copyFiles(self):
		pass

	def _mainRegister(self):
		_pairs = [("CodePage", _winreg.REG_DWORD, 850),\
				("ScreenBufferSize", _winreg.REG_DWORD, 19660909),\
				("WindowSize", _winreg.REG_DWORD, 2293869),\
				("FontSize", _winreg.REG_DWORD, 1179648), \
				("FontFamily", _winreg.REG_DWORD, 54),\
				("FontWeight", _winreg.REG_DWORD, 400), \
				("FaceName", _winreg.REG_SZ, "Source Code Pro"),
				]

		_suffix = "_MACQuery_main.exe"
		_hkey = self.path[-1] == "_" and self.path[:-1]+_suffix or self.path + _suffix

		try:
				_preKeyHandle = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, "Console", 0, _winreg.KEY_ALL_ACCESS)
				_newKeyHandle = _winreg.CreateKey(_preKeyHandle, _hkey)

				for _name, _type, _value in _pairs:
						_winreg.SetValueEx(_newKeyHandle, _name, 0, _type, _value)
		except WindowsError as err:
				print str(err)
				sys.exit(2)
		finally:
				_winreg.CloseKey(_newKeyHandle)
				_winreg.CloseKey(_preKeyHandle)


	def packed(self):
		pass


if __name__ == "__main__":
		pass
