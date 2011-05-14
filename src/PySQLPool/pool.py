"""
@author: Nick Verbeck
@since: date 5/12/2008
@version: 0.2
"""
from threading import Condition
from connection import ConnectionManager

class Pool(object):
	"""
	MySQL Connection Pool Manager
	
	This is the heart of the PySQLPool Library. The borg pattern is used here to store connections and manage the connections.
	
	@author: Nick Verbeck
	@since: 5/18/2008
	@version: 0.2
	"""
	
	#Dictionary used for storing all Connection information
	__Pool = {}
	
	#Max Connections that can be opened among all connections
	maxActiveConnections = 10
	
	def __init__(self):
		"""
		Constructor for PySQLPool
		
		@author: Nick Verbeck
		@since: 5/12/2008
		"""
		self.__dict__ = self.__Pool
		
		#For 1st instantiation lets setup all our variables
		if not self.__dict__.has_key('lock'):
			self.lock = Condition()
			
		if not self.__dict__.has_key('connections'):
			self.connections = {}
		
	def Terminate(self):
		"""
		Close all open connections
		
		Loop though all the connections and commit all queries and close all the connections. 
		This should be called at the end of your application.
		
		@author: Nick Verbeck
		@since: 5/12/2008
		"""
		
		self.lock.acquire()
		try:
			for bucket in self.connections.values():
				try:
					for conn in bucket.values():
						conn.lock.acquire()
						try:
							conn.Close()
						except Exception:
							#We may throw exceptions due to already closed connections
							pass
						conn.lock.release()
				except Exception:
					pass
			self.conn = {}
		finally:
			self.lock.release()

	def Cleanup(self):
		"""
		Cleanup Timed out connections
		
		Loop though all the connections and test if still active. If inactive close socket.
		
		@author: Nick Verbeck
		@since: 2/20/2009
		"""
		self.lock.acquire()
		try:
			for bucket in self.connections.values():
				try:
					for conn in bucket.values():
						conn.lock.acquire()
						try:
							open = conn.TestConnection(forceCheck=True)
							if open is True:
								conn.commit()
						except Exception:
							pass
						conn.lock.release()
				except Exception:
					pass
		finally:
			self.lock.release()
			
	def Commit(self):
		"""
		Commits all currently open connections
		
		@author: Nick Verbeck
		@since: 9/12/2008
		"""
		self.lock.acquire()
		try:
			for bucket in self.connections.values():
				try:
					for conn in bucket.values():
						conn.lock.acquire()
						try:
							conn.commit()
						except Exception:
							pass
						conn.lock.release()
				except Exception:
					pass
		finally:
			self.lock.release()
		
	def GetConnection(self, ConnectionObj):
		"""
		Get a Open and active connection
		
		Returns a PySQLConnectionManager if one is open else it will create a new one if the max active connections hasn't been hit.
		If all possible connections are used. Then None is returned.
		
		@param PySQLConnectionObj: PySQLConnection Object representing your connection string
		@author: Nick Verbeck
		@since: 5/12/2008   
		"""
		
		#Lock the Connection Collection/Pool
		
		key = ConnectionObj.key
		
		connection = None
		
		if self.connections.has_key(key):
			for conn in self.connections[key].values():
				#Grab an active connection if maxActivePerConnection is not meet
				#TODO: Implement a max usage per connection object
				if not conn.is_locked():
					conn.lock()
					try:
						if conn.TestConnection() is False:
							conn.ReConnect()
							
						connection = conn
						conn.release()
					except Exception:
						conn.release()
						raise
				
			if connection is None:
				#Create a new Connection if Max Connections is not meet
				connKey = len(self.connections[key])
				if connKey <= self.maxActiveConnections:
					self.lock.acquire()
					self.connections[key][connKey] = self._createConnection(ConnectionObj)
					self.lock.release()
				else:
					#TODO: We have maxed out a connection pool. Wait for a connection to become free
					pass
					
		#Create new Connection Pool Set
		else:
			self.lock.acquire()
			self.connections[key] = {}
			self.connections[key][0] = self._createConnection(ConnectionObj)
			self.lock.release()

		if connection is not None:
			connection.activeConnections += 1
			
		return connection
	
	def _createConnection(self, info):
		connection = ConnectionManager(info)
		connection.Connect()
		
		return connection
	
	def returnConnection(self, connObj):
		"""
		Return connection back to the pool for reuse.
		
		@author: Nick Verbeck
		@since: 5/12/2008
		"""
		connObj.activeConnections -= 1
		connObj.query = None
		connObj.lock.release()
