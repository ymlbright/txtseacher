#-*- coding: utf-8 -*-

import os, sys
from DbXmlParser import DbXmlParser
from logger import logger
reload(sys)
encoding_list = ['gbk', 'utf-8', 'ascii']

class DbObject(object):
	def __init__(self, path):
		self.path = path
		self.enabled = True
		self.readDbinfo()
		self.encoding = 2

	def readDbinfo(self):
		try:
			xml = DbXmlParser(os.path.join(self.path,'format.xml'))
			self.name = xml['source']
			self.extension = xml['extension']
			self.startline = xml['startline']
			self.splitchar = xml['splitchar'].replace('\\t','\t').replace('\\ ',' ')
			self.startno = xml['startno']
			self.endno = xml['endno']
			self.xml = xml
			self.meta = xml['filed'].split(',')
		except:
			self.enabled = False
			logger.debug('Read database information error. Path: %s'% self.path)

	def find(self, sstr, stype=''):
		fline = []
		for i in range(int(self.startno),int(self.endno)+1):
			filename = os.path.join(self.path, '%02d.%s'%(i, self.extension))
			logger.info('\t\t%s - %s [%d/%d]'%(self.name, self.xml['date'], i, int(self.endno)))
			try:
				encoding_change_count = 0
				fp = open(filename)
				for skipline in range(0, int(self.startline)+1):
					l = fp.readline()
				while l:
					try:
						if not l.find(sstr) == -1:
							logger.info("!!!Founded in %s."%filename)
							if stype != 'all':
								return l.split(self.splitchar)
							res = l.split(self.splitchar)
							logger.debug(res)
							fline.append(res)
						l = fp.readline()
					except UnicodeDecodeError:
						if encoding_change_count<=len(encoding_list):
							self.encoding = (self.encoding+1)%len(encoding_list)
							encoding_change_count += 1
							sys.setdefaultencoding(encoding_list[self.encoding])
							logger.debug('DecodeError, try to change default encoding to %s', encoding_list[self.encoding])
						else:
							logger.warning('Can\'t to decode file %s in %d'%(filename, fp.tell()))
							break
					except:
						logger.warning('Unknown error when reading file %s in %d.'%(filename, fp.tell()))
				fp.close()
			except:
				print sys.exc_info()
				logger.debug('Can\'t operate file %s'%filename)
		return fline

	def info(self):
		if self.enabled:
			return self.xml['source']+'\t'+self.xml['date']+'\t'+self.xml['size']+'\t'+self.xml['main']
		else:
			return 'Database error.'

	def meta_info(self):
		return "Database\tDate\tSize\tContent"

class Db(object):
	def __init__(self, basepath):
		self.basepath = basepath
		self.dblist = []
		self.Dbfounder()

	def Dbfounder(self):
		for d in os.listdir(self.basepath):
			newP = os.path.join(self.basepath,d)
			if os.path.isdir(newP):
				if self.DbCheck(newP):
					self.dblist.append(DbObject(newP))

	def DbCheck(self, path):
		return os.path.isfile(os.path.join(path,'format.xml'))

	def enabled(self):
		return len(self.dblist)

if __name__ == '__main__':
	D = Db('Datapath')
	i = 3
	x = D.dblist[i].find('123456')
	if x:
		print D.dblist[i].meta
		print x
	else:
		print "Nothing found."