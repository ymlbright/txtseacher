from xml.sax.handler import ContentHandler
from xml.sax import parse

#-*- coding: utf-8 -*-

class DbXMLHandle(ContentHandler):
	def __init__(self, indict):
		self.indict = indict
		self.name = ''

	def startElement(self, name, attrs):
		self.name = name

	def characters(self, chars):
		if 0x20<ord(chars[0])<0x7e:
			self.indict[self.name] = chars

def DbXmlParser(path):
	rdict = {}
	parse(path,DbXMLHandle(rdict))
	return rdict

if __name__ == '__main__':
	lt = {}
	parse('format.xml', DbXMLHandle(lt))
	for x in lt:
		print x,'-',lt[x]