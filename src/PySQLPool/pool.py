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
					for conn in bucket:
						conn.lock()
						try:
							conn.Close()
						except Exception:
							#We may throw exceptions due to already closed connections
							pass
						conn.release()
				except Exception:
					pass
			self.connections = {}
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
					for conn in bucket:
						conn.lock()
						try:
							open = conn.TestConnection(forceCheck=True)
							if open is True:
								conn.commit()
							else:
								#Remove the connection from the pool. Its dead better of recreating it.
								index = bucket.index(conn)
								del bucket[index]
							conn.release()
						except Exception:
							conn.release()
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
					for conn in bucket:
						conn.lock()
						try:
							conn.commit()
							conn.release()
						except Exception:
							conn.release()
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
		
		key = ConnectionObj.getKey()
		
		connection = None
		
		if self.connections.has_key(key):
			connection = self._getConnectionFromPoolSet(key)
			
			if connection is None:
				self.lock.acquire()
				if len(self.connections[key]) < self.maxActiveConnections:
					#Create a new connection
					connection = self._createConnection(ConnectionObj)
					self.connections[key].append(connection)
					self.lock.release()
				else:
					#Wait for a free connection. We maintain the lock on the pool so we are the 1st to get a connection.
					while connection is None:
						connection = self._getConnectionFromPoolSet(key)
					self.lock.release()
					
		#Create new Connection Pool Set
		else:
			self.lock.acquire()
			#We do a double check now that its locked to be sure some other thread didn't create this while we may have been waiting.
			if not self.connections.has_key(key):
				self.connections[key] = []
			
			if len(self.connections[key]) < self.maxActiveConnections:
				#Create a new connection
				connection = self._createConnection(ConnectionObj)
				self.connections[key].append(connection)
			else:
				#A rare thing happened. So many threads created connections so fast we need to wait for a free one.
				while connection is None:
					connection = self._getConnectionFromPoolSet(key)
			self.lock.release()
			
		return connection
	
	def _getConnectionFromPoolSet(self, key):
		connection = None
		
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
				
		return connection
				
	
	def _createConnection(self, info):
		connection = ConnectionManager(info)
		connection.Connect()
		
		return connection
