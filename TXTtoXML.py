#!/usr/bin/env python
#-*- coding:utf-8 -*-

class TXTtoXMLHandler:
	"""
	Convert the oui.txt(provided by the IEEE, which contains the MAC addrs and
	corresponding manufacturers and manufacturers' detail infomation) into an
	xml file(data.xml) so that it would be much easier for itering.
	"""
	def __init__(self, ptxt, pxml):
		self.ptxt = ptxt 	#the file path of the oui.txt
		self.pxml = pxml	#the file path of the data.txt

	def _open(self):
		"""
		Open oui.txt and data.xml as file objects _fileTXT and _fileXML,
		no need to worry about the existence of the data.xml, because it
		would be created automatically if not exists.
		"""
		try:
			self._fileTXT = open(self.ptxt, "r")
			self._fileXML = open(self.pxml, "w")
		except IOError as err:
			print str(err)
	
	def _close(self):
		"""
		The key reason to call this method is when file object closed, the buffer
		would be refreshed automatically. As a result, all data would be write to
		the hard disk(data.xml).
		"""
		self._fileTXT.close()
		self._fileXML.close()

	def _stripEnds(self, s):
		"""
		Strip the leading and trailing whitespace,"\n", and "\t" characters.
		"""
		return s.lstrip().rstrip()

	def _handleEntityRef(self, s):
		"""
		Handle the entity references, replace "<" by "&lt;", ">" by "&gt;", "&" by "&amp;",
		"'" by "&apos;", and "\"" by "&quot;".
		"""
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
		"""
		Core function of class TXTtoXMLHandler:
		Read lines from the oui.txt file and convert it to corresponding xml Elements, then write
		them into the data.xml.
		"""
		self._open()

		#the common fomat of Element Node <addr> as well as its subElement Node <org> and <detail>
		_node = """\t<addr id="%s">
			<org>%s</org>
			<detail>%s</detail>\n\t</addr>"""

		#write the xml instruction and root Element Node to the data.xml file
		print >> self._fileXML, "<?xml version=\"1.0\"?>"
		print >> self._fileXML, "<mac>"

		while True:
				line = self._fileTXT.readline()

				#when it comes to EOF, an empty string will be returned by readline()
				if not line:
						break
				else:
						_IdOrg = map(self._stripEnds, line.split("(hex)")) #split the first with the delimeter "(hex)"
						
						self._fileTXT.readline() #the 2nd line will be omitted

						#read the following 3 to 4 lines which the detail info of manufacturers will be constructed
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
