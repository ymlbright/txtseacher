#-*- coding: utf-8 -*-

from DbDirectoryParser import Db
from logger import logger, output
from getopt import getopt, GetoptError
import os, logging, sys

class DbSearcher(object):
	def __init__(self, basepath=''):
		self.basepath = basepath
		if self.basepath:
			self.D = Db(self.basepath)

	def load(self, basepath):
		self.basepath = basepath
		self.D = Db(self.basepath)

	def finddb(self, dbname):
		if self.D.enabled:
			for i in range(0, len(self.D.dblist)):
				if self.D.dblist[i].name == dbname:
					return i

	def search(self, dbindex, dstr):
		logger.info("Start to search \"%s\" in %s"%(dstr, self.D.dblist[dbindex].name))
		r = self.search_(dbindex, dstr)
		if not r:
			logger.info('Nothing found.')
			return 
		self.arrayprint(self.D.dblist[dbindex].meta)
		self.arrayprint(r)

	def search_(self, dbindex, dstr):
		if self.D.enabled:
			return self.D.dblist[dbindex].find(dstr)

	def searchall(self, dbindex, dstr):
		logger.info("Start to search \"%s\" in %s with all matches"%(dstr, self.D.dblist[dbindex].name))
		r = self.searchall_(dbindex, dstr)
		if not r:
			logger.info('Nothing found.')
			return 
		self.arrayprint(self.D.dblist[dbindex].meta)
		for m in r:
			self.arrayprint(m)

	def searchall_(self, dbindex, dstr):
		if self.D.enabled:
			return self.D.dblist[dbindex].find(dstr, 'all')

	def searchalldb(self, dstr):
		if self.D.enabled:
			for i in range(0, len(self.D.dblist)):
				self.searchall(i,dstr)

	def showdb(self):
		if self.D.enabled:
			output.info('#\t'+self.D.dblist[0].meta_info())
			for i in range(0, len(self.D.dblist)):
				output.info(('%d\t'%i)+self.D.dblist[i].info())

	def arrayprint(self, array):
		s = ''
		for a in array:
			s += "%s\t"%a
		output.info(s[:-2])

def _clear():
	if os.path.isfile('search.log'):
		os.remove('search.log')
	print 'Clear finished.'
	sys.exit(2)

def _log():
	file_handler = logging.FileHandler('search.log')
	file_handler.setFormatter(logging.Formatter('[%(asctime)s] %(message)s', \
			'%H:%M:%S'))
	file_handler.setLevel(logging.DEBUG)
	logger.addHandler(file_handler)

def _output(filepath):
	file_handler = logging.FileHandler(filepath)
	file_handler.setFormatter(logging.Formatter('%(message)s'))
	file_handler.setLevel(logging.INFO)
	output.addHandler(file_handler)

def usage():
	u = '''Database seacher v1.0 Usage:
	-c           \tClear log file
	-o [filename]\tSave result to a file
	-l           \tWrite programe log into search.log
	-f [string]  \tFind string in database
	-s           \tShow current database
	-d [index]   \tUse the database of index
	-a           \tSearch all matches items
	-A           \tSearch in all database[Slow!]
	-p [datapath]\tSet the folder of database
	-v           \tShow detial info
	'''
	print u
	sys.exit()

if __name__ == '__main__':
	try:
		opts, args = getopt(sys.argv[1:], 'hco:lf:sd:aAp:v')
	except GetoptError as err:
		print str(err)
		usage()
	if not opts:
		usage()

	datapath = '/media/bright/43955604-e871-419c-bdfd-216a3b3637bb/Database'
	fstr = ''
	dbindex = -1
	search_range = '' 
	show = False
	for o,a in opts:
		if o == '-h':
			usage()
		elif o == '-c':
			_clear()
		elif o == '-o':
			_output(a)
		elif o == '-l':
			_log()
		elif o == '-f':
			fstr = a
		elif o == '-s':
			show = True
		elif o == '-d':
			dbindex = int(a)
		elif o == '-a':
			search_range = 'all'
		elif o == '-A':
			search_range = 'all database'
		elif o == '-p':
			datapath = a
		elif o == '-v':
			logger.setLevel(logging.DEBUG)

	D = DbSearcher(datapath)
	if datapath and show:
		D.showdb()
		sys.exit()
	if search_range == 'all':
		if dbindex > -1 and fstr != '':
			D.searchall(dbindex, fstr)
		else:
			usage()
	elif search_range == 'all database':
		if fstr != '':
			logger.setLevel(logging.DEBUG)
			D.searchalldb(fstr)
		else:
			usage()
	else:
		if dbindex > -1 and fstr != '':
			D.search(dbindex, fstr)
		else:
			usage()