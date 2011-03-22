'''
Created on Mar 22, 2011

@author: nick
'''
'''
Created on Jun 23, 2009

@author: nick
'''
import unittest
import PySQLPool

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(Query)

class Query(unittest.TestCase):
    
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
        self.connection = PySQLPool.connection.PySQLConnection(**self.connDict)
            
    def testRawQueryCreation(self):
        """
        Raw Query Creation
        """
        try:
            query = PySQLPool.query.PySQLQuery(self.connection)
            self.assertTrue(isinstance(query, PySQLPool.query.PySQLQuery))
        except Exception, e:
            self.fail('Failed to create PySQLQuery Object with error: '+str(e))
            
    def testQuickQueryCreation(self):
        """
        Quick Query Creation
        """
        try:
            query = PySQLPool.getNewQuery(self.connection)
            self.assertTrue(isinstance(query, PySQLPool.query.PySQLQuery))
        except Exception, e:
            self.fail('Failed to create PySQLQuery Object with error: '+str(e))


if __name__ == "__main__":
    unittest.main(defaultTest='suite')