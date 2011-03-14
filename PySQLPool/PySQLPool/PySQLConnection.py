"""
@author: Nick Verbeck
@since: 5/12/2008
"""
import MySQLdb
import datetime
from threading import Semaphore

try:
	from hashlib import md5 
except Exception, e:
	from md5 import md5

class PySQLConnection(object):
	"""
	Command Pattern Object to store connection information for use in PySQLPool
	
	@author: Nick Verbeck
	@since: 5/12/2008
	@version: 0.1
	"""
	
	def __init__(self, *args, **kargs):
		"""
		Constructor for the PySQLConnection class
		@param commitOnEnd: Default False, When query is complete do you wish to auto commit. This is a always on for this connection
		@author: Nick Verbeck
		@since: 5/12/2008
		@updated: 7/19/2008 - Added commitOnEnd
		@updated: 10/26/2008 - Switched to use *args and **kargs
		"""
		self.info = {
					 'host': 'localhost',
					 'user': 'root',
					 'passwd': '',
					 'db': '',
					 'port': 3306
					 }
		if kargs.has_key('host'):
			self.info['host'] = kargs['host']
		if kargs.has_key('user'):
			self.info['user'] = kargs['user']
		if kargs.has_key('passwd'):
			self.info['passwd'] = kargs['passwd']
		if kargs.has_key('db'):
			self.info['db'] = kargs['db']
		if kargs.has_key('port'):
			self.info['port'] = int(kargs['port'])
		if kargs.has_key('connect_timeout'):
			self.info['connect_timeout'] = kargs['connect_timeout']
		if kargs.has_key('use_unicode'):
			self.info['use_unicode'] = kargs['use_unicode']
		if kargs.has_key('charset'):
			self.info['charset'] = kargs['charset']
		if kargs.has_key('local_infile'):
			self.info['local_infile'] = kargs['local_infile']
			
		#Support Legacy Username
		if kargs.has_key('username'):
			self.info['user'] = kargs['username']
		#Support Legacy Password
		if kargs.has_key('password'):
			self.info['passwd'] = kargs['password']
		#Support Legacy Schema
		if kargs.has_key('schema'):
			self.info['db'] = kargs['schema']
			
		if kargs.has_key('commitOnEnd'):
			self.commitOnEnd = kargs['commitOnEnd']
		else:
			self.commitOnEnd = False
			
		hashStr = ''.join([str(x) for x in self.info.values()])
		self.key = md5(hashStr).hexdigest()
		
	def __getattr__(self, name):
		try:
			return self.info[name]
		except Exception, e:
			return None
  

connection_timeout = datetime.timedelta(seconds=20)

class PySQLConnectionManager(object):
	"""
	Physical Connection manager
	
	Used to manage the physical MySQL connection and the thread safe locks on that connection
	
	@author: Nick Verbeck
	@since: 5/12/2008
	@version: 0.1
	"""
	def __init__(self, PySQLConnectionObj):
		"""
		Constructor for PySQLConnectionManager
		
		@param PySQLConnectionObj: PySQLConnection Object representing your connection string
		@author: Nick Verbeck
		@since: 5/12/2008
		"""
		
		self.connectionInfo = PySQLConnectionObj
		self.connection = None
		self.lock = Semaphore()
		self.activeConnections = 0
		self.query = None
		self.lastConnectionCheck = None
		self.Connect()
		
	def updateCheckTime(self):
		self.lastConnectionCheck = datetime.datetime.now()

	def Connect(self):
		"""
		Creates a new physical connection to the database
		
		@author: Nick Verbeck
		@since: 5/12/2008
		"""
		self.connection = MySQLdb.connect(*[], **self.connectionInfo.info)
		self.updateCheckTime()
		
	def ReConnect(self):
		"""
		Attempts to close current connection if open and re-opens a new connection to the database
		
		@author: Nick Verbeck
		@since: 5/12/2008
		"""
		self.Close()
		self.Connect()
		
	def TestConnection(self, forceCheck = False):
		"""
		Tests the current physical connection if it is open and hasn't timed out
		
		@return: boolean True is connection is open, False if connection is closed
		@author: Nick Verbeck
		@since: 5/12/2008
		"""
		if self.connection is None:
			return False
		else:
			if forceCheck is True or (datetime.datetime.now() - self.lastConnectionCheck) >= connection_timeout:
				try:
					cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
					cursor.execute('select current_user')
					self.updateCheckTime()
					return True
				except Exception, e:
					self.connection.close()
					self.connection = None
					return False
			else:
				return True
			
	def Commit(self):
		"""
		Commit MySQL Transaction to database
		
		@author: Nick Verbeck
		@since: 5/12/2008
		"""
		try:
			self.connection.commit()
			self.updateCheckTime()
		except Exception, e:
			pass
	
	def Close(self):
		"""
		Commits and closes the current connection
		
		@author: Nick Verbeck
		@since: 5/12/2008
		"""
		if self.connection is not None:
			try:
				self.connection.commit()
				self.connection.close()
				self.connection = None
			except Exception, e:
				pass
