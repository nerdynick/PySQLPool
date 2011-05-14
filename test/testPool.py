'''
Created on May 14, 2011

@author: nick
'''
import unittest
from PySQLPool import pool, connection
from mock import Mock

def suite():
    loader = unittest.TestLoader()
    alltests = unittest.TestSuite()
    alltests.addTest(loader.loadTestsFromTestCase(Pool))
        
    return alltests

class Pool(unittest.TestCase):
    def setUp(self):
        
        self.connDict = {
                    "host":'localhost',
                    "user":'unittest',
                    "passwd":'zEzaj37u',
                    "db":'employees'}
    
    def testPoolBorg(self):
        poolObj = pool.Pool()
        poolObj2 = pool.Pool()
        
        self.assertTrue(poolObj.connections is poolObj2.connections, msg="Connections don't match")
        self.assertTrue(poolObj.lock is poolObj2.lock, msg="Lock dosn't match")
        
    
    def testPoolGetConnection(self):
        #Create a mock connection object
        connObj = Mock(spec=connection.Connection)
        connObj.getKey.return_value = 'test_key'
        
        #Override the ConnectionManager for the Pool
        connManager = Mock(spec=connection.ConnectionManager)
        connManager.return_value = connManager
        connManager.is_locked.return_value = False
        pool.ConnectionManager = connManager
        
        #Make sure we get a ConnectionManager Object back
        connManObj = pool.Pool().GetConnection(connObj)
        self.assertTrue(isinstance(connManObj, connection.ConnectionManager), msg="Didn't get a ConnectionManager Object back")
        
        #Make sure our pool set persisted
        self.assertTrue(pool.Pool().connections.has_key('test_key'), msg="Pool doesn't contain our pool set")
        
        #Make sure our pool set only contains 1 connection object
        self.assertTrue(len(pool.Pool().connections['test_key']) == 1, msg="Pool doesn't contain only 1 connection for our pool set")
        
        #Re-fetch our ConnectionManager to make sure 2nd lookup work
        connManObj = pool.Pool().GetConnection(connObj)
        
        #Make sure our pool set only contains 1 connection object even after a 2nd call
        self.assertTrue(len(pool.Pool().connections['test_key']) == 1, msg="Pool doesn't contain only 1 connection for our pool set on 2nd call")
        
        #Make sure the correct methods where called as needed on the ConnectionManager
        connManager.Connect.assert_called_once_with()
        connManager.lock.assert_called_once_with()
        connManager.TestConnection.assert_called_once_with()
        connManager.release.assert_called_once_with()
        
    
    def testPoolTerminate(self):
        pass
    
    def testPoolCleanup(self):
        pass
    
    def testPoolCommit(self):
        pass
    
    def testPoolConnectionCreation(self):
        pass
    
    def testPoolMultiThreadGetConnection(self):
        pass
    
    def testPoolMultiThreadGetConnectionWithTransactions(self):
        pass

if __name__ == "__main__":
    unittest.main(defaultTest='suite')