'''
Created on Jun 23, 2009

@author: nick
'''
import unittest
import PySQLPool
from mock import Mock

def suite():
	loader = unittest.TestLoader()
	alltests = unittest.TestSuite()
	alltests.addTest(loader.loadTestsFromTestCase(Connection))
	alltests.addTest(loader.loadTestsFromTestCase(ConnectionManager))
		
	return alltests
#	return unittest.TestLoader().loadTestsFromTestCase(Connection)

class Connection(unittest.TestCase):
	
	def setUp(self):
		self.username = 'unittest'
		self.password = 'zEzaj37u'
		self.host = 'localhost'
		self.db = 'employees'
		
		
		self.connDict = {
					"host":self.host,
					"user":self.username,
					"passwd":self.password,
					"db":self.db}

	def testRawConnectionCreation(self):
		"""
		Raw Connection Creation
		"""
		try:
			connection = PySQLPool.connection.PySQLConnection(host=self.host, user=self.username, passwd=self.password, db=self.db)
			self.assertTrue(isinstance(connection, PySQLPool.connection.PySQLConnection))
		except Exception, e:
			self.fail("Failed to create connection with error: "+str(e))

	def testRawDictConnectionCreation(self):
		"""
		Raw Connection Creation using Kargs/Dict
		"""
		try:
			connection = PySQLPool.connection.PySQLConnection(**self.connDict)
			self.assertTrue(isinstance(connection, PySQLPool.connection.PySQLConnection))
		except Exception, e:
			self.fail("Failed to create connection with error: "+str(e))
	
	def testQuickConnectionCreation(self):
		"""
		Quick Connection Creation
		"""
		try:
			connection = PySQLPool.getNewConnection(host=self.host, user=self.username, passwd=self.password, db=self.db)
			self.assertTrue(isinstance(connection, PySQLPool.connection.PySQLConnection))
		except Exception, e:
			self.fail("Failed to create connection with error: "+str(e))
	
	def testQuickDictConnectionCreation(self):
		"""
		Quick Connection Creation using Kargs/Dict
		"""
		try:
			connection = PySQLPool.getNewConnection(**self.connDict)
			self.assertTrue(isinstance(connection, PySQLPool.connection.PySQLConnection))
		except Exception, e:
			self.fail("Failed to create connection with error: "+str(e))
		
		
class ConnectionManager(unittest.TestCase):
	
	def setUp(self):
		self.username = 'unittest'
		self.password = 'zEzaj37u'
		self.host = 'localhost'
		self.db = 'employees'
		
		
		self.connDict = {
					"host":self.host,
					"user":self.username,
					"passwd":self.password,
					"db":self.db}

	def testConnectionManagerCreation(self):
		"""
		Test the creation of a Connection Manager Object
		"""
		connectionInfo = PySQLPool.getNewConnection(**self.connDict)
		self.assertTrue(isinstance(connectionInfo, PySQLPool.connection.PySQLConnection))
		
		connection = PySQLPool.connection.PySQLConnectionManager(connectionInfo)
		self.assertTrue(isinstance(connection, PySQLPool.connection.PySQLConnectionManager), msg="Not an instance")
		
	def testConnectionManagerBasicLock(self):
		"""
		Test the locking of a Connection Manager Object
		"""
		connectionInfo = PySQLPool.getNewConnection(**self.connDict)
		self.assertTrue(isinstance(connectionInfo, PySQLPool.connection.PySQLConnection))
		
		connection = PySQLPool.connection.PySQLConnectionManager(connectionInfo)
		self.assertTrue(isinstance(connection, PySQLPool.connection.PySQLConnectionManager), msg="Not an instance")
		
		self.assertFalse(connection._locked, msg="Lock Bool not init false")
		
		locked = connection.lock()
		
		self.assertTrue(connection._locked, msg="Lock Bool not true")
		self.assertTrue(locked, msg="Return not true")
		
		connection.release()
		self.assertFalse(connection._locked, msg="Lock Bool not false")

if __name__ == "__main__":
	unittest.main(defaultTest='suite')