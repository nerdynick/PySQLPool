'''
Created on Jun 23, 2009

@author: nick
'''
import unittest
import PySQLPool

def suite():
	return unittest.TestLoader().loadTestsFromTestCase(Connection)

class Connection(unittest.TestCase):
	
	def setUp(self):
		self.username = 'unittest'
		self.password = 'zEzaj37u'
		self.host = 'localhost'
		self.db = 'employees'

	def testRawConnectionCreation(self):
		"""
		Raw Connection Creation
		"""
		try:
			connection = PySQLPool.PySQLConnection.PySQLConnection(host=self.host, user=self.username, passwd=self.password, db=self.db)
		except Exception, e:
			self.fail("Failed to create connection with error: "+str(e))

	def testRawDictConnectionCreation(self):
		"""
		Raw Connection Creation using Kargs/Dict
		"""
		try:
			connDict = {
					"host":self.host,
					"user":self.username,
					"passwd":self.password,
					"db":self.db}
			connection = PySQLPool.PySQLConnection.PySQLConnection(**connDict)
		except Exception, e:
			self.fail("Failed to create connection with error: "+str(e))
	
	def testQuickConnectionCreation(self):
		"""
		Quick Connection Creation
		"""
		try:
			connection = PySQLPool.getNewConnection(host=self.host, user=self.username, passwd=self.password, db=self.db)
		except Exception, e:
			self.fail("Failed to create connection with error: "+str(e))
	
	def testQuickDictConnectionCreation(self):
		"""
		Quick Connection Creation using Kargs/Dict
		"""
		try:
			connDict = {
					"host":self.host,
					"user":self.username,
					"passwd":self.password,
					"db":self.db}
			connection = PySQLPool.getNewConnection(**connDict)
		except Exception, e:
			self.fail("Failed to create connection with error: "+str(e))
			
	def testRawQueryCreation(self):
		"""
		Raw Query Creation
		"""
		try:
			connDict = {
						"host":self.host,
						"user":self.username,
						"passwd":self.password,
						"db":self.db}
			connection = PySQLPool.getNewConnection(**connDict)
			query = PySQLPool.PySQLQuery.PySQLQuery(connection)
		except Exception, e:
			self.fail('Failed to create PySQLQuery Object')
			
	def testQuickQueryCreation(self):
		"""
		Quick Query Creation
		"""
		try:
			connDict = {
						"host":self.host,
						"user":self.username,
						"passwd":self.password,
						"db":self.db}
			connection = PySQLPool.getNewConnection(**connDict)
			query = PySQLPool.getNewQuery(connection)
		except Exception, e:
			self.fail('Failed to create PySQLQuery Object')

	def testDBConnection(self):
		"""
		Test actual connection to Database
		"""
		connDict = {
					"host":self.host,
					"user":self.username,
					"passwd":self.password,
					"db":self.db}
		connection = PySQLPool.getNewConnection(**connDict)
		query = PySQLPool.getNewQuery(connection)
		query.Query("select current_user")
		result = str(query.record[0]['current_user']).split('@')[0]
		self.assertEqual(result, 'unittest', "DB Connection Failed")


if __name__ == "__main__":
	unittest.main(defaultTest='suite')