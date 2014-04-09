#!/usr/bin/env python
#-*- coding:utf-8 -*-

from MACQuery import MACQueryHandler, BadFormatError, BadRequestError
import sys, os
import getopt

class GetMACInfo:
	_resultInfo = """
	HWaddr : %s
	Manufacturer : %s
	M's addr : %s
	"""
	_warning_not_found = """
	HWaddr : %s
	Stop : %s
	Note : Unknown MAC addrs.
	Reasons:
		Network Adapter was produced by Illegal Manufacturer;
		MAC addr has been modified artificially;
		MAC addr of a Virtual Network Adapter.
	"""

	_warning_bad_format = """
	HWaddr : %s
	Stop : %s
	"""

	def __init__(self, path="data.xml"):
		self.handler = MACQueryHandler(path)
		self.result = []

	def get_macinfo(self):
		_platform = sys.platform
		method = getattr(self, "get_macinfo_%s" % _platform)
		method()
	
	def get_macinfo_linux2(self):
		_usage = """
		python main.py -h or python main.py --help
		python main.py -a LIST or python main.py --addr=LIST (LIST is MAC addrs seperated by commas)
		"""
		if sys.argv[1:]:
				try:
						opt, args = getopt.getopt(sys.argv[1:], "ha:", ["help", "addr="])
				except getopt.GetoptError as err:
						print str(err)
						print _usage
				else:
						for tag, value in opt:
								if tag in ("-h", "--help"):
										print _usage
								elif tag in ("-a", "--addr"):
										_maclist = map(str.strip, value.split(","))
										self._getBy(*_maclist)
		else:
				self._getDefaultLinux2()


	def get_macinfo_win32(self):
		_in_addrs = raw_input("Input a MAC addr or a list of MAC addrs seperated by commas\n\
		(default to local machine's MAC addrs):").split(",")
		_maclist = map(str.strip, _in_addrs)

		if _maclist[0]:
				self._getBy(*_maclist)
		else:
				self._getDefaultWin32()


	def _getBy(self, *argv):
		for addr in argv:
				try:
						_result = self.handler.query(addr)
				except BadFormatError as err:
						_tmp_warning_bad_format = self._warning_bad_format % (addr, str(err))
						self.result.append(_tmp_warning_bad_format)
				except BadRequestError as err:
						_tmp_warning_not_found = self._warning_not_found % (addr, str(err))
						self.result.append(_tmp_warning_not_found)
				else:
						_tmp_resultInfo = self._resultInfo % (_result["id"], _result["org"], _result["detail"])
						self.result.append(_tmp_resultInfo)

	def _getDefaultLinux2(self):
		_pipe_data = os.popen("/sbin/ifconfig -a | grep -i 'HWaddr'", "r").read()
		_tmp = map(str.strip, _pipe_data.split("\n")[:-1])
		_maclist = [item.split()[-1] for item in _tmp]

		self._getBy(*_maclist)

	def _getDefaultWin32(self):
		_pipe_data = os.popen("wmic nicconfig get MACAddress").read()
		_maclist = _pipe_data.split()[1:]

		self._getBy(*_maclist)

	def printHWaddrs(self):
		for info in self.result:
				print "+--------------------------------------------------------------------------------------------------------+"
				print info
				print "+--------------------------------------------------------------------------------------------------------+"


if __name__ == "__main__":
		handler = GetMACInfo()
		handler.get_macinfo()
		handler.printHWaddrs()
