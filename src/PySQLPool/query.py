"""
@author: Nick Verbeck
@since: date 5/12/2008
"""

import time
import MySQLdb
from pool import Pool
import log

class PySQLQuery(object):
	"""
	Front-End class used for interaction with the PySQLPool core
	
	This class is used to execute queries and to request a currently open connection from the pool. 
	If no open connections exist a new one is created by the pool.
	
	@author: Nick Verbeck
	@since: 5/12/2008
	@version: 0.1
	"""
	
	def __init__(self, PySQLConnectionObj, commitOnEnd = False):
		"""
		Constructor for PySQLQuery Class
		
		@param PySQLConnectionObj: PySQLConnection Object representing your connection string
		@param commitOnEnd: Default False, When query is complete do you wish to auto commit. This is a one time auto commit
		@author: Nick Verbeck
		@since: 5/12/2008
		"""
		self.connInfo = PySQLConnectionObj
		self.record = {}
		self.rowcount = 0
		self.affectedRows = None
		#The Real Connection to the DB
		self.conn = None
		self.lastError = None
		self.lastInsertID = None
		
	def __del__(self):
		"""
		On destruct make sure the current connection is returned back to the pool for use later
		
		@author: Nick Verbeck
		@since: 5/12/2008
		"""
		if self.conn is not None:
			self._ReturnConnection()
	
	def __enter__(self):
		"""
		Starts transaction, used with the 'with' statement.
		@author: Denis Malinovsky
		@since: 5/21/2010
		"""
		self.Query('START TRANSACTION')
		log.logger.info('Starting Transaction')
	
	def __exit__(self, exc_type, exc_value, traceback):
		"""
		Commits transaction, if no exception was raised.
		@author: Denis Malinovsky
		@since: 5/21/2010
		"""
		if exc_type is None:
			self.Query('COMMIT')
			log.logger.info('Commiting Transaction')
		else:
			self.Query('ROLLBACK')
			log.logger.info('Rolling Back Transaction')
		
	#TODO: In the future lets decorate all our query calls with a connection fetching and releasing handler. Help to centralize all this logic for use in transactions in the future.
	def query(self, query, args=None):
		"""
		Execute the passed in query against the database
		
		@param query: MySQL Query to execute. %s or %(key)s will be replaced by parameter args sequence
		@param args: Sequence of value to replace in your query. A mapping may also be used but your query must use %(key)s
		@author: Nick Verbeck
		@since: 5/12/2008
		"""
		self.affectedRows = None
		self.lastError = None
		cursor = None
		
		try:
			try:
				self._GetConnection()
				
				log.logger.debug('Running query "%s" with args "%s"', query, args)
				self.conn.query = query
				
				#Execute query and store results
				cursor = self.conn.getCursor()
				self.affectedRows = cursor.execute(query, args)
				self.lastInsertID = self.conn.connection.insert_id()
				self.rowcount = cursor.rowcount
				
				log.logger.debug('Query Resulted in %s affected rows, %s rows returned, %s last insert id', self.affectedRows, self.lastInsertID, self.rowcount)
				
				self.record = cursor.fetchall()
				self.conn.updateCheckTime()
			except Exception, e:
				self.lastError = e
				self.affectedRows = None
		finally:
			if cursor is not None:
				cursor.close()
			self._ReturnConnection()
			if self.lastError is not None:
				raise self.lastError
			else:
				return self.affectedRows
	execute = Query = query
	
	def queryOne(self, query, args=None):
		"""
		Execute the passed in query against the database. 
		Uses a Generator & fetchone to reduce your process memory size.
		
		@param query: MySQL Query to execute. %s or %(key)s will be replaced by parameter args sequence
		@param args: Sequence of value to replace in your query. A mapping may also be used but your query must use %(key)s
		@author: Nick Verbeck
		@since: 5/12/2008
		"""
		
		self.affectedRows = None
		self.lastError = None
		cursor = None
		try:
			try:
				self._GetConnection()
				self.conn.query = query
				#Execute query
				cursor = self.conn.getCursor()
				self.affectedRows = cursor.execute(query, args)
				self.conn.updateCheckTime()
				while 1:
					row = cursor.fetchone()
					if row is None:
						break
					else:
						self.record = row
						yield row
						
				self.rowcount = cursor.rowcount
			except Exception, e:
				self.lastError = e
				self.affectedRows = None
		finally:
			if cursor is not None:
				cursor.close()
			self._ReturnConnection()
			if self.lastError is not None:
				raise self.lastError
			else:
				raise StopIteration
	executeOne = QueryOne = queryOne
			
	def queryMany(self, query, args):
		"""
		Executes a series of the same Insert Statments
		
		Each tuple in the args list will be applied to the query and executed.
		This is the equivilant of MySQLDB.cursor.executemany()
		
		@author: Nick Verbeck
		@since: 9/7/2008
		"""
		self.lastError = None
		self.affectedRows = None
		self.rowcount = None
		self.record = None
		cursor = None
		
		try:
			try:
				self._GetConnection()
				self.conn.query = query
				#Execute query and store results
				cursor = self.conn.getCursor()
				self.affectedRows = cursor.executemany(query, args)
				self.conn.updateCheckTime()
			except Exception, e:
				self.lastError = e
		finally:
			if cursor is not None:
				cursor.close()
			self._ReturnConnection()
			if self.lastError is not None:
				raise self.lastError
			else:
				return self.affectedRows
	executeMany = queryMany
			
	def queryMulti(self, queries):
		"""
		Execute a series of Deletes,Inserts, & Updates in the Queires List
		
		@author: Nick Verbeck
		@since: 9/7/2008
		"""
		self.lastError = None
		self.affectedRows = 0
		self.rowcount = None
		self.record = None
		cursor = None
		
		try:
			try:
				self._GetConnection()
				#Execute query and store results
				cursor = self.conn.getCursor()
				for query in queries:
					self.conn.query = query
					if query.__class__ == [].__class__:
						self.affectedRows += cursor.execute(query[0], query[1])
					else:
						self.affectedRows += cursor.execute(query)
				self.conn.updateCheckTime()
			except Exception, e:
				self.lastError = e
		finally:
			if cursor is not None:
				cursor.close()
			self._ReturnConnection()
			if self.lastError is not None:
				raise self.lastError
			else:
				return self.affectedRows
	executeMulti = queryMulti
	
	def _GetConnection(self):
		"""
		Retieves a prelocked connection from the Pool
		
		@author: Nick Verbeck
		@since: 9/7/2008
		"""
		#Attempt to get a connection. If all connections are in use and we have reached the max number of connections,
		#we wait 1 second and try again.
		#The Connection is returned locked to be thread safe
		while self.conn is None:
			self.conn = Pool().GetConnection(self.connInfo)
			if self.conn is not None:
				break
			else:
				time.sleep(1)

	def _ReturnConnection(self):
		"""
		Returns a connection back to the pool
		
		@author: Nick Verbeck
		@since: 9/7/2008
		"""
		if self.conn is not None:
			if self.connInfo.commitOnEnd is True or self.commitOnEnd is True:
				self.conn.Commit()
					
			Pool().returnConnection(self.conn)
			self.conn = None
			
	def escape_string(self, string):
		"""
		This is just an adapter function to allow previus users of MySQLdb. 
		To be familier with there names of functions.
		
		@see: escapeString
		"""
		return MySQLdb.escape_string(string)
	
	def escapeString(self, string):
		"""
		Escapes a string for use in a query
		
		This is the equivilate and MySQLdb.escape_string()
		
		@author: Nick Verbeck
		@since: 9/7/2008
		"""
		return MySQLdb.escapeString(string)
	
	def escape(self, string):
		"""
		Escapes a string for use in a query
		
		This is the equivilate and MySQLdb.escape()
		
		@author: Nick Verbeck
		@since: 9/7/2008
		"""
		return MySQLdb.escape(string)
