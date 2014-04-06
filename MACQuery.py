#!/usr/bin/env python
#-*- coding:utf-8 -*-

__all__ = ["MACQueryError", "BadFormatError", "BadRequestError", "MACQueryHandler"]

import xml.etree.ElementTree as ET
import re

PATTERN = r"""
^	#start from the beginning of the string
([0-9a-fA-F]{2}[-:]{1}[0-9a-fA-F]{2}[-:]{1}[0-9a-fA-F]{2})	#1st group is the first 3 pair of characters
([-:]{1}[0-9a-fA-F]{2}){0,3}	#2nd group would be the 3rd to 6th pair of characters which is optional
$	#stop at the end of the string
"""

REGEX_OF_MAC = re.compile(PATTERN, re.VERBOSE)

class MACQueryError(Exception): pass
class BadFormatError(MACQueryError):
	"""
	NOTE:
		--The length of the MAC addr must be more than 6 characters and less than 12 characters
		except the delimeters)
		--Allowed characters: 0-9, a-f, A-F
		--Allowed delimeters: '-', ':'
	EXAMPLE:
		--The following MAC addrs are allowed:
		"00-00-00","58-8D-09","EC-89-F5","04-2B-BB-22-1F","DC:2B:66:2B:E7:00"
		--While this following addrs are not allowed:
		"FC-F6" : too short
		"E8-9A-8F-FC-78-C9-A0" : too long
		"5$-22-33" : unsupported characters
		"9C.3A.AF" : unsupported delimeters
	"""
	def __init__(self):
		self.info = "ERROR: Bad Format MAC addrs."

	@property
	def usage(self):
		return self.__doc__

class BadRequestError(MACQueryError):
	"""
	NOTE:
		The BadRequestError occurred only when the MAC addrs that you specified is not contained in the
		database.
		There would be two optional possibilities:
		--Your hardware(network adapter) is not produced by legal manufacturer or by a new manufacturer
		that is legal but set up recently.
		--Our database is out of date.You can contact the author by email:silverbullet7714@gmail.com
	"""
	def __init__(self):
		self.info = "ERROR: No Suitable MAC addrs Found."

	@property
	def usage(self):
		return self.__doc__


class MACQueryHandler:
	def __init__(self, path):
		self.tree = ET.parse(path)
		self.root = self.tree.getroot()

	def query(self, addr):
		"""
		Query MAC INFO database(actually an xml file) with the given MAC addr.
		Check the validity of the given MAC addr first. If invalid, a BadFormatError exception will be raised.
		If valid, then query the database for detail information. If not found, a BadRequestError exception will be raised.
		Otherwise, a dictionary which contains three attributes of the given MAC addr will be returned.
		"""
		_match = REGEX_OF_MAC.search(addr)
		if _match:
				_queryString = _match.groups()[0].replace(":", "-").upper()
				result = {}
				for addr in self.root.findall("addr"):
						if addr.attrib.get("id") == _queryString:
								result["id"] = _queryString		#The given MAC addr
								result["org"] = addr.find("org").text.encode("utf8")	#The manufacturer of the network adapter
								result["detail"] = addr.find("detail").text.encode("utf8")  #Detail information of the manufacturer
								break
				if result:
						return result
				else:
						raise BadRequestError
		else:
				raise BadFormatError

if __name__ == "__main__":
		handler = MACQueryHandler("./data.xml")
		result = handler.query("00-00-0A")
		print result["id"]
		print result["org"]
		print result["detail"]
