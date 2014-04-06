#!/usr/bin/env python
#-*- coding:utf-8 -*-

class TXTtoXMLHandler:
	def __init__(self, ptxt, pxml):
		self.ptxt = ptxt
		self.pxml = pxml

	def _open(self):
		try:
			self._fileTXT = open(self.ptxt, "r")
			self._fileXML = open(self.pxml, "w")
		except IOError as err:
			print str(err)
	
	def _close(self):
		self._fileTXT.close()
		self._fileXML.close()

	def _stripEnds(self, s):
		return s.lstrip().rstrip()

	def _handleEntityRef(self, s):
		_entityRefs = {
				"<" : "&lt;",
				">" : "&gt;",
				"&" : "&amp;",
				"'" : "&apos;",
				"\"" : "&quot;"
		}

		for entity, ref in _entityRefs.items():
				s = s.replace(entity, ref)

		return s

	def txt_to_xml(self):
		self._open()

		_node = """\t<addr id="%s">
			<org>%s</org>
			<detail>%s</detail>\n\t</addr>"""

		print >> self._fileXML, "<?xml version=\"1.0\"?>"
		print >> self._fileXML, "<mac>"

		while True:
				line = self._fileTXT.readline()
				if not line:
						break
				else:
						_IdOrg = map(self._stripEnds, line.split("(hex)"))
						
						self._fileTXT.readline()
						_info = []
						line = self._fileTXT.readline()
						while line != "\n":
								_info.append(line)
								line = self._fileTXT.readline()

						_info = map(self._stripEnds, _info)
						_detail = ",".join(_info)

						_nodeTMP = _node % (self._handleEntityRef(_IdOrg[0]), self._handleEntityRef(_IdOrg[1]),\
								self._handleEntityRef(_detail))

						print >> self._fileXML, _nodeTMP

		print >> self._fileXML, "</mac>"
		
		self._close()

if __name__ == "__main__":
		handler = TXTtoXMLHandler("./oui.txt", "./data.xml")
		handler.txt_to_xml()
