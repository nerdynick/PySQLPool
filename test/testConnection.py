'''
Created on Jun 23, 2009

@author: nick
'''
import unittest
import PySQLPool
from mock import Mock
try:
	from hashlib import md5 
except Exception, e:
	from md5 import md5

def suite():
	loader = unittest.TestLoader()
	alltests = unittest.TestSuite()
	alltests.addTest(loader.loadTestsFromTestCase(Connection))
		
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
			connection = PySQLPool.connection.Connection(host=self.host, user=self.username, passwd=self.password, db=self.db)
			self.assertTrue(isinstance(connection, PySQLPool.connection.Connection))
		except Exception, e:
			self.fail("Failed to create connection with error: "+str(e))

	def testRawDictConnectionCreation(self):
		"""
		Raw Connection Creation using Kargs/Dict
		"""
		try:
			connection = PySQLPool.connection.Connection(**self.connDict)
			self.assertTrue(isinstance(connection, PySQLPool.connection.Connection))
		except Exception, e:
			self.fail("Failed to create connection with error: "+str(e))
	
	def testQuickConnectionCreation(self):
		"""
		Quick Connection Creation
		"""
		try:
			connection = PySQLPool.getNewConnection(host=self.host, user=self.username, passwd=self.password, db=self.db)
			self.assertTrue(isinstance(connection, PySQLPool.connection.Connection))
		except Exception, e:
			self.fail("Failed to create connection with error: "+str(e))
	
	def testQuickDictConnectionCreation(self):
		"""
		Quick Connection Creation using Kargs/Dict
		"""
		try:
			connection = PySQLPool.getNewConnection(**self.connDict)
			self.assertTrue(isinstance(connection, PySQLPool.connection.Connection))
		except Exception, e:
			self.fail("Failed to create connection with error: "+str(e))
	
	def testAltConnectionOptions(self):
		"""
		Test Creating a connection with alternate arguments
		"""
		try:
			conArgs = {
				"username":"tUser",
				"password":"tPass",
				"schema":"tDB",
			}
			connection = PySQLPool.getNewConnection(**conArgs)
			self.assertEqual(connection.info['user'], conArgs['username'], msg="Usernames don't match")
			self.assertEqual(connection.info['passwd'], conArgs['password'], msg="Passwords don't match")
			self.assertEqual(connection.info['db'], conArgs['schema'], msg="DBs don't match")
		except Exception, e:
			self.fail("Failed to create connection with error: "+str(e))
	
	def testHashKeyGen(self):
		"""
		Test Hash Key Generation
		"""
		try:
			connection = PySQLPool.getNewConnection(**self.connDict)
			hashStr = ''.join([str(x) for x in connection.info.values()])
			key = md5(hashStr).hexdigest()
			self.assertEqual(connection.key, key, msg="Hash Keys don't match")
		except Exception, e:
			self.fail("Failed to create connection with error: "+str(e))
			
	def testPossitionBasedConnectionArgs(self):
		"""
		Test Creating a connection with position based arguments
		"""
		try:
			conArgs = [
				"tHost",
				"tUser",
				"tPass",
				"tDB",
				3306
			]
			connection = PySQLPool.getNewConnection(*conArgs)
			self.assertEqual(connection.info['host'], conArgs[0], msg="Hosts don't match")
			self.assertEqual(connection.info['user'], conArgs[1], msg="Usernames don't match")
			self.assertEqual(connection.info['passwd'], conArgs[2], msg="Passwords don't match")
			self.assertEqual(connection.info['db'], conArgs[3], msg="DBs don't match")
			self.assertEqual(connection.info['port'], conArgs[4], msg="Ports don't match")
		except Exception, e:
			self.fail("Failed to create connection with error: "+str(e))

if __name__ == "__main__":
	unittest.main(defaultTest='suite')